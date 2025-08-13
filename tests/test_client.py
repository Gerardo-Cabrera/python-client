"""Tests for python_client using pytest and monkeypatch."""
from __future__ import annotations

from typing import Any

import pytest
import requests

from python_client.client import PythonClient
from python_client.exceptions import APIError
from python_client.models import Post

HTTP_OK = 200
HTTP_REDIRECT = 300
HTTP_NOT_FOUND = 404
USER_NOT_FOUND = 9999


class FakePythonClientResponse:
    """Tiny fake response object used to mock requests.Session.get."""

    def __init__(self, status_code: int, payload: Any) -> None:
        """Initialize TestPythonClientResponse."""
        self.status_code = status_code
        self._payload = payload

    def raise_for_status(self) -> None:
        """Raise HTTPError if status is not 2xx."""
        if self.status_code < HTTP_OK or self.status_code >= HTTP_REDIRECT:
            raise requests.HTTPError('Status {0}'.format(self.status_code))

    def json(self) -> Any:
        """Return payload as JSON."""
        return self._payload

    @property
    def text(self) -> str:
        """Return payload as text."""
        return str(self._payload)


def fake_get_post(url, query_params=None, timeout=None, **kwargs):
    """Fake get for a single post."""
    return FakePythonClientResponse(HTTP_OK, {'userId': 1, 'id': 1, 'title': 't', 'body': 'b'})


def fake_get_posts(url, query_params=None, timeout=None, **kwargs):
    """Fake get for multiple posts with limit param."""
    new_query_params = kwargs.get('params', query_params)
    if new_query_params != {'_limit': 2}:
        pytest.fail('The _limit parameter must be 2')
    return FakePythonClientResponse(HTTP_OK, [
        {'userId': 1, 'id': 1, 'title': 't1', 'body': 'b1'},
        {'userId': 2, 'id': 2, 'title': 't2', 'body': 'b2'},
    ])


def fake_get_user_not_found(url, query_params=None, timeout=None, **kwargs):
    """Fake get for user not found (404)."""
    return FakePythonClientResponse(HTTP_NOT_FOUND, {'error': 'not found'})


def test_get_post(monkeypatch) -> None:
    """Test getting a single post returns a Post instance."""
    session = requests.Session()
    monkeypatch.setattr(session, 'get', fake_get_post)
    client = PythonClient(session=session)
    post: Post = client.get_post(1)
    if post.id != 1:
        pytest.fail('The id of the post must be 1')
    if post.user_id != 1:
        pytest.fail('The user_id of the post must be 1')
    if post.title != 't':
        pytest.fail('The title of the post must be "t"')


def test_get_posts_limit(monkeypatch) -> None:
    """Test get_posts passes limit param and returns list of Post."""
    session = requests.Session()
    monkeypatch.setattr(session, 'get', fake_get_posts)
    client = PythonClient(session=session)
    posts = client.get_posts(limit=2)
    if len(posts) != 2:
        pytest.fail('Must return two posts')
    if posts[0].id != 1:
        pytest.fail('The first post must have id 1')


def test_get_user_not_found(monkeypatch) -> None:
    """Test that a non-2xx response raises APIError."""
    session = requests.Session()
    monkeypatch.setattr(session, 'get', fake_get_user_not_found)
    client = PythonClient(session=session)
    with pytest.raises(APIError, match='API responded with 404:'):
        client.get_user(USER_NOT_FOUND)
