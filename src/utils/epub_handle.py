from pathlib import Path
import warnings

from ebooklib import ITEM_DOCUMENT, epub
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning


def read_epub_text(epub_file_path: str | Path) -> str:
    """Read plain text from an EPUB file."""
    book = epub.read_epub(str(epub_file_path))
    chapters: list[str] = []

    # 只读取 EPUB 中的 HTML 文档内容，过滤图片、CSS 等资源文件。
    for item in book.get_items():
        if item.get_type() != ITEM_DOCUMENT:
            continue

        html_content = item.get_content().decode("utf-8", errors="ignore")
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
            soup = BeautifulSoup(html_content, "lxml")
        text = " ".join(" ".join(part.split()) for part in soup.stripped_strings)
        if text:
            chapters.append(text)

    return "\n\n".join(chapters)


def extract_text_from_epub(
        epub_file_path: str | Path,
        output_txt_file_path: str | Path | None = None,
) -> str:
    """Extract plain text from an EPUB file and optionally save it as TXT."""
    text = read_epub_text(epub_file_path)

    if output_txt_file_path is not None:
        output_path = Path(output_txt_file_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")

    return text


if __name__ == "__main__":
    src_dir = Path(__file__).resolve().parents[1]
    epub_file = src_dir / "resource" / "HarryPotter.epub"
    output_txt_file = src_dir / "resource" / "temp" / "epub_text_test.txt"

    text = extract_text_from_epub(epub_file, output_txt_file)

    print(f"读取文件：{epub_file}")
    print(f"生成文件：{output_txt_file}")
    print(f"提取字符数：{len(text)}")
    print("前 500 个字符：")
    print(text[:500])
