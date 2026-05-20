import traceback

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.config.app_config import AppConfig
from src.exceptions.app_exception import AuthenticationException, InvalidRequestException
from src.exceptions.response_code import ResponseCode
from src.log.logging_manager import get_logger

logger = get_logger("exceptions.handler")


def _failed_response(code: int, message: str, debug_msg: str | None = None) -> dict[str, str | int]:
    payload: dict[str, str | int] = {
        "code": code,
        "message": message,
    }
    if debug_msg:
        payload["debug_msg"] = debug_msg
    return payload


def _env() -> str:
    raw_env = (AppConfig.app_env() or "dev").lower()
    if raw_env == "prod":
        return "pro"
    return raw_env


def _first_validation_error(exc: RequestValidationError) -> dict:
    errors = exc.errors()
    if not errors:
        return {}
    return errors[0]


def _extract_field_name(error: dict) -> str:
    loc = error.get("loc", ())
    if not isinstance(loc, (list, tuple)) or not loc:
        return ""
    return str(loc[-1])


def _stack_trace_as_string(exc: Exception) -> str:
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))


def _render_validation_error(exc: RequestValidationError) -> dict[str, str | int]:
    app_env = _env()
    error = _first_validation_error(exc)
    error_msg = str(error.get("msg", "参数错误"))
    error_type = str(error.get("type", ""))
    field_name = _extract_field_name(error)
    debug_msg = str(error)

    if error_type == "json_invalid":
        if app_env == "pro":
            return _failed_response(ResponseCode.INVALID_PARAM, "数据格式错误")
        return _failed_response(ResponseCode.INVALID_PARAM, "数据格式错误", error_msg)

    if "missing" in error_type:
        return _failed_response(ResponseCode.INVALID_PARAM, f"{field_name} 参数缺失", debug_msg)

    if "parsing" in error_type or "type" in error_type:
        field_tip = f"{field_name} 参数数据类型错误" if field_name else "参数数据类型错误"
        return _failed_response(ResponseCode.INVALID_PARAM, field_tip, debug_msg)

    if app_env == "pro":
        return _failed_response(ResponseCode.INVALID_PARAM, error_msg)
    return _failed_response(ResponseCode.INVALID_PARAM, error_msg, debug_msg)


def register_exception_handlers(app: FastAPI) -> None:
    async def handle_validation_exception(
            _request: Request,
            exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=200,
            content=_render_validation_error(exc),
        )

    async def handle_http_exception(
            _request: Request,
            exc: StarletteHTTPException,
    ) -> JSONResponse:
        app_env = _env()
        if exc.status_code == 404:
            return JSONResponse(
                status_code=404,
                content=_failed_response(ResponseCode.NOT_FOUND_RESOURCE, f"{app_env}：资源不存在"),
            )
        if exc.status_code == 405:
            return JSONResponse(
                status_code=404,
                content=_failed_response(ResponseCode.NOT_FOUND_RESOURCE, "资源不存在-方法错误"),
            )
        return JSONResponse(
            status_code=404,
            content=_failed_response(ResponseCode.NOT_FOUND_RESOURCE, str(exc.detail)),
        )

    async def handle_invalid_request_exception(
            _request: Request,
            exc: InvalidRequestException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=200,
            content=_failed_response(exc.code, str(exc)),
        )

    async def handle_value_error(
            _request: Request,
            exc: ValueError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=200,
            content=_failed_response(ResponseCode.INVALID_PARAM, str(exc)),
        )

    async def handle_unknown_exception(
            _request: Request,
            exc: Exception,
    ) -> JSONResponse:
        app_env = _env()
        logger.exception("Unhandled exception", exc_info=exc)
        if app_env == "local":
            return JSONResponse(
                status_code=200,
                content=_failed_response(
                    ResponseCode.BUSINESS_ERROR,
                    "系统错误-请立即修复 local",
                    _stack_trace_as_string(exc),
                ),
            )

        if app_env == "dev":
            return JSONResponse(
                status_code=200,
                content=_failed_response(
                    ResponseCode.BUSINESS_ERROR,
                    "系统错误-请立即修复 dev",
                    _stack_trace_as_string(exc),
                ),
            )
        return JSONResponse(
            status_code=200,
            content=_failed_response(ResponseCode.BUSINESS_ERROR, "系统错误-请联系管理员"),
        )

    app.add_exception_handler(RequestValidationError, handle_validation_exception)
    app.add_exception_handler(StarletteHTTPException, handle_http_exception)
    app.add_exception_handler(InvalidRequestException, handle_invalid_request_exception)
    app.add_exception_handler(ValueError, handle_value_error)
    app.add_exception_handler(Exception, handle_unknown_exception)
