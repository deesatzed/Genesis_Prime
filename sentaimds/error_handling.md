# MCP Hub Error Handling System

This document describes the standardized error handling system implemented in the MCP Hub.

## Overview

The MCP Hub uses a comprehensive error handling system that provides:

- Standardized error responses across all services
- Structured logging for errors and exceptions
- Consistent error codes and categories
- Automatic mapping of HTTP errors to appropriate exception types
- Centralized error handling for FastAPI endpoints

## Error Response Format

All API endpoints return errors in a standardized format:

```json
{
  "code": "ERROR_CODE",
  "message": "Human-readable error message",
  "details": {
    "additional": "error details",
    "specific": "to the error"
  },
  "timestamp": "2025-04-05T10:00:00Z",
  "request_id": "req-123456",
  "category": "error_category",
  "severity": "error"
}
```

## Error Categories

Errors are categorized to help with filtering and handling:

- `validation`: Input validation errors
- `authentication`: Authentication-related errors
- `authorization`: Permission-related errors
- `resource`: Resource not found or unavailable
- `service`: Service-level errors
- `network`: Network-related errors
- `database`: Database-related errors
- `timeout`: Timeout errors
- `dependency`: External dependency errors
- `internal`: Internal server errors
- `unknown`: Unknown errors

## Error Severity Levels

Errors have severity levels to indicate their impact:

- `debug`: Debug-level issues
- `info`: Informational issues
- `warning`: Warning-level issues
- `error`: Error-level issues
- `critical`: Critical issues

## Common Error Codes

The system defines standard error codes for common scenarios:

### Validation Errors (400 range)
- `INVALID_INPUT`: General invalid input
- `MISSING_REQUIRED_FIELD`: Missing required field
- `INVALID_FORMAT`: Invalid data format
- `VALIDATION_FAILED`: Validation failed

### Authentication Errors (401 range)
- `UNAUTHORIZED`: Unauthorized access
- `INVALID_CREDENTIALS`: Invalid credentials
- `TOKEN_EXPIRED`: Token expired

### Authorization Errors (403 range)
- `FORBIDDEN`: Forbidden access
- `INSUFFICIENT_PERMISSIONS`: Insufficient permissions

### Resource Errors (404 range)
- `RESOURCE_NOT_FOUND`: Resource not found
- `SERVER_NOT_FOUND`: Server not found
- `ENDPOINT_NOT_FOUND`: Endpoint not found

### Service Errors (500 range)
- `SERVICE_UNAVAILABLE`: Service unavailable
- `SERVICE_ERROR`: Service error
- `INTERNAL_SERVER_ERROR`: Internal server error

### Network Errors
- `NETWORK_ERROR`: Network error
- `CONNECTION_ERROR`: Connection error
- `TIMEOUT_ERROR`: Timeout error

### Database Errors
- `DATABASE_ERROR`: Database error
- `QUERY_ERROR`: Query error

### Dependency Errors
- `DEPENDENCY_ERROR`: Dependency error
- `EXTERNAL_SERVICE_ERROR`: External service error

### Other Errors
- `UNKNOWN_ERROR`: Unknown error
- `NOT_IMPLEMENTED`: Not implemented

## Using the Error Handling System

### Raising Exceptions

```python
from shared.utils.error_handling import ServiceException, ErrorCode, ErrorCategory, ErrorSeverity

# Raise a service exception
raise ServiceException(
    code=ErrorCode.RESOURCE_NOT_FOUND,
    message="The requested resource was not found",
    details={"resource_id": "123"},
    category=ErrorCategory.RESOURCE,
    severity=ErrorSeverity.ERROR
)
```

### Handling HTTP Errors

```python
from mcp_hub.utils.error_handling import handle_http_error

try:
    response = await client.get(url)
    response.raise_for_status()
except httpx.HTTPStatusError as e:
    # This will automatically map the HTTP status code to the appropriate exception
    exception = handle_http_error(e, "service_name", url)
    raise exception
```

### Handling Network Errors

```python
from mcp_hub.utils.error_handling import handle_network_error

try:
    response = await client.get(url)
except httpx.RequestError as e:
    exception = handle_network_error(e, "service_name", url)
    raise exception
```

### Logging Exceptions

```python
from shared.utils.error_handling import log_exception

try:
    # Some code that might raise an exception
    result = some_function()
except Exception as e:
    log_exception(e, logger, additional_context={"function": "some_function"})
    raise
```

### Creating Error Responses

```python
from mcp_hub.utils.error_handling import create_error_response

# Create an error response from an exception
error_response = create_error_response(exception, request_id="req-123456")
```

## FastAPI Integration

The error handling system is integrated with FastAPI through exception handlers:

```python
from mcp_hub.api.error_handlers import register_exception_handlers

# Register all exception handlers with the FastAPI app
register_exception_handlers(app)
```

This will register handlers for:
- `ServiceException` and its subclasses
- `RequestValidationError` for request validation errors
- `ValidationError` for Pydantic validation errors
- `HTTPException` for FastAPI's built-in HTTP exceptions
- `Exception` for uncaught exceptions

### Custom 404 Handler

A custom 404 handler is implemented to handle non-existent endpoints:

```python
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    """Handle 404 errors for non-existent endpoints."""
    service_exc = ResourceException(
        message=f"Endpoint not found: {request.url.path}",
        code=ErrorCode.RESOURCE_NOT_FOUND,
        details={"path": request.url.path}
    )
    error_response = service_exc.to_response()
    return JSONResponse(
        status_code=404,
        content=error_response.dict()
    )
```

## Best Practices

1. **Use Specific Exception Types**: Use the most specific exception type for the error scenario.
2. **Include Detailed Context**: Always include detailed context in the `details` field.
3. **Use Appropriate Severity**: Set the appropriate severity level for the error.
4. **Log Exceptions**: Always log exceptions with the `log_exception` function.
5. **Handle Exceptions**: Handle exceptions at the appropriate level and convert them to `ServiceException` when needed.
6. **Include Request ID**: Always include a request ID for traceability.
7. **Use Error Codes Consistently**: Use the predefined error codes consistently across the application.

## Testing Error Handling

A comprehensive test suite has been created to verify the error handling system:

### Test Endpoints

The following test endpoints are available for testing different error scenarios:

- `/error/validation` - Tests validation errors (400)
- `/error/resource` - Tests resource not found errors (404)
- `/error/service` - Tests service errors (500)
- `/error/http` - Tests HTTP exceptions (404)
- `/error/uncaught` - Tests uncaught exceptions (500)

### Running Error Tests

Use the provided test scripts to verify error handling:

```bash
# Run the error handling demo server
python run_error_demo.py

# Run comprehensive tests against all error endpoints
python test_all_errors.py

# Test specifically for 404 error handling
python test_404_endpoint.py
```

### Verification Criteria

All error responses should:

1. Return the appropriate HTTP status code
2. Include all required fields in the standardized format
3. Provide meaningful error messages and details
4. Properly categorize the error
5. Set appropriate severity levels
