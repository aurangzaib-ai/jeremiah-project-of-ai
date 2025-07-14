"""
Logging configuration and utilities.

This module provides standardized logging setup for the underwriting system,
including structured logging, log formatting, and logger management.
"""

import logging
import logging.config
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
    include_timestamp: bool = True
) -> None:
    """
    Set up logging configuration for the underwriting system.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        log_format: Custom log format string
        include_timestamp: Whether to include timestamps in logs
    """
    # Default log format
    if log_format is None:
        if include_timestamp:
            log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        else:
            log_format = "%(name)s - %(levelname)s - %(message)s"
    
    # Configure logging
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": log_format,
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "standard",
                "stream": sys.stdout
            }
        },
        "loggers": {
            "underwriting": {
                "level": level,
                "handlers": ["console"],
                "propagate": False
            },
            "root": {
                "level": level,
                "handlers": ["console"]
            }
        }
    }
    
    # Add file handler if log_file is specified
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logging_config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": level,
            "formatter": "standard",
            "filename": log_file,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
        
        # Add file handler to loggers
        logging_config["loggers"]["underwriting"]["handlers"].append("file")
        logging_config["loggers"]["root"]["handlers"].append("file")
    
    # Apply configuration
    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the specified module.
    
    Args:
        name: Logger name (typically __name__ from calling module)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def log_function_call(func):
    """
    Decorator to log function calls with arguments and return values.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        # Log function entry
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned: {result}")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised {type(e).__name__}: {e}")
            raise
    
    return wrapper


def log_performance(func):
    """
    Decorator to log function execution time.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        start_time = datetime.now()
        try:
            result = func(*args, **kwargs)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"{func.__name__} completed in {duration:.3f} seconds")
            return result
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.error(f"{func.__name__} failed after {duration:.3f} seconds: {e}")
            raise
    
    return wrapper


class StructuredLogger:
    """
    Structured logger for consistent log formatting with additional context.
    """
    
    def __init__(self, name: str):
        """
        Initialize structured logger.
        
        Args:
            name: Logger name
        """
        self.logger = get_logger(name)
        self.context = {}
    
    def set_context(self, **kwargs):
        """
        Set context variables that will be included in all log messages.
        
        Args:
            **kwargs: Context key-value pairs
        """
        self.context.update(kwargs)
    
    def clear_context(self):
        """Clear all context variables."""
        self.context.clear()
    
    def _format_message(self, message: str, **kwargs) -> str:
        """
        Format message with context and additional data.
        
        Args:
            message: Base log message
            **kwargs: Additional data to include
            
        Returns:
            Formatted message string
        """
        all_data = {**self.context, **kwargs}
        
        if all_data:
            data_str = " | ".join(f"{k}={v}" for k, v in all_data.items())
            return f"{message} | {data_str}"
        
        return message
    
    def debug(self, message: str, **kwargs):
        """Log debug message with context."""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message: str, **kwargs):
        """Log info message with context."""
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log warning message with context."""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, **kwargs):
        """Log error message with context."""
        self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message: str, **kwargs):
        """Log critical message with context."""
        self.logger.critical(self._format_message(message, **kwargs))


# Default logging setup
def configure_default_logging():
    """Configure default logging for the underwriting system."""
    log_level = os.getenv("UNDERWRITING_LOG_LEVEL", "INFO")
    log_file = os.getenv("UNDERWRITING_LOG_FILE")
    
    setup_logging(level=log_level, log_file=log_file)


# Auto-configure logging when module is imported
configure_default_logging()

