class ResponseCode:
    """统一接口业务码配置。"""

    # 正常
    SUCCESS = 20000

    # 参数问题（被拦截校验）
    INVALID_PARAM = -1

    # 权限校验问题（appid / secret-key 等）
    FORBIDDEN = 40300

    NOT_FOUND_RESOURCE = 40400

    # 业务错误码区间
    BUSINESS_ERROR_MIN = 50000
    BUSINESS_ERROR_MAX = 59999

    # 通用业务错误
    BUSINESS_ERROR = 50000
