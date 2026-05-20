import logging
from datetime import datetime, timedelta, timezone
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from pathlib import Path

from src.config.app_config import AppConfig

# 日志格式：时间 级别 来源文件:行号 函数 logger名称 - 消息内容
_LOG_FORMAT = (
    "%(asctime)s %(levelname)-5s %(relativepath)s:%(lineno)d %(funcName)s "
    "%(name)s - %(message)s"
)
# 日期格式：年-月-日 时:分:秒 UTC+8（使用 UTC+8 时间）
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S UTC+8"
# 标记日志系统是否已配置，避免重复初始化
_IS_CONFIGURED = False
_UTC_PLUS_8 = timezone(timedelta(hours=8))
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_LOG_DIR_NAME = "default"


def _utc_plus_8_converter(timestamp: float) -> tuple[int, ...]:
    """
    将时间戳转换为 UTC+8 对应的时间元组，供 logging.Formatter 使用。
    """
    return datetime.fromtimestamp(timestamp, _UTC_PLUS_8).timetuple()


class RelativePathFormatter(logging.Formatter):
    """
    在日志记录中注入项目相对路径字段 `relativepath`。
    """

    def format(self, record: logging.LogRecord) -> str:
        raw_path = getattr(record, "pathname", "") or ""
        try:
            path_obj = Path(raw_path).resolve()
            try:
                relative_path = path_obj.relative_to(_PROJECT_ROOT)
                record.relativepath = relative_path.as_posix()
            except ValueError:
                record.relativepath = path_obj.name or raw_path
        except Exception:
            record.relativepath = raw_path
        return super().format(record)


def _build_formatter() -> logging.Formatter:
    formatter: logging.Formatter = RelativePathFormatter(_LOG_FORMAT, _DATE_FORMAT)
    formatter.converter = _utc_plus_8_converter
    return formatter


def _env() -> str:
    """
    获取当前运行环境标识

    Returns:
        str: 环境标识，生产环境返回 'pro'，其他返回原始值（如 'dev', 'local'）
    """
    raw_env = (AppConfig.app_env() or "dev").lower()
    if raw_env == "prod":
        return "pro"
    return raw_env


def _ensure_log_dirs(project_root: Path) -> None:
    """
    确保所有日志子目录存在

    Args:
        project_root: 项目根目录路径
    """
    logs_root = project_root / "logs"
    (logs_root / _DEFAULT_LOG_DIR_NAME).mkdir(parents=True, exist_ok=True)


def _build_console_handler() -> logging.Handler:
    """
    创建控制台日志处理器

    Returns:
        logging.Handler: 配置好格式的控制台处理器
    """
    handler = logging.StreamHandler()
    handler.setFormatter(_build_formatter())
    return handler


def _build_size_file_handler(file_path: Path, max_mb: int, backup_count: int) -> logging.Handler:
    """
    创建基于文件大小轮转的文件日志处理器

    Args:
        file_path: 日志文件路径
        max_mb: 单个日志文件最大大小（MB）
        backup_count: 保留的备份文件数量

    Returns:
        logging.Handler: 配置好的文件处理器
    """
    handler = RotatingFileHandler(
        filename=file_path,
        maxBytes=max_mb * 1024 * 1024,
        backupCount=backup_count,
        encoding="utf-8",
    )
    handler.setFormatter(_build_formatter())
    return handler


def _build_daily_file_handler(file_path: Path, backup_count: int) -> logging.Handler:
    """
    创建基于时间（每天）轮转的文件日志处理器

    Args:
        file_path: 日志文件路径
        backup_count: 保留的备份文件数量（天数）

    Returns:
        logging.Handler: 配置好的文件处理器
    """
    handler = TimedRotatingFileHandler(
        filename=file_path,
        when="midnight",
        interval=1,
        backupCount=backup_count,
        encoding="utf-8",
    )
    handler.setFormatter(_build_formatter())
    return handler


def _clear_logger_handlers(logger: logging.Logger) -> None:
    """
    清除 logger 的所有处理器并关闭它们

    Args:
        logger: 需要清理的 logger 实例
    """
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        try:
            handler.close()
        except Exception:
            pass


def _build_handlers_by_env(log_level: int, log_dir: Path) -> tuple[int, list[logging.Handler]]:
    """
    按当前运行环境创建日志处理器

    Args:
        log_level: 期望日志级别（主要用于 dev/local 环境）
        log_dir: 日志文件夹路径

    Returns:
        tuple[int, list[logging.Handler]]:
            - logger 实际生效级别
            - 处理器列表
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{log_dir.name}.log"
    file_handler = _build_daily_file_handler(log_file, 30)

    # dev/local: 所有级别输出到控制台 + 文件
    if _env() in {"dev", "local"}:
        console_handler = _build_console_handler()
        file_handler.setLevel(log_level)
        console_handler.setLevel(log_level)
        return log_level, [file_handler, console_handler]

    # 正式环境：只写文件，且最少 INFO 级别
    file_handler.setLevel(logging.INFO)
    return logging.INFO, [file_handler]


def _configure_logger(logger: logging.Logger, log_level: int, log_dir: Path, propagate: bool = False) -> None:
    """
    按统一策略配置单个 logger

    Args:
        logger: 要配置的 logger 实例
        log_level: 期望日志级别
        log_dir: 日志文件夹路径
        propagate: 是否向父 logger 传播
    """
    _clear_logger_handlers(logger)
    logger.disabled = False
    logger.propagate = propagate
    actual_level, handlers = _build_handlers_by_env(log_level, log_dir)
    logger.setLevel(actual_level)
    for handler in handlers:
        logger.addHandler(handler)


def _logger_dir_name(logger_name: str) -> str:
    """
    将 logger 名称转换为安全的日志目录名。
    """
    normalized = (logger_name or "").strip()
    if not normalized:
        return _DEFAULT_LOG_DIR_NAME
    return normalized.replace("/", "_").replace("\\", "_")


def get_logger(name: str = "app") -> logging.Logger:
    """
    获取项目 logger，首次调用时自动完成日志系统初始化。

    Args:
        name: logger 名称

    Returns:
        logging.Logger: 可直接使用的 logger
    """
    setup_logging()

    if not name.strip():
        return logging.getLogger()

    logger = logging.getLogger(name)
    # 动态 logger：按 logger 名称创建同名目录并独立写入
    if not logger.handlers or logger.propagate:
        _configure_logger(
            logger,
            logging.DEBUG,
            _PROJECT_ROOT / "logs" / _logger_dir_name(name),
            propagate=False,
        )
    return logger


def setup_logging() -> None:
    """
    初始化并配置整个项目的日志系统

    配置策略：
    - 开发/本地环境：所有级别日志输出到控制台 + 文件
    - 正式环境：仅写入文件，且仅记录 INFO 及以上级别

    配置的 Logger：

    """
    global _IS_CONFIGURED
    # 防止重复配置
    if _IS_CONFIGURED:
        return

    # 确定项目根目录
    project_root = _PROJECT_ROOT
    _ensure_log_dirs(project_root)

    logs_root = project_root / "logs"

    # 根 logger 作为兜底：未知 logger 统一写入默认文件夹
    root_logger = logging.getLogger()
    _configure_logger(root_logger, logging.DEBUG, logs_root / _DEFAULT_LOG_DIR_NAME, propagate=False)

    # 标记已完成配置
    _IS_CONFIGURED = True
