# Logging Implementation Guide

## Overview

This document describes the comprehensive logging system implemented throughout the FastAPI Calculator application. The logging system tracks all operations, errors, and important events for debugging, monitoring, and auditing purposes.

---

## Architecture

### Logging Components

1. **Logging Configuration Module** (`app/logging_config.py`)
   - Centralized logging setup
   - Multiple handlers for different log types
   - Color-coded console output
   - Rotating file handlers to prevent log overflow

2. **Operations Module** (`app/operations/__init__.py`)
   - Logs each arithmetic operation
   - Tracks input parameters and results
   - Captures and logs errors with context

3. **Main Application** (`main.py`)
   - Logs API requests and responses
   - Tracks endpoint calls
   - Monitors application lifecycle events
   - Measures request processing time

---

## Logging Configuration

### Setup Function

```python
from app.logging_config import setup_logging

# Initialize logging at application startup
setup_logging(log_level="INFO")
```

**Available Log Levels:**
- `DEBUG` - Detailed diagnostic information
- `INFO` - General informational messages
- `WARNING` - Warning messages for potentially problematic situations
- `ERROR` - Error messages for serious problems
- `CRITICAL` - Critical messages for very serious problems

### Handlers

The logging system uses three main file handlers:

1. **General Application Log** (`logs/app.log`)
   - All log messages at INFO level and above
   - Verbose format with function names and line numbers
   - Rotating: 10 MB max size, 5 backup files

2. **Error Log** (`logs/error.log`)
   - Only ERROR and CRITICAL level messages
   - Verbose format for debugging
   - Rotating: 10 MB max size, 5 backup files

3. **Operations Log** (`logs/operations.log`)
   - Operation execution and results
   - Simple format for readability
   - Rotating: 5 MB max size, 5 backup files

4. **Console Output**
   - Real-time log display with color coding
   - Color scheme:
     - 🔵 DEBUG: Cyan
     - 🟢 INFO: Green
     - 🟡 WARNING: Yellow
     - 🔴 ERROR: Red
     - 🟣 CRITICAL: Magenta

---

## Logging in Operations Module

### Basic Operation Logging

Each operation function includes logging at multiple levels:

```python
def add(a: Number, b: Number) -> Number:
    try:
        logger.debug(f"Executing add operation: a={a}, b={b}")
        result = a + b
        logger.info(f"Add operation completed successfully: {a} + {b} = {result}")
        log_operation("add", a, b, result, "SUCCESS")
        return result
    except Exception as e:
        logger.error(f"Add operation failed: {str(e)}", exc_info=True)
        log_error_with_context("Add", str(e), {"a": a, "b": b})
        raise
```

### Log Output Examples

**Successful Operation:**
```
2024-12-11 14:30:45,123 - app.operations - INFO - add:50 - Add operation completed successfully: 10 + 5 = 15
2024-12-11 14:30:45,124 - operations - INFO - Operation: add | a=10 | b=5 | result=15 | status=SUCCESS
```

**Division by Zero Error:**
```
2024-12-11 14:30:46,456 - app.operations - WARNING - divide:92 - Division by zero attempted: 10 / 0
2024-12-11 14:30:46,457 - errors - ERROR - Error Type: ValueError | Message: Cannot divide by zero! | Context: a=10 | b=0
```

---

## Logging in Main Application

### Request/Response Middleware

Logs are automatically recorded for all incoming requests and outgoing responses:

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log incoming requests and outgoing responses."""
    request_id = id(request)
    logger.info(f"[Request {request_id}] {request.method} {request.url.path}")
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(f"[Response {request_id}] Status={response.status_code}, Duration={process_time:.3f}s")
    return response
```

### Example Request Log Output

```
2024-12-11 14:30:50,123 - main - INFO - log_requests:35 - [Request 12345678] POST /add
2024-12-11 14:30:50,124 - main - INFO - add_route:105 - Add endpoint called with a=10, b=5
2024-12-11 14:30:50,125 - app.operations - INFO - add:50 - Add operation completed successfully: 10 + 5 = 15
2024-12-11 14:30:50,126 - main - INFO - add_route:107 - Add operation successful: 10 + 5 = 15
2024-12-11 14:30:50,127 - main - INFO - log_requests:48 - [Response 12345678] Status=200, Duration=0.004s
```

### Endpoint Logging

Each endpoint logs its execution:

```python
@app.post("/add", response_model=OperationResponse)
async def add_route(operation: OperationRequest):
    logger.info(f"Add endpoint called with a={operation.a}, b={operation.b}")
    try:
        result = add(operation.a, operation.b)
        logger.info(f"Add operation successful: {operation.a} + {operation.b} = {result}")
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Add Operation Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
```

### Application Lifecycle Logging

```python
@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application startup event triggered")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI application shutdown event triggered")
```

---

## Helper Functions

### 1. get_logger()

Get a logger instance for a specific module:

```python
from app.logging_config import get_logger

logger = get_logger(__name__)
logger.info("Module started")
```

### 2. log_operation()

Log an arithmetic operation with its parameters and result:

```python
from app.logging_config import log_operation

log_operation("add", 10, 5, 15, "SUCCESS")
log_operation("divide", 10, 0, None, "ERROR")
```

**Log Output:**
```
Operation: add | a=10 | b=5 | result=15 | status=SUCCESS
Operation: divide | a=10 | b=0 | result=None | status=ERROR
```

### 3. log_error_with_context()

Log an error with contextual information:

```python
from app.logging_config import log_error_with_context

log_error_with_context(
    "ValueError",
    "Cannot divide by zero",
    {"a": 10, "b": 0}
)
```

**Log Output:**
```
Error Type: ValueError | Message: Cannot divide by zero | Context: a=10 | b=0
```

---

## Log Levels Guide

### DEBUG
Used for detailed diagnostic information during development.

**Example:**
```python
logger.debug(f"Executing add operation: a={a}, b={b}")
```

**Output:**
```
2024-12-11 14:30:45,123 - app.operations - DEBUG - add:48 - Executing add operation: a=10, b=5
```

### INFO
Used for confirmation that things are working as expected.

**Example:**
```python
logger.info(f"Add operation completed successfully: {a} + {b} = {result}")
```

**Output:**
```
2024-12-11 14:30:45,124 - app.operations - INFO - add:50 - Add operation completed successfully: 10 + 5 = 15
```

### WARNING
Used for warnings about potential issues.

**Example:**
```python
logger.warning("Division by zero attempted")
```

**Output:**
```
2024-12-11 14:30:46,456 - app.operations - WARNING - divide:92 - Division by zero attempted: 10 / 0
```

### ERROR
Used for error conditions that should be investigated.

**Example:**
```python
logger.error(f"Operation failed: {str(e)}", exc_info=True)
```

**Output:**
```
2024-12-11 14:30:50,500 - app.operations - ERROR - add:53 - Operation failed: TypeError
Traceback (most recent call last):
  File "app/operations/__init__.py", line 50, in add
    result = a + b
TypeError: unsupported operand type(s) for +: 'str' and 'int'
```

### CRITICAL
Used for very serious errors that may cause the application to stop.

**Example:**
```python
logger.critical("Database connection failed - application cannot continue")
```

---

## Log File Locations

The application creates a `logs/` directory in the project root with the following structure:

```
logs/
├── app.log              # General application logs
├── app.log.1            # Backup 1 (oldest)
├── app.log.2            # Backup 2
├── app.log.3            # Backup 3
├── app.log.4            # Backup 4
├── app.log.5            # Backup 5 (newest)
├── error.log            # Error-only logs
├── error.log.1-5        # Error backups
├── operations.log       # Operation-specific logs
└── operations.log.1-5   # Operations backups
```

---

## Rotating File Handlers

Log files automatically rotate when they reach their size limits:

- **app.log**: 10 MB max, keeps 5 backup files
- **error.log**: 10 MB max, keeps 5 backup files
- **operations.log**: 5 MB max, keeps 5 backup files

This prevents logs from consuming excessive disk space while maintaining historical records.

---

## Typical Log Flow

Here's a typical request flow and its logging:

### 1. Request Received
```
[Request 140523456456] POST /add
```

### 2. Validation
```
Add endpoint called with a=10, b=5
```

### 3. Operation Execution
```
Executing add operation: a=10, b=5
```

### 4. Operation Result
```
Add operation completed successfully: 10 + 5 = 15
Operation: add | a=10 | b=5 | result=15 | status=SUCCESS
```

### 5. Response Sent
```
[Response 140523456456] Status=200, Duration=0.004s
```

---

## Error Handling Logging

### Validation Errors
```
ValidationError on /add: a: value is not a valid number
```

### Operation Errors
```
ERROR - Divide Operation Error: Cannot divide by zero!
Error Type: ValueError | Message: Cannot divide by zero! | Context: a=10 | b=0
```

### Internal Server Errors
```
ERROR - Divide Operation Internal Error: Unexpected error occurred
ERROR - exc_info=True shows full stack trace
```

---

## Performance Monitoring

Request processing time is logged and included in response headers:

```
[Response 140523456456] Status=200, Duration=0.004s
X-Process-Time: 0.0042
```

This helps identify slow endpoints that may need optimization.

---

## Configuration Options

To change log levels:

```python
from app.logging_config import setup_logging

# Debug mode with detailed logging
setup_logging(log_level="DEBUG")

# Production with minimal logging
setup_logging(log_level="WARNING")
```

---

## Best Practices

1. **Use appropriate log levels:**
   - DEBUG: Detailed diagnostic info
   - INFO: Important events
   - WARNING: Potential issues
   - ERROR: Actual problems

2. **Include context:**
   ```python
   logger.info(f"Operation: {operation}, a={a}, b={b}, result={result}")
   ```

3. **Use exc_info for exceptions:**
   ```python
   logger.error("Operation failed", exc_info=True)
   ```

4. **Monitor log file sizes:**
   - Check `logs/` directory regularly
   - Rotating handlers prevent overflow

5. **Review logs regularly:**
   - Check error.log for issues
   - Check operations.log for performance data

---

## Summary

The logging implementation provides:

✅ Comprehensive tracking of all operations
✅ Detailed error logging with context
✅ Request/response tracking with performance metrics
✅ Rotating file handlers to manage disk space
✅ Color-coded console output for easy reading
✅ Multiple log files for different purposes
✅ Helper functions for consistent logging
✅ Application lifecycle event logging

This enables easy debugging, performance monitoring, auditing, and troubleshooting of the FastAPI Calculator application.
