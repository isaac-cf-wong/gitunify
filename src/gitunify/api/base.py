"""Base API class for gitunify."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Literal

import requests
from requests import Response
from requests.exceptions import HTTPError, RequestException

logger = logging.getLogger("gitunify")


SupportPlatforms = Literal["github", "gitlab", "gitea", "unknown"]


class API(ABC):  # pylint: disable=too-few-public-methods
    """Base class for API clients."""

    _platform: SupportPlatforms = "unknown"
    """Git service platform name."""

    def __init__(
        self, token: str, base_url: str | None = None, api_url: str | None = None, headers: dict | None = None
    ) -> None:
        """Initialize the API client.

        Args:
            token: Authentication token.
            base_url: The base URL of the service.
            api_url: The API URL of the service.
            headers: Custom headers to include in requests.
        """
        self.token = token
        self.base_url = base_url
        self.api_url = api_url
        self._set_api_url(base_url=base_url, api_url=api_url)
        self.headers = headers

    @property
    def headers(self) -> dict:
        """Get the custom headers.

        Returns:
            A dictionary of headers.
        """
        return self._headers

    @headers.setter
    def headers(self, value: dict | None) -> None:
        """Set custom headers.

        Args:
            value: A dictionary of headers to set.
        """
        if value is None:
            self._headers = {}
        elif isinstance(value, dict):
            self._headers = value
        else:
            raise ValueError("Headers must be a dictionary or None.")

    @abstractmethod
    def _set_api_url(self, base_url: str | None, api_url: str | None) -> None:
        """Set the API URL based on the base URL.

        Args:
            base_url: The base URL of the service.
            api_url: The API URL of the service.
        """

    def _request(self, method: str, url: str, headers: dict, timeout: int = 60, **kwargs) -> Response:
        """Make an HTTP request.

        Args:
            method: HTTP method (GET, POST, etc.).
            url: URL to request.
            headers: HTTP headers.
            timeout: Request timeout in seconds.
            **kwargs: Additional arguments for requests.request.

        Returns:
            Response: The HTTP response object.

        Raises:
            HTTPError: If the HTTP request returned an unsuccessful status code.
            RequestException: If the request fails.
        """
        merged_headers = {**self.headers, **(headers or {})}
        logger.debug("%s %s", method, url)
        try:
            response = requests.request(method=method, url=url, headers=merged_headers, timeout=timeout, **kwargs)
            response.raise_for_status()
            logger.debug("Response: %s", response.status_code)
            return response
        except HTTPError as e:
            logger.error("HTTP %s: %s", e.response.status_code, e.response.text)
            raise
        except RequestException as e:
            logger.error("Request failed: %s", e)
            raise
