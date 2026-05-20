from src.controllers.article_controller import router as article_router
from src.controllers.article_sentence_controller import router as article_sentence_router
from src.controllers.llm_sentence_translation_controller import (
    router as llm_sentence_translation_router,
)
from src.controllers.translation_controller import router as translation_router
from src.controllers.user_sentence_translation_controller import (
    router as user_sentence_translation_router,
)

__all__ = [
    "article_router",
    "article_sentence_router",
    "llm_sentence_translation_router",
    "translation_router",
    "user_sentence_translation_router",
]
