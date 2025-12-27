"""Unit tests for the API base class."""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest
import requests

from gitunify.api.base import API


class TestAPI:
    """Test cases for the API base class."""

    def test_init_sets_attributes(self):
        """Test that __init__ sets token, base_url, api_url, and headers."""
        from tests.conftest import MockAPI

        api = MockAPI(
            token="test_token",
            base_url="https://example.com",
            api_url="https://api.example.com",
            headers={"Custom": "header"},
        )

        assert api.token == "test_token"
        assert api.base_url == "https://example.com"
        assert api.api_url == "https://api.example.com"
        assert api.headers == {"Custom": "header"}

    def test_init_default_headers(self):
        """Test that __init__ uses default headers when none provided."""
        from tests.conftest import MockAPI

        api = MockAPI(token="test_token")

        assert api.token == "test_token"
        assert api.base_url is None
        assert api.api_url == "https://api.example.com"  # From mock
        assert api.headers == {}

    @patch("gitunify.api.base.requests.request")
    def test_request_success(self, mock_request, mock_response, mock_api):
        """Test successful HTTP request."""
        mock_request.return_value = mock_response

        response = mock_api._request("GET", "https://api.example.com/test", headers={})

        mock_request.assert_called_once_with(method="GET", url="https://api.example.com/test", headers={}, timeout=60)
        assert response == mock_response

    @patch("gitunify.api.base.requests.request")
    def test_request_with_headers_merge(self, mock_request, mock_response, mock_api):
        """Test that headers are merged correctly."""
        mock_request.return_value = mock_response

        # Set headers on the mock_api
        mock_api.headers = {"Authorization": "Bearer token"}

        _response = mock_api._request("GET", "https://api.example.com/test", headers={"Custom": "header"})

        expected_headers = {"Authorization": "Bearer token", "Custom": "header"}
        mock_request.assert_called_once_with(
            method="GET", url="https://api.example.com/test", headers=expected_headers, timeout=60
        )

    @patch("gitunify.api.base.requests.request")
    def test_request_http_error(self, mock_request, caplog, mock_api):
        """Test HTTP error handling."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        http_error = requests.exceptions.HTTPError("404 Not Found")
        http_error.response = mock_response
        mock_request.side_effect = http_error

        with pytest.raises(requests.exceptions.HTTPError):
            mock_api._request("GET", "https://api.example.com/test", headers={})

        # Check that error was logged
        assert "HTTP 404: Not Found" in caplog.text

    @patch("gitunify.api.base.requests.request")
    def test_request_request_exception(self, mock_request, caplog, mock_api):
        """Test general request exception handling."""
        request_error = requests.exceptions.RequestException("Connection failed")
        mock_request.side_effect = request_error

        with pytest.raises(requests.exceptions.RequestException):
            mock_api._request("GET", "https://api.example.com/test", headers={})

        # Check that error was logged
        assert "Request failed: Connection failed" in caplog.text

    @patch("gitunify.api.base.requests.request")
    @patch("gitunify.api.base.logger")
    def test_request_logs_debug_info(self, mock_logger, mock_request, mock_response, mock_api):
        """Test that requests are logged at debug level."""
        mock_request.return_value = mock_response

        mock_api._request("GET", "https://api.example.com/test", headers={})

        mock_logger.debug.assert_any_call("GET https://api.example.com/test")
        mock_logger.debug.assert_any_call("Response: 200")  # Assuming status_code=200

    def test_abstract_method_not_implemented(self):
        """Test that API cannot be instantiated directly due to abstract method."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class API"):
            API(token="test_token")
