from langchain_core.prompts import ChatPromptTemplate


translation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是专业翻译助手。请根据句子列表提供的上下文，"
            "把用户指定的句子翻译成目标语言。只输出翻译后的句子，"
            "不要解释，不要添加引号，不要输出原文。",
        ),
        (
            "human",
            "句子列表：\n{sentence_context}\n\n"
            "需要翻译的句子：{sentence}\n"
            "目标翻译语言类型：{target_language}",
        ),
    ]
)
