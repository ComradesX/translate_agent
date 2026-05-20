from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, Index, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.session import Base

if TYPE_CHECKING:
    from src.models.article import Article
    from src.models.article_sentence import ArticleSentence


class UserSentenceTranslation(Base):
    __tablename__ = "user_sentence_translation"
    __table_args__ = (
        Index("idx_user_article", "user_id", "article_id"),
        Index("idx_sentence_id", "sentence_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
        comment="用户ID，如果暂时没有用户系统可为空",
    )
    article_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="文章ID",
    )
    sentence_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="原文句子ID",
    )
    target_language: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="用户翻译目标语言",
    )
    translation_content: Mapped[str] = mapped_column(Text, nullable=False, comment="用户翻译内容")
    ai_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True, comment="AI评分，如 0-100")
    ai_comment: Mapped[str | None] = mapped_column(Text, nullable=True, comment="AI评语")
    created_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    article: Mapped["Article"] = relationship(
        back_populates="user_translations",
        primaryjoin="foreign(UserSentenceTranslation.article_id) == Article.id",
    )
    sentence: Mapped["ArticleSentence"] = relationship(
        back_populates="user_translations",
        primaryjoin="foreign(UserSentenceTranslation.sentence_id) == ArticleSentence.id",
    )
