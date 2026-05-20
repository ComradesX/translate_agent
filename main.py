from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.config.app_config import AppConfig
from src.controllers import (
    article_router,
    article_sentence_router,
    llm_sentence_translation_router,
    translation_router,
    user_sentence_translation_router,
)
from src.exceptions.handler import register_exception_handlers

WEB_DIR = Path(__file__).resolve().parent / "src" / "resource" / "web"


def create_app() -> FastAPI:
    app = FastAPI(title="translate-agent")
    app.include_router(article_router)
    app.include_router(article_sentence_router)
    app.include_router(llm_sentence_translation_router)
    app.include_router(translation_router)
    app.include_router(user_sentence_translation_router)
    app.mount("/web", StaticFiles(directory=WEB_DIR, html=True), name="web")
    register_exception_handlers(app)

    @app.get("/", include_in_schema=False)
    async def index() -> RedirectResponse:
        return RedirectResponse(url="/web/")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=AppConfig.app_port(),
        reload=AppConfig.is_dev(),
    )
