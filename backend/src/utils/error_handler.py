"""
Error handling middleware for the Physical AI & Humanoid Robotics Textbook API
Provides comprehensive error handling and structured error responses
"""
import json
import traceback
import logging
from typing import Callable, Dict, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from backend.src.utils.logging_config import log_error, get_logger

logger = get_logger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Comprehensive error handling middleware for the API
    Handles various types of errors and provides structured responses
    """

    async def dispatch(self, request: Request, call_next: Callable):
        try:
            # Add request ID for tracking
            request_id = request.headers.get("X-Request-ID")
            if not request_id:
                import uuid
                request_id = str(uuid.uuid4())

            # Add request ID to request state for logging
            request.state.request_id = request_id

            # Add to response headers
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            return response

        except StarletteHTTPException as exc:
            # Handle HTTP exceptions from FastAPI
            return await self.handle_http_exception(request, exc, request_id)

        except RequestValidationError as exc:
            # Handle request validation errors
            return await self.handle_validation_error(request, exc, request_id)

        except HTTPException as exc:
            # Handle FastAPI HTTP exceptions
            return await self.handle_http_exception(request, exc, request_id)

        except Exception as exc:
            # Handle all other exceptions
            return await self.handle_general_exception(request, exc, request_id)


    async def handle_http_exception(self, request: Request, exc: StarletteHTTPException, request_id: str):
        """
        Handle HTTP exceptions
        """
        error_detail = {
            "error": {
                "type": "HTTPException",
                "code": exc.status_code,
                "message": exc.detail if hasattr(exc, 'detail') else str(exc),
                "request_id": request_id,
                "path": str(request.url),
                "method": request.method
            }
        }

        # Log the error
        log_error(
            logger=logger,
            error=exc,
            context=f"HTTP Exception {exc.status_code}",
            request_id=request_id
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=error_detail
        )


    async def handle_validation_error(self, request: Request, exc: RequestValidationError, request_id: str):
        """
        Handle request validation errors
        """
        errors = []
        for error in exc.errors():
            errors.append({
                "loc": error["loc"],
                "type": error["type"],
                "msg": error["msg"],
                "input": error.get("input", "N/A")
            })

        error_detail = {
            "error": {
                "type": "ValidationError",
                "code": 422,
                "message": "Validation error in request",
                "details": errors,
                "request_id": request_id,
                "path": str(request.url),
                "method": request.method
            }
        }

        # Log the error
        log_error(
            logger=logger,
            error=exc,
            context="Request Validation Error",
            request_id=request_id
        )

        return JSONResponse(
            status_code=422,
            content=error_detail
        )


    async def handle_general_exception(self, request: Request, exc: Exception, request_id: str):
        """
        Handle general exceptions
        """
        error_detail = {
            "error": {
                "type": "InternalServerError",
                "code": 500,
                "message": "An internal server error occurred",
                "request_id": request_id,
                "path": str(request.url),
                "method": request.method
            }
        }

        # Log the full error with traceback
        log_error(
            logger=logger,
            error=exc,
            context="General Exception",
            request_id=request_id
        )

        # Log the full traceback for debugging
        logger.error(f"Unhandled exception in {request.method} {request.url.path}: {str(exc)}")
        logger.error(f"Traceback: {traceback.format_exc()}")

        return JSONResponse(
            status_code=500,
            content=error_detail
        )


# Custom exception handlers for specific error types
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Custom HTTP exception handler
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "HTTPException",
                "code": exc.status_code,
                "message": exc.detail,
                "path": str(request.url)
            }
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom validation exception handler
    """
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "type": "ValidationError",
                "code": 422,
                "message": "Request validation failed",
                "details": exc.errors(),
                "path": str(request.url)
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    General exception handler for unhandled exceptions
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "InternalServerError",
                "code": 500,
                "message": "An internal server error occurred"
            }
        }
    )


# Error response models
class ErrorResponse:
    """
    Standard error response model
    """

    @staticmethod
    def create_error_response(
        error_type: str,
        error_code: int,
        message: str,
        details: Dict[str, Any] = None,
        request_id: str = None
    ) -> Dict[str, Any]:
        """
        Create a standardized error response
        """
        error_response = {
            "error": {
                "type": error_type,
                "code": error_code,
                "message": message
            }
        }

        if details:
            error_response["error"]["details"] = details

        if request_id:
            error_response["error"]["request_id"] = request_id

        return error_response


# Common error types
class APIError:
    """
    Common API error types and codes
    """

    # 400 Bad Request
    @staticmethod
    def bad_request(message: str, details: Dict[str, Any] = None):
        return JSONResponse(
            status_code=400,
            content=ErrorResponse.create_error_response(
                error_type="BadRequest",
                error_code=400,
                message=message,
                details=details
            )
        )

    # 401 Unauthorized
    @staticmethod
    def unauthorized(message: str = "Authentication required"):
        return JSONResponse(
            status_code=401,
            content=ErrorResponse.create_error_response(
                error_type="Unauthorized",
                error_code=401,
                message=message
            )
        )

    # 403 Forbidden
    @staticmethod
    def forbidden(message: str = "Access forbidden"):
        return JSONResponse(
            status_code=403,
            content=ErrorResponse.create_error_response(
                error_type="Forbidden",
                error_code=403,
                message=message
            )
        )

    # 404 Not Found
    @staticmethod
    def not_found(message: str = "Resource not found"):
        return JSONResponse(
            status_code=404,
            content=ErrorResponse.create_error_response(
                error_type="NotFound",
                error_code=404,
                message=message
            )
        )

    # 422 Validation Error
    @staticmethod
    def validation_error(message: str, details: Dict[str, Any] = None):
        return JSONResponse(
            status_code=422,
            content=ErrorResponse.create_error_response(
                error_type="ValidationError",
                error_code=422,
                message=message,
                details=details
            )
        )

    # 500 Internal Server Error
    @staticmethod
    def internal_error(message: str = "Internal server error"):
        return JSONResponse(
            status_code=500,
            content=ErrorResponse.create_error_response(
                error_type="InternalServerError",
                error_code=500,
                message=message
            )
        )