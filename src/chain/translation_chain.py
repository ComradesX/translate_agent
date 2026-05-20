from pathlib import Path
import sys
from typing import Any

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from src.llm.deepseek import llm
from src.prompts import translation_prompt


def _normalize_sentences(sentences: Any) -> list[str]:
    if sentences is None:
        return []
    if isinstance(sentences, str):
        return [sentences]
    return [str(sentence) for sentence in sentences if str(sentence).strip()]


def _prepare_translation_inputs(inputs: dict[str, Any]) -> dict[str, str]:
    sentences = _normalize_sentences(
        inputs.get("sentences")
        or inputs.get("sentence_list")
        or inputs.get("sentence_list_context")
    )
    sentence = inputs.get("sentence") or inputs.get("source_sentence") or inputs.get("text")
    target_language = inputs.get("target_language") or inputs.get("language_type")

    if not sentence:
        raise ValueError("sentence is required")
    if not target_language:
        raise ValueError("target_language is required")

    sentence_context = "\n".join(
        f"{index}. {context_sentence}"
        for index, context_sentence in enumerate(sentences, start=1)
    )

    return {
        "sentence_context": sentence_context or "无上下文句子列表",
        "sentence": str(sentence).strip(),
        "target_language": str(target_language).strip(),
    }


sentence_translation_chain = (
    RunnableLambda(_prepare_translation_inputs)
    | translation_prompt
    | llm
    | StrOutputParser()
    | RunnableLambda(lambda translated_sentence: translated_sentence.strip())
)


def translate_sentence(
    sentences: list[str],
    sentence: str,
    target_language: str,
) -> str:
    return sentence_translation_chain.invoke(
        {
            "sentences": sentences,
            "sentence": sentence,
            "target_language": target_language,
        }
    )


if __name__ == "__main__":
    result = sentence_translation_chain.invoke(
        {
            "sentence_list": [
                "I opened the window because the room was too hot.",
                "A cool breeze came in and made everyone feel better.",
            ],
            "sentence": "A cool breeze came in and made everyone feel better.",
            "target_language": "中文",
        }
    )
    print(result)
