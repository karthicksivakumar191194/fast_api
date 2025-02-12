from typing import Any
from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    formatted_errors = {
        error['loc'][-1]: error['msg'] for error in errors
    }

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=formatted_errors
    )


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request"


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Resource not found"


# class PermissionDenied(DetailedHTTPException):
#     STATUS_CODE = status.HTTP_403_FORBIDDEN
#     DETAIL = "Permission denied"
#
#
# class NotAuthenticated(DetailedHTTPException):
#     STATUS_CODE = status.HTTP_401_UNAUTHORIZED
#     DETAIL = "User not authenticated"
#
#     def __init__(self) -> None:
#         super().__init__(headers={"WWW-Authenticate": "Bearer"})