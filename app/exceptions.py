"""Exception for API endpoints."""
from fastapi import Request
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    """Resource not found error."""

    def __init__(self, message):
        """Init."""
        self.message = message
        self.status_code = 404


async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )
