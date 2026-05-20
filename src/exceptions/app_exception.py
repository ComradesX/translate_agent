from src.exceptions.response_code import ResponseCode


class InvalidRequestException(Exception):
    """业务异常。"""

    def __init__(
        self,
        message: str,
        code: int = ResponseCode.INVALID_PARAM,
        status_code: int = 200,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code


class AuthenticationException(Exception):
    """认证异常。"""

    def __init__(
        self,
        message: str = "unauthorized",
        code: int = ResponseCode.FORBIDDEN,
        status_code: int = 401,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code
