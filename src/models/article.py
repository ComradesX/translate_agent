from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.session import Base

if TYPE_CHECKING:
    from src.models.article_sentence import ArticleSentence
    from src.models.user_sentence_translation import UserSentenceTranslation


class Article(Base):
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False, comment="文件名")
    file_path: Mapped[str] = mapped_column(String(500), nullable=False, comment="文件地址")
    content: Mapped[str] = mapped_column(
        LONGTEXT,
        nullable=False,
        comment="文章完整内容",
    )
    language_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="语言类型，如 en、zh")
    upload_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        comment="上传时间",
    )

    sentences: Mapped[list["ArticleSentence"]] = relationship(
        back_populates="article",
        primaryjoin="Article.id == foreign(ArticleSentence.article_id)",
        cascade="all, delete-orphan",
    )
    user_translations: Mapped[list["UserSentenceTranslation"]] = relationship(
        back_populates="article",
        primaryjoin="Article.id == foreign(UserSentenceTranslation.article_id)",
        cascade="all, delete-orphan",
    )
