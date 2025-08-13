

"""Models for Python resources."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Post:
    """Representation of a Post resource from Python."""

    user_id: int
    id: int
    title: str
    body: str

    @classmethod
    def from_dict(cls, post_dict: Dict[str, Any]) -> 'Post':
        """Create a Post instance from a JSON-style dict."""
        return cls(
            user_id=int(post_dict.get('userId', 0)),
            id=int(post_dict.get('id', 0)),
            title=str(post_dict.get('title', '')),
            body=str(post_dict.get('body', '')),
        )


@dataclass(frozen=True)
class User:
    """Representation of a User resource from Python."""

    id: int
    name: str
    username: str
    email: str

    @classmethod
    def from_dict(cls, user_dict: Dict[str, Any]) -> 'User':
        """Create a User instance from a JSON-style dict."""
        return cls(
            id=int(user_dict.get('id', 0)),
            name=str(user_dict.get('name', '')),
            username=str(user_dict.get('username', '')),
            email=str(user_dict.get('email', '')),
        )
