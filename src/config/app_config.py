from src.config.base import Config


class AppConfig:
    """应用基础配置"""

    _app_env: str | None = None
    _app_port: str | None = None

    @classmethod
    def load(cls) -> None:
        """从环境变量加载配置"""
        cls._app_env = Config.get_env("APP_ENV", "dev")
        cls._app_port = Config.get_env("APP_PORT", "8890")

    @classmethod
    def app_env(cls) -> str:
        """获取应用环境"""
        if cls._app_env is None:
            cls.load()
        return cls._app_env or "dev"

    @classmethod
    def is_dev(cls) -> bool:
        """是否为开发环境"""
        return cls.app_env() == "dev"

    @classmethod
    def is_prod(cls) -> bool:
        """是否为生产环境"""
        return cls.app_env() == "prod"

    @classmethod
    def app_port(cls) -> int:
        """获取 HTTP 服务端口"""
        if cls._app_port is None:
            cls.load()
        raw_value = (cls._app_port or "8890").strip()
        try:
            port = int(raw_value)
        except ValueError as exc:
            raise ValueError("APP_PORT must be an integer") from exc
        if port <= 0 or port > 65535:
            raise ValueError("APP_PORT must be between 1 and 65535")
        return port
