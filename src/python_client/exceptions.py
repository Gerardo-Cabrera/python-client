

"""Custom exceptions for Python client."""

from __future__ import annotations

from typing import Optional


class APIError(RuntimeError):
    """Raised when the remote API returns an error status."""

    def __init__(self, status_code: int, message: Optional[str] = None) -> None:
        """Initialize the APIError with a status code and optional message."""
        error_msg = 'API responded with {0}: {1}'.format(status_code, message or '')
        super().__init__(error_msg)
        self.status_code = status_code
        self.message = message
