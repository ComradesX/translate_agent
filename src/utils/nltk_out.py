"""Sentence splitting helpers.

The main public API is ``split_article_sentences``:

    split_article_sentences("Hello world. Nice to meet you.", "en")
    # ["Hello world.", "Nice to meet you."]
"""

from __future__ import annotations

from pathlib import Path


LANGUAGE_ALIASES = {
    "en": "en",
    "eng": "en",
    "english": "en",
    "de": "de",
    "german": "de",
    "es": "es",
    "spanish": "es",
    "fr": "fr",
    "french": "fr",
    "it": "it",
    "italian": "it",
    "ja": "ja",
    "japanese": "ja",
    "nl": "nl",
    "dutch": "nl",
    "pl": "pl",
    "polish": "pl",
    "ru": "ru",
    "russian": "ru",
}


def split_article_sentences(article: str, language: str = "english") -> list[str]:
    """Split an article string into a list of sentence strings.

    Args:
        article: Full article text.
        language: Language name or alias, for example ``english`` or ``en``.

    Returns:
        A list of non-empty sentence strings.
    """

    if not article:
        return []

    return split_pysbd_sentences(article, normalize_language(language))


def normalize_language(language: str) -> str:
    """Normalize language aliases to names accepted by the splitter."""

    normalized = (language or "english").strip().lower().replace("_", "-")
    return LANGUAGE_ALIASES.get(normalized, normalized)


def split_pysbd_sentences(article: str, language: str) -> list[str]:
    """Split text with pySBD."""

    pysbd = load_pysbd()

    try:
        segmenter = pysbd.Segmenter(language=language, clean=False)
    except Exception as exc:
        raise ValueError(f"Unsupported language for pySBD: {language}") from exc

    sentences = [
        normalize_sentence_text(sentence)
        for sentence in segmenter.segment(article)
        if sentence.strip()
    ]
    return sentences


def normalize_sentence_text(sentence: str) -> str:
    """Collapse internal whitespace so each returned sentence fits on one line."""

    return " ".join(sentence.split())


def load_pysbd():
    """Import pySBD lazily."""

    try:
        import pysbd
    except ImportError as exc:
        raise RuntimeError(
            "pySBD is required for this language. Install dependencies with "
            "`pip install -r requirements.txt`."
        ) from exc

    return pysbd


def split_file(input_file: str | Path, output_file: str | Path, language: str) -> list[str]:
    """Read an article file, split it, write one sentence per line, and return it."""

    input_path = Path(input_file)
    output_path = Path(output_file)

    article = input_path.read_text(encoding="utf-8")
    sentences = split_article_sentences(article, language)
    output_path.write_text("\n".join(sentences), encoding="utf-8")
    return sentences


def main() -> None:
    src_dir = Path(__file__).resolve().parents[1]
    input_file = src_dir / "resource" / "temp" / "epub_text_test.txt"
    output_file = src_dir / "resource" / "temp" / "epub_text_test_sentence.txt"

    sentences = split_file(input_file, output_file, "english")
    print(f"读取文件：{input_file}")
    print(f"生成文件：{output_file}")
    print(f"分句完成，共切分出 {len(sentences)} 个句子。")


if __name__ == "__main__":
    main()
