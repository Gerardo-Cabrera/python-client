"""Async client for Python using httpx.AsyncClient."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from python_client.exceptions import APIError
from python_client.models import Post, User

BASE_URL = 'https://jsonplaceholder.typicode.com'
DEFAULT_TIMEOUT = 5.0
MIN_SUCCESS_CODE = 200
MAX_SUCCESS_CODE = 299
MAX_BODY_PREVIEW = 200


class AsyncPythonContext:
    """Context manager for httpx.AsyncClient."""

    def __init__(self, timeout: float = DEFAULT_TIMEOUT) -> None:
        """Initialize the context manager."""
        self._timeout = float(timeout)
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> httpx.AsyncClient:
        """Enter async context and create AsyncClient."""
        self._client = httpx.AsyncClient(timeout=self._timeout)
        return self._client

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc: Optional[BaseException],
        tb: Optional[Any],
    ) -> None:
        """Exit async context and close AsyncClient."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None


class AsyncPythonClient:
    """Async client for Python API operations."""

    def __init__(self, timeout: float = DEFAULT_TIMEOUT) -> None:
        """Initialize the async client."""
        self._timeout = float(timeout)
        self._client: Optional[httpx.AsyncClient] = None

    async def get_posts(self, limit: Optional[int] = None) -> List[Post]:
        """Get posts using the async client."""
        query_params = {'_limit': int(limit)} if limit is not None else None
        posts_data = await self._get('/posts', query_params=query_params)
        return [Post.from_dict(post) for post in posts_data]

    async def get_post(self, post_id: int) -> Post:
        """Get a post by id."""
        post_data = await self._get('/posts/{0}'.format(post_id))
        return Post.from_dict(post_data)

    async def get_user(self, user_id: int) -> User:
        """Get a user by id."""
        user_data = await self._get('/users/{0}'.format(user_id))
        return User.from_dict(user_data)

    async def _ensure_client(self) -> httpx.AsyncClient:
        """Ensure that an AsyncClient exists and return it."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout)
        return self._client

    async def _get(self, path: str, query_params: Optional[Dict[str, Any]] = None) -> Any:
        """Perform async GET request and raise APIError on non-success status."""
        client = await self._ensure_client()
        url = BASE_URL + path
        response = await client.get(url, params=query_params)
        status_code = response.status_code
        if status_code < MIN_SUCCESS_CODE or status_code > MAX_SUCCESS_CODE:
            raise APIError(status_code, response.text[:MAX_BODY_PREVIEW])
        return response.json()
