
"""Synchronous client for Python API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import requests

from python_client.exceptions import APIError
from python_client.models import Post, User

BASE_URL = 'https://jsonplaceholder.typicode.com'
DEFAULT_TIMEOUT = 5.0
STATUS_OK_MIN = 200
STATUS_OK_MAX = 299


class PythonClient:
    """Minimal Python client implementing a few endpoints.

    - Reusable requests.Session
    - Timeouts
    - Clear exceptions
    - Small and testable methods
    """

    def __init__(
        self,
        session: Optional[requests.Session] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """
        Initialize the client.

        Args:
            session: Optional requests.Session to use (helps testing and reuse).
            timeout: Default timeout for requests in seconds.
        """
        self._session = session or requests.Session()
        self._timeout = float(timeout)

    def get_posts(self, limit: Optional[int] = None) -> List[Post]:
        """Return a list of posts. Use _limit query param to limit results."""
        query_params = {'_limit': int(limit)} if limit is not None else None
        posts_data = self._get('/posts', query_params=query_params)
        return [Post.from_dict(post) for post in posts_data]

    def get_post(self, post_id: int) -> Post:
        """Return a single post by id."""
        post_data = self._get('/posts/{0}'.format(post_id))
        return Post.from_dict(post_data)

    def get_user(self, user_id: int) -> User:
        """Return a user by id."""
        user_data = self._get('/users/{0}'.format(user_id))
        return User.from_dict(user_data)

    def _get(self, path: str, query_params: Optional[Dict[str, Any]] = None) -> Any:
        """Perform GET requests and raise APIError on non-2xx."""
        url = BASE_URL + path
        response = self._session.get(url, params=query_params, timeout=self._timeout)
        status_code = response.status_code
        if status_code < STATUS_OK_MIN or status_code > STATUS_OK_MAX:
            raise APIError(status_code, response.text[:STATUS_OK_MIN])
        return response.json()
