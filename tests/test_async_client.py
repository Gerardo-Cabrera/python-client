"""Tests for AsyncPythonClient using pytest and httpx-style mocking."""

from __future__ import annotations

import pytest
from httpx import Request, Response

from python_client.async_client import APIError, AsyncPythonClient
from python_client.models import Post

SUCCESS_CODE = 200
NOT_FOUND_CODE = 404
POST_ERROR = 999


class MockAsyncClient:
    """Mock async client that mimics httpx.AsyncClient.get."""

    def __init__(self, responses: list) -> None:
        """Initialize with a list of httpx.Response-like objects."""
        self._responses = list(responses)
        self.calls: list = []

    async def get(self, url: str, query_params=None, **kwargs):
        """Return the next prepared response and record the call."""
        self.calls.append((url, query_params))
        return self._responses.pop(0)


class MockEnsureClientFactory:
    """Callable factory that returns a MockAsyncClient when awaited."""

    def __init__(self, responses: list) -> None:
        """Store responses to be used when creating MockAsyncClient instances."""
        self._responses = list(responses)

    async def __call__(self) -> MockAsyncClient:
        """Return a fresh MockAsyncClient when awaited (no nested functions)."""
        return MockAsyncClient(self._responses)


@pytest.fixture(name='posts_data')
def _posts_data():
    """Fixture providing a small list of post dicts used by tests."""
    return [
        {'userId': 1, 'id': 1, 'title': 't1', 'body': 'b1'},
        {'userId': 2, 'id': 2, 'title': 't2', 'body': 'b2'},
    ]


@pytest.mark.asyncio
async def test_get_posts(monkeypatch, posts_data):
    """Test get_posts returns a list of Post objects of requested length."""
    responses = [
        Response(
            SUCCESS_CODE,
            request=Request('GET', ''),
            json=list(posts_data),
        ),
    ]
    client = AsyncPythonClient()
    # monkeypatch to use our awaitable factory instance
    monkeypatch.setattr(client, '_ensure_client', MockEnsureClientFactory(responses))
    posts = await client.get_posts(limit=2)
    if len(posts) != 2:
        pytest.fail('Expected two posts')
    if not isinstance(posts[0], Post):
        pytest.fail('First item is not a Post')
    if posts[0].title != 't1':
        pytest.fail('First post title should be t1')


@pytest.mark.asyncio
async def test_get_post(monkeypatch):
    """Test get_post returns correct Post object for given id."""
    post_data = {'userId': 1, 'id': 1, 'title': 't', 'body': 'b'}
    responses = [Response(SUCCESS_CODE, request=Request('GET', ''), json=post_data)]
    client = AsyncPythonClient()
    monkeypatch.setattr(client, '_ensure_client', MockEnsureClientFactory(responses))
    post = await client.get_post(1)
    if post.id != 1:
        pytest.fail('Post id should be 1')
    if post.title != 't':
        pytest.fail('Post title should be t')


@pytest.mark.asyncio
async def test_get_user(monkeypatch):
    """Test get_user returns correct User object for given id."""
    user_data = {'id': 1, 'name': 'Neo'}
    responses = [Response(SUCCESS_CODE, request=Request('GET', ''), json=user_data)]
    client = AsyncPythonClient()
    monkeypatch.setattr(client, '_ensure_client', MockEnsureClientFactory(responses))
    user = await client.get_user(1)
    if user.id != 1:
        pytest.fail('User id should be 1')
    if user.name != 'Neo':
        pytest.fail('User name should be Neo')


@pytest.mark.asyncio
async def test_get_post_error(monkeypatch):
    """Test get_post raises APIError when client returns non-2xx (404)."""
    error_response = [Response(NOT_FOUND_CODE, request=Request('GET', ''), text='Not found')]
    client = AsyncPythonClient()
    monkeypatch.setattr(client, '_ensure_client', MockEnsureClientFactory(error_response))
    with pytest.raises(APIError):
        await client.get_post(POST_ERROR)
