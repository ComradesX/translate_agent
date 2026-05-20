from src.config.base import Config


class DeepSeekConfig:
    """DeepSeek API configuration."""

    _MODEL_ALIASES = {
        "DeepSeek-V4-Flash": "deepseek-v4-flash",
        "DeepSeek-V4-Pro": "deepseek-v4-pro",
    }

    _api_key: str | None = None
    _base_url: str | None = None
    _base_model: str | None = None
    _base_model_pro: str | None = None

    @classmethod
    def load(cls) -> None:
        """Load configuration from environment variables."""
        cls._api_key = Config.get_env("DEEPSEEK_API_KEY")
        cls._base_url = Config.get_env("DEEPSEEK_BASE_URL")
        cls._base_model = Config.get_env("DEEPSEEK_BASE_MODEL")
        cls._base_model_pro = Config.get_env("DEEPSEEK_BASE_MODEL_PRO")

    @classmethod
    def api_key(cls) -> str:
        """Get API key."""
        if cls._api_key is None:
            cls.load()
        if cls._api_key is None:
            raise ValueError("DEEPSEEK_API_KEY not set in environment")
        return cls._api_key

    @classmethod
    def base_url(cls) -> str:
        """Get base URL."""
        if cls._base_url is None:
            cls.load()
        if cls._base_url is None:
            raise ValueError("DEEPSEEK_BASE_URL not set in environment")
        return cls._base_url

    @classmethod
    def base_model(cls) -> str:
        """Get base model name."""
        if cls._base_model is None:
            cls.load()
        if cls._base_model is None:
            raise ValueError("DEEPSEEK_BASE_MODEL not set in environment")
        return cls._normalize_model_name(cls._base_model)

    @classmethod
    def base_model_pro(cls) -> str:
        """Get pro model name."""
        if cls._base_model_pro is None:
            cls.load()
        if cls._base_model_pro is None:
            raise ValueError("DEEPSEEK_BASE_MODEL_PRO not set in environment")
        return cls._normalize_model_name(cls._base_model_pro)

    @classmethod
    def to_dict(cls) -> dict[str, str]:
        """Return configuration as a dictionary."""
        return {
            "api_key": cls.api_key(),
            "base_url": cls.base_url(),
            "base_model": cls.base_model(),
            "base_model_pro": cls.base_model_pro(),
        }

    @classmethod
    def _normalize_model_name(cls, model_name: str) -> str:
        """Normalize friendly model aliases to DeepSeek API model ids."""
        return cls._MODEL_ALIASES.get(model_name, model_name)
