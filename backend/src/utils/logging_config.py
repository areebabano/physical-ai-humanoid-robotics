"""
Logging and monitoring configuration for the Physical AI & Humanoid Robotics Textbook
"""
import logging
import sys
import os
from datetime import datetime
from typing import Dict, Any
import json
from enum import Enum


class LogLevel(Enum):
    """
    Log level enumeration
    """
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggingConfig:
    """
    Configuration class for logging and monitoring
    """

    def __init__(self):
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.log_format = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.log_file = os.getenv("LOG_FILE", "app.log")
        self.max_log_file_size = int(os.getenv("MAX_LOG_FILE_SIZE", "10485760"))  # 10MB
        self.log_backup_count = int(os.getenv("LOG_BACKUP_COUNT", "5"))

        # Initialize the logging configuration
        self.setup_logging()

    def setup_logging(self):
        """
        Set up the logging configuration
        """
        # Create formatter
        formatter = logging.Formatter(self.log_format)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)

        # Create file handler with rotation
        try:
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                self.log_file,
                maxBytes=self.max_log_file_size,
                backupCount=self.log_backup_count
            )
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(formatter)
        except Exception as e:
            # If file handler creation fails, log to console only
            print(f"Warning: Could not create file handler: {e}")
            file_handler = None

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)

        # Clear existing handlers
        root_logger.handlers.clear()

        # Add handlers
        root_logger.addHandler(console_handler)
        if file_handler:
            root_logger.addHandler(file_handler)

    def get_logger(self, name: str) -> logging.Logger:
        """
        Get a logger with the specified name
        """
        return logging.getLogger(name)

    def log_structured(self, logger: logging.Logger, level: LogLevel, message: str,
                      extra_data: Dict[str, Any] = None, request_id: str = None):
        """
        Log structured data in JSON format
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.value,
            "message": message,
            "service": "textbook-api",
            "version": os.getenv("APP_VERSION", "1.0.0")
        }

        if request_id:
            log_data["request_id"] = request_id

        if extra_data:
            log_data["extra"] = extra_data

        # Log as JSON string
        logger.log(
            getattr(logging, level.value),
            json.dumps(log_data)
        )


class MonitoringConfig:
    """
    Configuration for application monitoring
    """

    def __init__(self):
        self.enable_metrics = os.getenv("ENABLE_METRICS", "true").lower() == "true"
        self.metrics_port = int(os.getenv("METRICS_PORT", "8000"))
        self.enable_tracing = os.getenv("ENABLE_TRACING", "false").lower() == "true"
        self.tracing_endpoint = os.getenv("TRACING_ENDPOINT", "http://localhost:14268/api/traces")
        self.enable_profiling = os.getenv("ENABLE_PROFILING", "false").lower() == "true"

    def get_monitoring_config(self) -> Dict[str, Any]:
        """
        Get monitoring configuration as dictionary
        """
        return {
            "enable_metrics": self.enable_metrics,
            "metrics_port": self.metrics_port,
            "enable_tracing": self.enable_tracing,
            "tracing_endpoint": self.tracing_endpoint,
            "enable_profiling": self.enable_profiling
        }


# Initialize logging configuration
logging_config = LoggingConfig()
monitoring_config = MonitoringConfig()


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance
    """
    return logging_config.get_logger(name)


def log_api_request(
    logger: logging.Logger,
    method: str,
    path: str,
    status_code: int,
    response_time: float,
    user_id: str = None,
    request_id: str = None
):
    """
    Log API request details
    """
    extra_data = {
        "method": method,
        "path": path,
        "status_code": status_code,
        "response_time_ms": round(response_time * 1000, 2)
    }

    if user_id:
        extra_data["user_id"] = user_id

    logging_config.log_structured(
        logger=logger,
        level=LogLevel.INFO,
        message="API request completed",
        extra_data=extra_data,
        request_id=request_id
    )


def log_error(
    logger: logging.Logger,
    error: Exception,
    context: str = "",
    user_id: str = None,
    request_id: str = None
):
    """
    Log error with context
    """
    extra_data = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context
    }

    if user_id:
        extra_data["user_id"] = user_id

    logging_config.log_structured(
        logger=logger,
        level=LogLevel.ERROR,
        message="Error occurred",
        extra_data=extra_data,
        request_id=request_id
    )


def log_performance(
    logger: logging.Logger,
    operation: str,
    duration: float,
    details: Dict[str, Any] = None,
    request_id: str = None
):
    """
    Log performance metrics
    """
    extra_data = {
        "operation": operation,
        "duration_ms": round(duration * 1000, 2)
    }

    if details:
        extra_data.update(details)

    logging_config.log_structured(
        logger=logger,
        level=LogLevel.INFO,
        message="Performance metric",
        extra_data=extra_data,
        request_id=request_id
    )


def log_user_action(
    logger: logging.Logger,
    user_id: str,
    action: str,
    details: Dict[str, Any] = None,
    request_id: str = None
):
    """
    Log user actions for analytics
    """
    extra_data = {
        "user_id": user_id,
        "action": action
    }

    if details:
        extra_data.update(details)

    logging_config.log_structured(
        logger=logger,
        level=LogLevel.INFO,
        message="User action",
        extra_data=extra_data,
        request_id=request_id
    )


# Performance monitoring decorators
def monitor_performance(operation_name: str = None):
    """
    Decorator to monitor function performance
    """
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            start_time = datetime.now()
            logger = get_logger(func.__module__)
            op_name = operation_name or f"{func.__module__}.{func.__name__}"

            try:
                result = await func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                log_performance(logger, op_name, duration)
                return result
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                log_performance(
                    logger, op_name, duration,
                    details={"error": str(e), "status": "failed"}
                )
                raise

        def sync_wrapper(*args, **kwargs):
            start_time = datetime.now()
            logger = get_logger(func.__module__)
            op_name = operation_name or f"{func.__module__}.{func.__name__}"

            try:
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                log_performance(logger, op_name, duration)
                return result
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                log_performance(
                    logger, op_name, duration,
                    details={"error": str(e), "status": "failed"}
                )
                raise

        # Return appropriate wrapper based on function type
        if hasattr(func, '__code__') and 'async' in str(func.__code__.co_flags):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


# Initialize root logger with configured settings
logger = get_logger(__name__)
logger.info("Logging configuration initialized")