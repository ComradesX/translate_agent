import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """基础配置类，从环境变量读取配置"""

    @staticmethod
    def get_env(key: str, default: str | None = None) -> str | None:
        """获取环境变量值"""
        return os.getenv(key, default)
