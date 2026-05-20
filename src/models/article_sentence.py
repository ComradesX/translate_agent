from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, Index, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.session import Base

if TYPE_CHECKING:
    from src.models.article import Article
    from src.models.llm_sentence_translation import LlmSentenceTranslation
    from src.models.user_sentence_translation import UserSentenceTranslation


class ArticleSentence(Base):
    __tablename__ = "article_sentence"
    __table_args__ = (
        UniqueConstraint("article_id", "sentence_index", name="uk_article_sentence_index"),
        Index("idx_article_id", "article_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    article_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="所属文章ID",
    )
    sentence_content: Mapped[str] = mapped_column(Text, nullable=False, comment="句子内容")
    sentence_index: Mapped[int] = mapped_column(nullable=False, comment="第几句，从1开始")
    language_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="语言类型")
    created_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    article: Mapped["Article"] = relationship(
        back_populates="sentences",
        primaryjoin="foreign(ArticleSentence.article_id) == Article.id",
    )
    llm_translations: Mapped[list["LlmSentenceTranslation"]] = relationship(
        back_populates="sentence",
        primaryjoin="ArticleSentence.id == foreign(LlmSentenceTranslation.sentence_id)",
        cascade="all, delete-orphan",
    )
    user_translations: Mapped[list["UserSentenceTranslation"]] = relationship(
        back_populates="sentence",
        primaryjoin="ArticleSentence.id == foreign(UserSentenceTranslation.sentence_id)",
        cascade="all, delete-orphan",
    )
