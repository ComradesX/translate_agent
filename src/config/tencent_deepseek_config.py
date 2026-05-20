from src.config.base import Config


class TencentDeepSeekConfig:
    """腾讯 DeepSeek API 配置"""

    _api_key: str | None = None
    _base_url: str | None = None
    _model_name: str | None = None

    @classmethod
    def load(cls) -> None:
        """从环境变量加载配置"""
        cls._api_key = Config.get_env("TENCENT_KEY_DEEPSEEK")
        cls._base_url = Config.get_env("TENCENT_BASE_URL_DEEPSEEK")
        cls._model_name = Config.get_env("TENCENT_MODEL_NAME_DEEPSEEK")

    @classmethod
    def api_key(cls) -> str:
        """获取 API Key"""
        if cls._api_key is None:
            cls.load()
        if cls._api_key is None:
            raise ValueError("TENCENT_KEY_DEEPSEEK not set in environment")
        return cls._api_key

    @classmethod
    def base_url(cls) -> str:
        """获取 Base URL"""
        if cls._base_url is None:
            cls.load()
        if cls._base_url is None:
            raise ValueError("TENCENT_BASE_URL_DEEPSEEK not set in environment")
        return cls._base_url

    @classmethod
    def model_name(cls) -> str:
        """获取模型名称"""
        if cls._model_name is None:
            cls.load()
        if cls._model_name is None:
            raise ValueError("TENCENT_MODEL_NAME_DEEPSEEK not set in environment")
        return cls._model_name

    @classmethod
    def to_dict(cls) -> dict[str, str]:
        """返回配置字典"""
        return {
            "api_key": cls.api_key(),
            "base_url": cls.base_url(),
            "model_name": cls.model_name(),
        }
