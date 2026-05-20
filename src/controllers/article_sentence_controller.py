from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.exceptions.app_exception import InvalidRequestException
from src.exceptions.response_code import ResponseCode
from src.models import ArticleSentence


router = APIRouter(
    prefix="/article-sentences",
    tags=["article-sentences"],
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
async def list_article_sentences(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    article_id: int | None = Query(None),
    language_type: str | None = Query(None),
    db: Session = Depends(get_db),
) -> dict:
    """Get article_sentence list."""

    query = select(ArticleSentence)
    if article_id is not None:
        query = query.where(ArticleSentence.article_id == article_id)
    if language_type:
        query = query.where(ArticleSentence.language_type == language_type)

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    sentences = db.scalars(
        query.order_by(
            ArticleSentence.article_id.desc(),
            ArticleSentence.sentence_index.asc(),
        )
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return _success_response(
        _page_response(
            [_article_sentence_to_dict(sentence) for sentence in sentences],
            total,
            page,
            page_size,
        )
    )


@router.get("/{sentence_id}")
async def get_article_sentence_detail(
    sentence_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """Get article_sentence detail."""

    sentence = db.get(ArticleSentence, sentence_id)
    if sentence is None:
        _not_found("文章句子不存在")

    return _success_response(_article_sentence_to_dict(sentence))
