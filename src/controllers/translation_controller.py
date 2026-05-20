from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.chain.translation_chain import translate_sentence
from src.chain.translation_review_chain import translation_review_chain
from src.db.session import get_db
from src.exceptions.app_exception import InvalidRequestException
from src.exceptions.response_code import ResponseCode
from src.llm.deepseek import llm
from src.models import ArticleSentence, LlmSentenceTranslation, UserSentenceTranslation


router = APIRouter(prefix="/translations", tags=["translations"])


class LlmSentenceTranslationRequest(BaseModel):
    sentence_id: int = Field(..., description="原文句子ID")
    target_language: str = Field(..., description="翻译目标语言")


class UserSentenceTranslationReviewRequest(BaseModel):
    sentence_id: int = Field(..., description="原文句子ID")
    target_language: str = Field(..., description="用户翻译目标语言")
    translation_content: str = Field(..., description="用户翻译内容")
    user_id: int = Field(0, description="用户ID，默认 0")


def _success_response(data: dict) -> dict:
    return {
        "code": ResponseCode.SUCCESS,
        "message": "success",
        "data": data,
    }


def _get_model_name() -> str:
    return str(
        getattr(llm, "model_name", None)
        or getattr(llm, "model", None)
        or getattr(llm, "model_id", None)
        or "unknown"
    )


def _get_sentence_or_raise(db: Session, sentence_id: int) -> ArticleSentence:
    sentence = db.get(ArticleSentence, sentence_id)
    if sentence is None:
        raise InvalidRequestException(
            "句子不存在",
            code=ResponseCode.NOT_FOUND_RESOURCE,
        )
    return sentence


def _get_article_sentence_context(
    db: Session,
    sentence: ArticleSentence,
    window_size: int = 5,
) -> list[str]:
    start_index = max(1, sentence.sentence_index - window_size)
    end_index = sentence.sentence_index + window_size

    rows = (
        db.query(ArticleSentence.sentence_content)
        .filter(
            ArticleSentence.article_id == sentence.article_id,
            ArticleSentence.sentence_index >= start_index,
            ArticleSentence.sentence_index <= end_index,
        )
        .order_by(ArticleSentence.sentence_index.asc())
        .all()
    )
    return [row.sentence_content for row in rows]


@router.post("/llm")
def create_llm_sentence_translation(
    request: LlmSentenceTranslationRequest,
    db: Session = Depends(get_db),
) -> dict:
    sentence = _get_sentence_or_raise(db, request.sentence_id)
    sentence_context = _get_article_sentence_context(db, sentence)
    model_name = _get_model_name()

    translation_content = translate_sentence(
        sentences=sentence_context,
        sentence=sentence.sentence_content,
        target_language=request.target_language,
    )

    try:
        translation = (
            db.query(LlmSentenceTranslation)
            .filter(
                LlmSentenceTranslation.sentence_id == sentence.id,
                LlmSentenceTranslation.target_language == request.target_language,
                LlmSentenceTranslation.model_name == model_name,
            )
            .one_or_none()
        )
        if translation is None:
            translation = LlmSentenceTranslation(
                sentence_id=sentence.id,
                source_language=sentence.language_type,
                target_language=request.target_language,
                translation_content=translation_content,
                model_name=model_name,
            )
            db.add(translation)
        else:
            translation.source_language = sentence.language_type
            translation.translation_content = translation_content

        db.commit()
        db.refresh(translation)
    except Exception:
        db.rollback()
        raise

    return _success_response(
        {
            "id": translation.id,
            "sentence_id": translation.sentence_id,
            "source_language": translation.source_language,
            "target_language": translation.target_language,
            "translation_content": translation.translation_content,
            "model_name": translation.model_name,
            "created_time": translation.created_time.isoformat(),
        }
    )


@router.post("/review")
def create_user_sentence_translation_review(
    request: UserSentenceTranslationReviewRequest,
    db: Session = Depends(get_db),
) -> dict:
    sentence = _get_sentence_or_raise(db, request.sentence_id)
    sentence_context = _get_article_sentence_context(db, sentence)

    review_result = translation_review_chain.invoke(
        {
            "sentence_list": sentence_context,
            "sentence_to_translate": sentence.sentence_content,
            "target_language_type": request.target_language,
            "user_translation": request.translation_content,
        }
    )

    try:
        user_translation = UserSentenceTranslation(
            user_id=request.user_id,
            article_id=sentence.article_id,
            sentence_id=sentence.id,
            target_language=request.target_language,
            translation_content=request.translation_content,
            ai_score=Decimal(review_result.score),
            ai_comment=review_result.comment,
        )
        db.add(user_translation)
        db.commit()
        db.refresh(user_translation)
    except Exception:
        db.rollback()
        raise

    return _success_response(
        {
            "id": user_translation.id,
            "user_id": user_translation.user_id,
            "article_id": user_translation.article_id,
            "sentence_id": user_translation.sentence_id,
            "target_language": user_translation.target_language,
            "translation_content": user_translation.translation_content,
            "ai_score": float(user_translation.ai_score),
            "ai_comment": user_translation.ai_comment,
            "created_time": user_translation.created_time.isoformat(),
            "updated_time": user_translation.updated_time.isoformat(),
        }
    )
