from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.exceptions.app_exception import InvalidRequestException
from src.exceptions.response_code import ResponseCode
from src.models import ArticleSentence, UserSentenceTranslation


router = APIRouter(
    prefix="/user-sentence-translations",
    tags=["user-sentence-translations"],
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


def _decimal_to_float(value: Decimal | None) -> float | None:
    if value is None:
        return None
    return float(value)


def _user_sentence_translation_to_dict(translation: UserSentenceTranslation) -> dict:
    return {
        "id": translation.id,
        "user_id": translation.user_id,
        "article_id": translation.article_id,
        "sentence_id": translation.sentence_id,
        "target_language": translation.target_language,
        "translation_content": translation.translation_content,
        "ai_score": _decimal_to_float(translation.ai_score),
        "ai_comment": translation.ai_comment,
        "created_time": translation.created_time.isoformat(),
        "updated_time": translation.updated_time.isoformat(),
    }


def _article_sentence_to_dict(sentence: ArticleSentence) -> dict:
    return {
        "id": sentence.id,
        "article_id": sentence.article_id,
        "sentence_content": sentence.sentence_content,
        "sentence_index": sentence.sentence_index,
        "language_type": sentence.language_type,
        "created_time": sentence.created_time.isoformat(),
    }


@router.get("")
@router.get("/")
async def list_user_sentence_translations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: int | None = Query(None),
    article_id: int | None = Query(None),
    sentence_id: int | None = Query(None),
    target_language: str | None = Query(None),
    db: Session = Depends(get_db),
) -> dict:
    """Get user_sentence_translation list."""

    query = select(UserSentenceTranslation)
    if user_id is not None:
        query = query.where(UserSentenceTranslation.user_id == user_id)
    if article_id is not None:
        query = query.where(UserSentenceTranslation.article_id == article_id)
    if sentence_id is not None:
        query = query.where(UserSentenceTranslation.sentence_id == sentence_id)
    if target_language:
        query = query.where(UserSentenceTranslation.target_language == target_language)

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    translations = db.scalars(
        query.order_by(UserSentenceTranslation.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return _success_response(
        _page_response(
            [
                _user_sentence_translation_to_dict(translation)
                for translation in translations
            ],
            total,
            page,
            page_size,
        )
    )


@router.get("/latest-sentence")
async def get_latest_user_translation_sentence(
    article_id: int = Query(..., ge=1),
    user_id: int = Query(0, ge=0),
    target_language: str | None = Query(None),
    db: Session = Depends(get_db),
) -> dict:
    """Get the latest user translation and its sentence for an article."""

    query = select(UserSentenceTranslation).where(
        UserSentenceTranslation.article_id == article_id,
        UserSentenceTranslation.user_id == user_id,
    )
    if target_language:
        query = query.where(UserSentenceTranslation.target_language == target_language)

    translation = db.scalars(
        query.order_by(
            UserSentenceTranslation.updated_time.desc(),
            UserSentenceTranslation.id.desc(),
        ).limit(1)
    ).first()
    if translation is None:
        return _success_response(
            {
                "translation": None,
                "sentence": None,
            }
        )

    sentence = db.get(ArticleSentence, translation.sentence_id)
    return _success_response(
        {
            "translation": _user_sentence_translation_to_dict(translation),
            "sentence": _article_sentence_to_dict(sentence) if sentence else None,
        }
    )


@router.get("/{translation_id}")
async def get_user_sentence_translation_detail(
    translation_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """Get user_sentence_translation detail."""

    translation = db.get(UserSentenceTranslation, translation_id)
    if translation is None:
        _not_found("用户翻译不存在")

    return _success_response(_user_sentence_translation_to_dict(translation))
