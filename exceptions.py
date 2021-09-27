"""Exception for API endpoints."""


class NotFoundError(Exception):
    """Resource not found error."""

    def __init__(self, message, error_number=None):
        """Init."""
        self.message = message
        self.status_code = 404
        self.error_number = error_number
