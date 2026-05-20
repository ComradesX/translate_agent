from pathlib import Path
import sys
from typing import Any

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda

from src.llm.deepseek import llm
from src.prompts import translation_review_prompt
from src.response_struct import TranslationReviewResponse

translation_review_parser = PydanticOutputParser(
    pydantic_object=TranslationReviewResponse
)


def _normalize_sentences(sentences: Any) -> list[str]:
    if sentences is None:
        return []
    if isinstance(sentences, str):
        return [sentences]
    return [str(sentence).strip() for sentence in sentences if str(sentence).strip()]


def _prepare_translation_review_inputs(inputs: dict[str, Any]) -> dict[str, str]:
    sentences = _normalize_sentences(
        inputs.get("sentence_list")
        or inputs.get("sentences")
        or inputs.get("sentence_list_context")
    )
    sentence_to_translate = (
        inputs.get("sentence_to_translate")
        or inputs.get("sentence")
        or inputs.get("source_sentence")
        or inputs.get("text")
    )
    target_language_type = (
        inputs.get("target_language_type")
        or inputs.get("target_language")
        or inputs.get("language_type")
    )
    user_translation = inputs.get("user_translation") or inputs.get("translation")

    if not sentence_to_translate:
        raise ValueError("sentence_to_translate is required")
    if not target_language_type:
        raise ValueError("target_language_type is required")
    if not user_translation:
        raise ValueError("user_translation is required")

    sentence_context = "\n".join(
        f"{index}. {sentence}" for index, sentence in enumerate(sentences, start=1)
    )

    return {
        "sentence_list": sentence_context or "无上下文句子列表",
        "sentence_to_translate": str(sentence_to_translate).strip(),
        "target_language_type": str(target_language_type).strip(),
        "user_translation": str(user_translation).strip(),
        "format_instructions": translation_review_parser.get_format_instructions(),
    }


def build_translation_review_chain():
    return (
        RunnableLambda(_prepare_translation_review_inputs)
        | translation_review_prompt
        | llm
        | translation_review_parser
    )


translation_review_chain = build_translation_review_chain()


if __name__ == "__main__":
    result = translation_review_chain.invoke(
        {
            "sentence_list": [
                "I opened the window because the room was too hot.",
                "A cool breeze came in and made everyone feel better.",
            ],
            "sentence_to_translate": "A cool breeze came in and made everyone feel better.",
            "target_language_type": "中文",
            "user_translation": "一阵风进来了，让每个人都感觉好些。",
        }
    )
    print(result.model_dump())
