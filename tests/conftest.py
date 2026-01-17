"""Shared fixtures for pytest."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from gitunify.api.base import API


class MockAPI(API):
    """Mock implementation of API for testing."""

    def _set_api_url(self, base_url: str | None, api_url: str | None) -> None:
        """Mock implementation of _set_api_url."""
        self.api_url = api_url or "https://api.example.com"


@pytest.fixture
def mock_api():
    """Fixture providing a MockAPI instance."""
    return MockAPI(token="test_token")


@pytest.fixture
def mock_response():
    """Fixture providing a mock HTTP response."""
    response = Mock()
    response.raise_for_status.return_value = None
    response.status_code = 200
    return response


@pytest.fixture
def mock_validation_error_forbidden():
    """Fixture providing a ValidationError for forbidden parameters."""
    error = Mock(spec=ValidationError)
    error.errors.return_value = [
        {
            "loc": ("invalid_param",),
            "type": "extra_forbidden",
            "msg": "Extra inputs are not permitted",
            "input": "some_value",
        }
    ]
    return error


@pytest.fixture
def mock_validation_error_missing():
    """Fixture providing a ValidationError for missing parameters."""
    error = Mock(spec=ValidationError)
    error.errors.return_value = [
        {"loc": ("required_param",), "type": "missing", "msg": "Field required", "input": None}
    ]
    return error


@pytest.fixture
def mock_validation_error_value():
    """Fixture providing a ValidationError for invalid values."""
    error = Mock(spec=ValidationError)
    error.errors.return_value = [
        {"loc": ("state",), "type": "value_error", "msg": "Invalid state value", "input": "invalid"}
    ]
    return error


@pytest.fixture
def sample_issue_data():
    """Fixture providing sample issue data for testing."""
    return {
        "id": 123,
        "title": "Test Issue",
        "state": "open",
        "body": "Test description",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "html_url": "https://github.com/test/repo/issues/123",
        "number": 123,
    }


@pytest.fixture
def github_headers():
    """Fixture providing GitHub API headers."""
    return {"Authorization": "Bearer test_token", "Accept": "application/vnd.github+json"}


@pytest.fixture
def gitlab_headers():
    """Fixture providing GitLab API headers."""
    return {"PRIVATE-TOKEN": "test_token"}
