# Logging Implementation Summary

## Overview

A comprehensive logging system has been implemented throughout the FastAPI Calculator application to track all operations, errors, and important events. The system provides multiple log files, color-coded console output, and helper functions for consistent logging across the application.

---

## Key Features Implemented

### 1. **Centralized Logging Configuration** (`app/logging_config.py`)

✅ **Single source of truth** for all logging setup
✅ **Colored console output** with ANSI color codes
✅ **Multiple handlers**:
   - Console handler (with colors)
   - General application log file
   - Error-only log file
   - Operations-specific log file

✅ **Rotating file handlers** to prevent disk space overflow
✅ **Formatter customization** for different output formats
✅ **Helper functions** for common logging tasks

### 2. **Enhanced Operations Module** (`app/operations/__init__.py`)

Each arithmetic function now includes comprehensive logging:

```
✅ DEBUG: When operation is called
✅ INFO: When operation succeeds (with result)
✅ WARNING: When issues occur (e.g., division by zero)
✅ ERROR: When exceptions happen (with full stack trace)
✅ Context: Input parameters and results logged
```

**Functions Enhanced:**
- `add()` - Addition with logging
- `subtract()` - Subtraction with logging
- `multiply()` - Multiplication with logging
- `divide()` - Division with logging (special handling for zero)

### 3. **Enhanced Main Application** (`main.py`)

✅ **Request/Response Middleware**
   - Logs all incoming requests with request ID
   - Tracks response status codes
   - Measures and logs processing time
   - Adds `X-Process-Time` header to responses

✅ **Endpoint Logging**
   - Logs when each endpoint is called
   - Logs endpoint parameters
   - Logs operation results
   - Logs errors with full context

✅ **Validation Logging**
   - Logs validation errors with details
   - Tracks invalid inputs

✅ **Application Lifecycle**
   - Startup event logging
   - Shutdown event logging
   - Application initialization logging

### 4. **Log File Structure**

```
logs/
├── app.log (0-10 MB)              # All application logs
│   ├── app.log.1 (older backups)
│   └── app.log.5 (newest backups)
│
├── error.log (0-10 MB)            # Errors only
│   ├── error.log.1
│   └── error.log.5
│
└── operations.log (0-5 MB)        # Operation logs
    ├── operations.log.1
    └── operations.log.5
```

### 5. **Log Levels**

| Level | Color | Purpose |
|-------|-------|---------|
| DEBUG | 🔵 Cyan | Detailed diagnostic info |
| INFO | 🟢 Green | Confirmation of normal operation |
| WARNING | 🟡 Yellow | Potential issues |
| ERROR | 🔴 Red | Actual problems |
| CRITICAL | 🟣 Magenta | Very serious issues |

---

## Usage Examples

### Example 1: Successful Operation

**Console Output:**
```
2024-12-11 14:30:45,123 - app.operations - INFO - add:50 - Add operation completed successfully: 10 + 5 = 15
2024-12-11 14:30:45,124 - operations - INFO - Operation: add | a=10 | b=5 | result=15 | status=SUCCESS
2024-12-11 14:30:45,125 - main - INFO - log_requests:48 - [Response 123456789] Status=200, Duration=0.004s
```

### Example 2: Division by Zero Error

**Console Output:**
```
2024-12-11 14:30:46,456 - app.operations - WARNING - divide:92 - Division by zero attempted: 10 / 0
2024-12-11 14:30:46,457 - errors - ERROR - Error Type: ValueError | Message: Cannot divide by zero! | Context: a=10 | b=0
2024-12-11 14:30:46,458 - main - ERROR - divide_route:145 - Divide Operation Error: Cannot divide by zero!
```

### Example 3: Validation Error

**Console Output:**
```
2024-12-11 14:30:47,789 - main - WARNING - validation_exception_handler:65 - ValidationError on /add: a: value is not a valid number
2024-12-11 14:30:47,790 - main - INFO - log_requests:48 - [Response 987654321] Status=422, Duration=0.002s
```

---

## Helper Functions

### 1. `setup_logging(log_level: str = "INFO")`

Initialize the logging system at application startup:

```python
from app.logging_config import setup_logging

# At application startup
setup_logging(log_level="INFO")  # or "DEBUG", "WARNING", etc.
```

### 2. `get_logger(name: str) -> logging.Logger`

Get a logger instance for any module:

```python
from app.logging_config import get_logger

logger = get_logger(__name__)
logger.info("Module initialized")
```

### 3. `log_operation(operation: str, a: float, b: float, result: float, status: str)`

Log an arithmetic operation with standardized format:

```python
from app.logging_config import log_operation

log_operation("add", 10, 5, 15, "SUCCESS")
# Output: Operation: add | a=10 | b=5 | result=15 | status=SUCCESS
```

### 4. `log_error_with_context(error_type: str, error_message: str, context: dict)`

Log an error with relevant context information:

```python
from app.logging_config import log_error_with_context

log_error_with_context(
    "ValueError", 
    "Cannot divide by zero",
    {"a": 10, "b": 0}
)
# Output: Error Type: ValueError | Message: Cannot divide by zero | Context: a=10 | b=0
```

---

## Log Format

### Verbose Format (for detailed files)
```
%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s

Example:
2024-12-11 14:30:45,123 - app.operations - INFO - add:50 - Add operation completed successfully: 10 + 5 = 15
```

### Simple Format (for operations.log)
```
%(asctime)s - %(levelname)s - %(message)s

Example:
2024-12-11 14:30:45,123 - INFO - Operation: add | a=10 | b=5 | result=15 | status=SUCCESS
```

---

## Logging Flow

### Request Processing Flow

```
1. Request Arrives
   ↓
2. Middleware logs: [Request ID] METHOD PATH
   ↓
3. Endpoint handler logs: "Endpoint called with params"
   ↓
4. Operation function logs: "Executing operation"
   ↓
5. Operation succeeds: "Operation completed: result"
   ↓
6. Middleware logs: [Response ID] Status=200, Duration=Xms
   ↓
7. All info written to:
   - Console (with colors)
   - app.log (general)
   - operations.log (if operation)
```

### Error Processing Flow

```
1. Error occurs
   ↓
2. Operation logs: "Operation failed: error message"
   ↓
3. Exception handler logs: "Error Type + Context"
   ↓
4. Endpoint handler logs: "Operation Error: message"
   ↓
5. All error info written to:
   - Console (in red)
   - app.log (general)
   - error.log (errors only)
   - Full stack trace included
```

---

## File Rotation Details

### When Do Logs Rotate?

- **app.log**: Rotates when it reaches 10 MB
- **error.log**: Rotates when it reaches 10 MB
- **operations.log**: Rotates when it reaches 5 MB

### How Many Backups?

- Each log maintains 5 backup files
- Example for app.log:
  - `app.log` (current)
  - `app.log.1` (oldest)
  - `app.log.2`
  - `app.log.3`
  - `app.log.4`
  - `app.log.5` (newest backup)

### Automatic Cleanup

Oldest backups are automatically removed when new ones are created.

---

## Configuration Options

### Change Log Level

```python
# Debug mode (verbose)
setup_logging(log_level="DEBUG")

# Production mode (less verbose)
setup_logging(log_level="WARNING")

# Standard mode
setup_logging(log_level="INFO")
```

### Log Level Recommendations

| Environment | Level | Reason |
|-------------|-------|--------|
| Development | DEBUG | Detailed troubleshooting info |
| Testing | INFO | Normal events + errors |
| Staging | INFO | Same as testing |
| Production | WARNING | Only important events |

---

## Performance Considerations

### Request Processing Time

Each request is measured and logged:

```
[Response 12345678] Status=200, Duration=0.004s
```

This helps identify:
- Slow operations
- Performance bottlenecks
- Response time trends

### Log File Performance

- Rotating handlers prevent unbounded log growth
- Separate files reduce I/O contention
- Color coding adds minimal overhead

---

## Documentation Files

### 1. **LOGGING_GUIDE.md**
- Comprehensive logging documentation
- Usage examples
- Best practices
- Troubleshooting tips

### 2. **This Summary**
- Quick reference
- Feature overview
- Common tasks

---

## Integration with Existing Code

### Before
```python
# Old logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### After
```python
# New logging setup
from app.logging_config import setup_logging, get_logger

setup_logging(log_level="INFO")
logger = get_logger(__name__)
```

---

## Monitoring and Debugging

### Check All Logs
```bash
tail -f logs/app.log              # Watch real-time logs
tail -f logs/error.log            # Watch errors
tail -f logs/operations.log       # Watch operations
```

### Search for Specific Operation
```bash
grep "add" logs/operations.log
grep "divide" logs/operations.log
```

### Find Errors
```bash
grep "ERROR" logs/app.log
cat logs/error.log
```

### Performance Analysis
```bash
grep "Duration=" logs/app.log | awk '{print $NF}'  # Extract durations
```

---

## Best Practices Applied

✅ **Centralized configuration** - Single source of truth
✅ **Appropriate log levels** - Correct level for each message
✅ **Contextual information** - Include relevant parameters
✅ **Performance tracking** - Monitor request processing time
✅ **Error stack traces** - Full tracebacks for debugging
✅ **File rotation** - Prevent disk space issues
✅ **Color coding** - Easier console reading
✅ **Separate log files** - Organized logging structure
✅ **Helper functions** - Consistent logging patterns
✅ **Application lifecycle** - Track startup/shutdown

---

## Files Modified/Created

| File | Type | Changes |
|------|------|---------|
| `app/logging_config.py` | NEW | Centralized logging configuration |
| `app/operations/__init__.py` | MODIFIED | Added logging to all functions |
| `main.py` | MODIFIED | Enhanced with middleware and endpoint logging |
| `LOGGING_GUIDE.md` | NEW | Comprehensive logging documentation |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Log Files | 3 types (app, error, operations) |
| Backup Files | 5 per log type |
| Color Levels | 5 (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| Helper Functions | 4 (setup_logging, get_logger, log_operation, log_error_with_context) |
| Max File Size | 10 MB (app/error), 5 MB (operations) |
| Code Enhancements | All 4 operations + main.py + middleware |

---

## Next Steps

1. **Monitor logs during operation**:
   ```bash
   tail -f logs/app.log
   ```

2. **Test error scenarios** and review error logs

3. **Analyze performance** using Duration metrics

4. **Adjust log levels** as needed for production

5. **Implement log aggregation** for production environments

---

## Conclusion

The logging implementation provides comprehensive tracking of all operations and errors throughout the FastAPI Calculator application. With multiple log files, rotating handlers, color-coded output, and helper functions, the system makes it easy to:

- Debug issues
- Monitor application performance
- Audit operations
- Track errors with context
- Understand application behavior

For detailed information, see [LOGGING_GUIDE.md](LOGGING_GUIDE.md).
