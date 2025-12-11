# main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator  # Use @validator for Pydantic 1.x
from fastapi.exceptions import RequestValidationError
from app.operations import add, subtract, multiply, divide  # Ensure correct import path
from app.logging_config import setup_logging, get_logger
import uvicorn
import logging
import time

# Setup logging configuration
setup_logging(log_level="INFO")

# Get logger for this module
logger = get_logger(__name__)

# Log application startup
logger.info("=" * 80)
logger.info("FastAPI Calculator Application Starting")
logger.info("=" * 80)

app = FastAPI(title="Calculator API", description="A simple calculator API with comprehensive logging")

# Setup templates directory
templates = Jinja2Templates(directory="templates")

logger.info("Application initialized successfully")

# Pydantic model for request data
class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator('a', 'b')  # Correct decorator for Pydantic 1.x
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            logger.debug(f"Validation failed: {value} is not a number")
            raise ValueError('Both a and b must be numbers.')
        return value

# Pydantic model for successful response
class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")

# Pydantic model for error response
class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")

# Custom Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: Status={exc.status_code}, Detail={exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extracting error messages
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.warning(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(
        status_code=422,
        content={"error": error_messages},
    )

# Add middleware for request/response logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log incoming requests and outgoing responses."""
    # Log request details
    request_id = id(request)
    logger.info(f"[Request {request_id}] {request.method} {request.url.path}")
    logger.debug(f"[Request {request_id}] Headers: {dict(request.headers)}")
    
    # Measure request processing time
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response details
        logger.info(f"[Response {request_id}] Status={response.status_code}, Duration={process_time:.3f}s")
        
        # Add process time to response headers
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"[Request {request_id}] Error during processing: {str(e)}, Duration={process_time:.3f}s", exc_info=True)
        raise

@app.get("/")
async def read_root(request: Request):
    """
    Serve the index.html template.
    """
    logger.debug("Serving root endpoint (index.html)")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def add_route(operation: OperationRequest):
    """
    Add two numbers.
    """
    logger.info(f"Add endpoint called with a={operation.a}, b={operation.b}")
    try:
        result = add(operation.a, operation.b)
        logger.info(f"Add operation successful: {operation.a} + {operation.b} = {result}")
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Add Operation Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/subtract", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def subtract_route(operation: OperationRequest):
    """
    Subtract two numbers.
    """
    logger.info(f"Subtract endpoint called with a={operation.a}, b={operation.b}")
    try:
        result = subtract(operation.a, operation.b)
        logger.info(f"Subtract operation successful: {operation.a} - {operation.b} = {result}")
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Subtract Operation Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/multiply", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def multiply_route(operation: OperationRequest):
    """
    Multiply two numbers.
    """
    logger.info(f"Multiply endpoint called with a={operation.a}, b={operation.b}")
    try:
        result = multiply(operation.a, operation.b)
        logger.info(f"Multiply operation successful: {operation.a} * {operation.b} = {result}")
        return OperationResponse(result=result)
    except Exception as e:
        logger.error(f"Multiply Operation Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/divide", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def divide_route(operation: OperationRequest):
    """
    Divide two numbers.
    """
    logger.info(f"Divide endpoint called with a={operation.a}, b={operation.b}")
    try:
        result = divide(operation.a, operation.b)
        logger.info(f"Divide operation successful: {operation.a} / {operation.b} = {result}")
        return OperationResponse(result=result)
    except ValueError as e:
        logger.warning(f"Divide Operation ValueError: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Divide Operation Internal Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.on_event("startup")
async def startup_event():
    """Log application startup."""
    logger.info("FastAPI application startup event triggered")
    logger.info(f"Application is running on http://127.0.0.1:8000")

@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown."""
    logger.info("FastAPI application shutdown event triggered")
    logger.info("=" * 80)
    logger.info("FastAPI Calculator Application Shutting Down")
    logger.info("=" * 80)

if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
