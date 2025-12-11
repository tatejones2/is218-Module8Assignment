# app/logging_config.py

"""
Logging Configuration Module

This module provides a centralized logging configuration for the FastAPI Calculator application.
It sets up logging with appropriate formatters, handlers, and levels for different parts of the application.

Features:
- Console logging with color-coded output
- File logging for persistent records
- Separate loggers for different modules
- Configurable log levels for development and production
- Structured logging format with timestamps and context
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional

# Define log directory
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Log file names with timestamps
LOG_FILE = os.path.join(LOG_DIR, "app.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
OPERATION_LOG_FILE = os.path.join(LOG_DIR, "operations.log")


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds color codes to console output for better readability.
    
    Color codes:
    - DEBUG: Cyan
    - INFO: Green
    - WARNING: Yellow
    - ERROR: Red
    - CRITICAL: Red with bold
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        """Format the log record with color coding."""
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        return super().format(record)


def setup_logging(log_level: str = "INFO") -> None:
    """
    Set up logging configuration for the entire application.
    
    This function configures:
    1. Root logger with specified log level
    2. Console handler with colored output
    3. File handler for general application logs
    4. File handler for error logs
    5. File handler for operation logs
    
    Parameters:
    - log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Example:
    >>> setup_logging("DEBUG")  # Enable debug logging
    >>> setup_logging("INFO")   # Standard info level logging
    """
    
    # Convert string log level to logging constant
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Create formatters
    verbose_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    colored_formatter = ColoredFormatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Remove existing handlers to avoid duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console Handler (with colors)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(colored_formatter)
    root_logger.addHandler(console_handler)
    
    # General File Handler
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=10_000_000,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(verbose_formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Failed to set up file handler: {e}")
    
    # Error File Handler
    try:
        error_handler = logging.handlers.RotatingFileHandler(
            ERROR_LOG_FILE,
            maxBytes=10_000_000,  # 10 MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(verbose_formatter)
        root_logger.addHandler(error_handler)
    except Exception as e:
        print(f"Failed to set up error handler: {e}")
    
    # Operation File Handler
    try:
        operation_handler = logging.handlers.RotatingFileHandler(
            OPERATION_LOG_FILE,
            maxBytes=5_000_000,  # 5 MB
            backupCount=5
        )
        operation_handler.setLevel(logging.INFO)
        operation_handler.setFormatter(simple_formatter)
        root_logger.addHandler(operation_handler)
    except Exception as e:
        print(f"Failed to set up operation handler: {e}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Parameters:
    - name (str): The name of the logger (typically __name__)
    
    Returns:
    - logging.Logger: A configured logger instance
    
    Example:
    >>> logger = get_logger(__name__)
    >>> logger.info("Application started")
    """
    return logging.getLogger(name)


def log_operation(operation: str, a: float, b: float, result: float, status: str = "SUCCESS") -> None:
    """
    Log an arithmetic operation with its parameters and result.
    
    Parameters:
    - operation (str): The operation name (add, subtract, multiply, divide)
    - a (float): The first operand
    - b (float): The second operand
    - result (float): The result of the operation
    - status (str): The status of the operation (SUCCESS, ERROR)
    
    Example:
    >>> log_operation("add", 10, 5, 15, "SUCCESS")
    """
    logger = get_logger("operations")
    message = f"Operation: {operation} | a={a} | b={b} | result={result} | status={status}"
    
    if status == "SUCCESS":
        logger.info(message)
    else:
        logger.warning(message)


def log_error_with_context(error_type: str, error_message: str, context: dict) -> None:
    """
    Log an error with contextual information.
    
    Parameters:
    - error_type (str): Type of error (e.g., ValueError, ZeroDivisionError)
    - error_message (str): The error message
    - context (dict): Additional context information
    
    Example:
    >>> log_error_with_context("ValueError", "Invalid input", {"a": "not_a_number", "b": 5})
    """
    logger = get_logger("errors")
    context_str = " | ".join([f"{k}={v}" for k, v in context.items()])
    logger.error(f"Error Type: {error_type} | Message: {error_message} | Context: {context_str}")
