from pathlib import Path
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import SecretStr

from src.config import DeepSeekConfig

# 使用 DeepSeek 官方配置初始化 LLM
deepseekv4flash = ChatOpenAI(
    model=DeepSeekConfig.base_model(),
    api_key=SecretStr(DeepSeekConfig.api_key()),
    base_url=DeepSeekConfig.base_url(),
)

deepseekv4pro = ChatOpenAI(
    model=DeepSeekConfig.base_model_pro(),
    api_key=SecretStr(DeepSeekConfig.api_key()),
    base_url=DeepSeekConfig.base_url(),
)

# 默认使用 Pro 模型
llm = deepseekv4flash


if __name__ == "__main__":
    chain = (
            ChatPromptTemplate.from_template("请解释：{topic}")
            | llm
            | StrOutputParser()
    )
    # 测试链式调用
    result = chain.invoke({"topic": "你的当前模型是什么， 是 deepseek-v4-flash吗 ？"})
    print(result)
