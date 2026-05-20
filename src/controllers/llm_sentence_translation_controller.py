from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.exceptions.app_exception import InvalidRequestException
from src.exceptions.response_code import ResponseCode
from src.models import LlmSentenceTranslation


router = APIRouter(
    prefix="/llm-sentence-translations",
    tags=["llm-sentence-translations"],
)


def _success_response(data: dict) -> dict:
    return {
        "code": ResponseCode.SUCCESS,
        "message": "success",
        "data": data,
    }


def _not_found(message: str) -> None:
    raise InvalidRequestException(message, code=ResponseCode.NOT_FOUND_RESOURCE)


def _page_response(items: list[dict], total: int, page: int, page_size: int) -> dict:
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


def _llm_sentence_translation_to_dict(translation: LlmSentenceTranslation) -> dict:
    return {
        "id": translation.id,
        "sentence_id": translation.sentence_id,
        "source_language": translation.source_language,
        "target_language": translation.target_language,
        "translation_content": translation.translation_content,
        "model_name": translation.model_name,
        "created_time": translation.created_time.isoformat(),
    }


@router.get("")
@router.get("/")
async def list_llm_sentence_translations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sentence_id: int | None = Query(None),
    target_language: str | None = Query(None),
    model_name: str | None = Query(None),
    db: Session = Depends(get_db),
) -> dict:
    """Get llm_sentence_translation list."""

    query = select(LlmSentenceTranslation)
    if sentence_id is not None:
        query = query.where(LlmSentenceTranslation.sentence_id == sentence_id)
    if target_language:
        query = query.where(LlmSentenceTranslation.target_language == target_language)
    if model_name:
        query = query.where(LlmSentenceTranslation.model_name == model_name)

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    translations = db.scalars(
        query.order_by(LlmSentenceTranslation.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return _success_response(
        _page_response(
            [
                _llm_sentence_translation_to_dict(translation)
                for translation in translations
            ],
            total,
            page,
            page_size,
        )
    )


@router.get("/{translation_id}")
async def get_llm_sentence_translation_detail(
    translation_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """Get llm_sentence_translation detail."""

    translation = db.get(LlmSentenceTranslation, translation_id)
    if translation is None:
        _not_found("LLM 翻译不存在")

    return _success_response(_llm_sentence_translation_to_dict(translation))
