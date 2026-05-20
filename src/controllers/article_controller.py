from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.exceptions.app_exception import InvalidRequestException
from src.exceptions.response_code import ResponseCode
from src.models import Article, ArticleSentence
from src.utils.epub_handle import read_epub_text
from src.utils.nltk_out import split_article_sentences


router = APIRouter(prefix="/articles", tags=["articles"])
root_router = APIRouter(tags=["articles"])

UPLOAD_DIR = Path(__file__).resolve().parents[1] / "resource" / "uploads"


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


def _article_to_dict(article: Article) -> dict:
    filename = article.filename or Path(article.file_path).name
    return {
        "id": article.id,
        "filename": filename,
        "file_path": article.file_path,
        "language_type": article.language_type,
        "upload_time": article.upload_time.isoformat(),
    }


def _validate_article_file(file: UploadFile) -> None:
    filename = file.filename or ""
    if not filename.lower().endswith((".epub", ".txt")):
        raise InvalidRequestException("请上传 epub 或 txt 文件")


def _source_filename(file: UploadFile) -> str:
    return Path(file.filename or "article").name or "article"


def _build_save_path(filename: str) -> Path:
    source_name = Path(filename).name
    suffix = Path(source_name).suffix or ".epub"
    stem = Path(source_name).stem or "article"
    return UPLOAD_DIR / f"{stem}_{uuid4().hex}{suffix}"


async def _save_upload_file(file: UploadFile) -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    save_path = _build_save_path(file.filename or "article.epub")

    content = await file.read()
    if not content:
        raise InvalidRequestException("上传文件不能为空")

    save_path.write_bytes(content)
    return save_path


def _read_article_text(save_path: Path) -> str:
    if save_path.suffix.lower() == ".txt":
        return save_path.read_text(encoding="utf-8").strip()
    return read_epub_text(save_path)


@root_router.post("/upload-epub")
@router.post("/upload-epub")
async def upload_epub_article(
    file: UploadFile = File(...),
    language_type: str = Form("english"),
    db: Session = Depends(get_db),
) -> dict:
    """Upload an EPUB or TXT file, split it into sentences, and save article data."""

    _validate_article_file(file)
    save_path = await _save_upload_file(file)

    article_content = _read_article_text(save_path)
    if not article_content:
        raise InvalidRequestException("文件未读取到有效文本")

    sentences = split_article_sentences(article_content, language_type)
    if not sentences:
        raise InvalidRequestException("文章未切分出有效句子")

    try:
        article = Article(
            filename=_source_filename(file),
            file_path=str(save_path),
            content=article_content,
            language_type=language_type,
        )
        db.add(article)
        db.flush()

        db.add_all(
            ArticleSentence(
                article_id=article.id,
                sentence_content=sentence,
                sentence_index=index,
                language_type=language_type,
            )
            for index, sentence in enumerate(sentences, start=1)
        )
        db.commit()
        db.refresh(article)
    except Exception:
        db.rollback()
        raise

    return _success_response(
        {
            "article_id": article.id,
            "filename": article.filename,
            "file_path": article.file_path,
            "language_type": article.language_type,
            "sentence_count": len(sentences),
            "upload_time": article.upload_time.isoformat(),
        }
    )


@router.get("")
@router.get("/")
async def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    language_type: str | None = Query(None),
    db: Session = Depends(get_db),
) -> dict:
    """Get article list."""

    query = select(Article)
    if language_type:
        query = query.where(Article.language_type == language_type)

    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    articles = db.scalars(
        query.order_by(Article.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return _success_response(
        _page_response(
            [_article_to_dict(article) for article in articles],
            total,
            page,
            page_size,
        )
    )


@router.get("/{article_id}")
async def get_article_detail(
    article_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """Get article detail."""

    article = db.get(Article, article_id)
    if article is None:
        _not_found("文章不存在")

    return _success_response(_article_to_dict(article))
