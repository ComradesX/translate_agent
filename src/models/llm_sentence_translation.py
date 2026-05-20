from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, Index, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.session import Base

if TYPE_CHECKING:
    from src.models.article_sentence import ArticleSentence


class LlmSentenceTranslation(Base):
    __tablename__ = "llm_sentence_translation"
    __table_args__ = (
        UniqueConstraint(
            "sentence_id",
            "target_language",
            "model_name",
            name="uk_sentence_target_model",
        ),
        Index("idx_sentence_id", "sentence_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sentence_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="原文句子ID",
    )
    source_language: Mapped[str] = mapped_column(String(20), nullable=False, comment="原文语言")
    target_language: Mapped[str] = mapped_column(String(20), nullable=False, comment="翻译目标语言")
    translation_content: Mapped[str] = mapped_column(Text, nullable=False, comment="LLM翻译内容")
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True, comment="使用的模型")
    created_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    sentence: Mapped["ArticleSentence"] = relationship(
        back_populates="llm_translations",
        primaryjoin="foreign(LlmSentenceTranslation.sentence_id) == ArticleSentence.id",
    )
