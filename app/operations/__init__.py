# app/operations.py

"""
Module: operations.py

This module contains basic arithmetic functions that perform addition, subtraction,
multiplication, and division of two numbers. These functions are foundational for
building more complex applications, such as calculators or financial tools.

Functions:
- add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the sum of a and b.
- subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the difference when b is subtracted from a.
- multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]: Returns the product of a and b.
- divide(a: Union[int, float], b: Union[int, float]) -> float: Returns the quotient when a is divided by b. Raises ValueError if b is zero.

Usage:
These functions can be imported and used in other modules or integrated into APIs
to perform arithmetic operations based on user input.
"""

import logging
from typing import Union  # Import Union for type hinting multiple possible types

# Import logging configuration
from app.logging_config import get_logger, log_operation, log_error_with_context

# Get logger for this module
logger = get_logger(__name__)

# Define a type alias for numbers that can be either int or float
Number = Union[int, float]

def add(a: Number, b: Number) -> Number:
    """
    Add two numbers and return the result.

    Parameters:
    - a (int or float): The first number to add.
    - b (int or float): The second number to add.

    Returns:
    - int or float: The sum of a and b.

    Example:
    >>> add(2, 3)
    5
    >>> add(2.5, 3)
    5.5
    """
    try:
        logger.debug(f"Executing add operation: a={a}, b={b}")
        # Perform addition of a and b
        result = a + b
        logger.info(f"Add operation completed successfully: {a} + {b} = {result}")
        log_operation("add", a, b, result, "SUCCESS")
        return result
    except Exception as e:
        logger.error(f"Add operation failed: {str(e)}", exc_info=True)
        log_error_with_context("Add", str(e), {"a": a, "b": b})
        raise

def subtract(a: Number, b: Number) -> Number:
    """
    Subtract the second number from the first and return the result.

    Parameters:
    - a (int or float): The number from which to subtract.
    - b (int or float): The number to subtract.

    Returns:
    - int or float: The difference between a and b.

    Example:
    >>> subtract(5, 3)
    2
    >>> subtract(5.5, 2)
    3.5
    """
    try:
        logger.debug(f"Executing subtract operation: a={a}, b={b}")
        # Perform subtraction of b from a
        result = a - b
        logger.info(f"Subtract operation completed successfully: {a} - {b} = {result}")
        log_operation("subtract", a, b, result, "SUCCESS")
        return result
    except Exception as e:
        logger.error(f"Subtract operation failed: {str(e)}", exc_info=True)
        log_error_with_context("Subtract", str(e), {"a": a, "b": b})
        raise

def multiply(a: Number, b: Number) -> Number:
    """
    Multiply two numbers and return the product.

    Parameters:
    - a (int or float): The first number to multiply.
    - b (int or float): The second number to multiply.

    Returns:
    - int or float: The product of a and b.

    Example:
    >>> multiply(2, 3)
    6
    >>> multiply(2.5, 4)
    10.0
    """
    try:
        logger.debug(f"Executing multiply operation: a={a}, b={b}")
        # Perform multiplication of a and b
        result = a * b
        logger.info(f"Multiply operation completed successfully: {a} * {b} = {result}")
        log_operation("multiply", a, b, result, "SUCCESS")
        return result
    except Exception as e:
        logger.error(f"Multiply operation failed: {str(e)}", exc_info=True)
        log_error_with_context("Multiply", str(e), {"a": a, "b": b})
        raise

def divide(a: Number, b: Number) -> float:
    """
    Divide the first number by the second and return the quotient.

    Parameters:
    - a (int or float): The dividend.
    - b (int or float): The divisor.

    Returns:
    - float: The quotient of a divided by b.

    Raises:
    - ValueError: If b is zero, as division by zero is undefined.

    Example:
    >>> divide(6, 3)
    2.0
    >>> divide(5.5, 2)
    2.75
    >>> divide(5, 0)
    Traceback (most recent call last):
        ...
    ValueError: Cannot divide by zero!
    """
    try:
        logger.debug(f"Executing divide operation: a={a}, b={b}")
        
        # Check if the divisor is zero to prevent division by zero
        if b == 0:
            error_msg = "Cannot divide by zero!"
            logger.warning(f"Division by zero attempted: {a} / {b}")
            log_error_with_context("ValueError", error_msg, {"a": a, "b": b})
            raise ValueError(error_msg)
        
        # Perform division of a by b and return the result as a float
        result = a / b
        logger.info(f"Divide operation completed successfully: {a} / {b} = {result}")
        log_operation("divide", a, b, result, "SUCCESS")
        return result
    except ValueError as e:
        logger.error(f"Divide operation failed with ValueError: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Divide operation failed with unexpected error: {str(e)}", exc_info=True)
        log_error_with_context("Divide", str(e), {"a": a, "b": b})
        raise
