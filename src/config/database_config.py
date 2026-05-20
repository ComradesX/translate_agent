from urllib.parse import quote_plus

from src.config.base import Config


class DatabaseConfig:
    """Database configuration loaded from environment variables."""

    _host: str | None = None
    _port: str | None = None
    _database: str | None = None
    _user: str | None = None
    _password: str | None = None
    _charset: str | None = None
    _pool_size: str | None = None
    _max_overflow: str | None = None
    _pool_timeout: str | None = None
    _pool_recycle: str | None = None

    @classmethod
    def load(cls) -> None:
        cls._host = Config.get_env("MYSQL_HOST", "127.0.0.1")
        cls._port = Config.get_env("MYSQL_PORT", "3306")
        cls._database = Config.get_env("MYSQL_DATABASE", "translate_agent")
        cls._user = Config.get_env("MYSQL_USER", "root")
        cls._password = Config.get_env("MYSQL_PASSWORD", "root_pwd")
        cls._charset = Config.get_env("MYSQL_CHARSET", "utf8mb4")
        cls._pool_size = Config.get_env("MYSQL_POOL_SIZE", "10")
        cls._max_overflow = Config.get_env("MYSQL_MAX_OVERFLOW", "20")
        cls._pool_timeout = Config.get_env("MYSQL_POOL_TIMEOUT", "30")
        cls._pool_recycle = Config.get_env("MYSQL_POOL_RECYCLE", "3600")

    @staticmethod
    def _positive_int(value: str, env_name: str) -> int:
        try:
            parsed = int(value)
        except ValueError as exc:
            raise ValueError(f"{env_name} must be an integer") from exc
        if parsed <= 0:
            raise ValueError(f"{env_name} must be greater than 0")
        return parsed

    @staticmethod
    def _non_negative_int(value: str, env_name: str) -> int:
        try:
            parsed = int(value)
        except ValueError as exc:
            raise ValueError(f"{env_name} must be an integer") from exc
        if parsed < 0:
            raise ValueError(f"{env_name} must be greater than or equal to 0")
        return parsed

    @classmethod
    def host(cls) -> str:
        if cls._host is None:
            cls.load()
        return cls._host or "127.0.0.1"

    @classmethod
    def port(cls) -> int:
        if cls._port is None:
            cls.load()
        raw_value = cls._port or "3306"
        try:
            port = int(raw_value)
        except ValueError as exc:
            raise ValueError("MYSQL_PORT must be an integer") from exc
        if port <= 0 or port > 65535:
            raise ValueError("MYSQL_PORT must be between 1 and 65535")
        return port

    @classmethod
    def database(cls) -> str:
        if cls._database is None:
            cls.load()
        return cls._database or "translate_agent"

    @classmethod
    def user(cls) -> str:
        if cls._user is None:
            cls.load()
        return cls._user or "root"

    @classmethod
    def password(cls) -> str:
        if cls._password is None:
            cls.load()
        return cls._password or "root_pwd"

    @classmethod
    def charset(cls) -> str:
        if cls._charset is None:
            cls.load()
        return cls._charset or "utf8mb4"

    @classmethod
    def pool_size(cls) -> int:
        if cls._pool_size is None:
            cls.load()
        return cls._positive_int(cls._pool_size or "10", "MYSQL_POOL_SIZE")

    @classmethod
    def max_overflow(cls) -> int:
        if cls._max_overflow is None:
            cls.load()
        return cls._non_negative_int(cls._max_overflow or "20", "MYSQL_MAX_OVERFLOW")

    @classmethod
    def pool_timeout(cls) -> int:
        if cls._pool_timeout is None:
            cls.load()
        return cls._positive_int(cls._pool_timeout or "30", "MYSQL_POOL_TIMEOUT")

    @classmethod
    def pool_recycle(cls) -> int:
        if cls._pool_recycle is None:
            cls.load()
        return cls._positive_int(cls._pool_recycle or "3600", "MYSQL_POOL_RECYCLE")

    @classmethod
    def database_url(cls) -> str:
        user = quote_plus(cls.user())
        password = quote_plus(cls.password())
        database = quote_plus(cls.database())
        return (
            f"mysql+pymysql://{user}:{password}@{cls.host()}:{cls.port()}/"
            f"{database}?charset={cls.charset()}"
        )
