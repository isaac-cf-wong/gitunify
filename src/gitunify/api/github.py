"""GitHub API client implementation."""

from __future__ import annotations

import urllib.parse

from gitunify.api.base import API, SupportPlatforms


class GitHubAPI(API):  # pylint: disable=too-few-public-methods
    """GitHub API client."""

    _platform: SupportPlatforms = "github"
    """Name of the platform."""

    def __init__(
        self, token: str, base_url: str | None = None, api_url: str | None = None, headers: dict | None = None
    ) -> None:
        """Initialize the GitHub API client.

        Args:
            token: Authentication token.
            base_url: The base URL of the GitHub service.
            api_url: The API URL of the GitHub service.
            headers: Additional headers to include in requests.
        """
        default_headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }
        if headers is not None:
            default_headers.update(headers)
        super().__init__(token=token, base_url=base_url, api_url=api_url, headers=default_headers)

    def _set_api_url(self, base_url: str | None, api_url: str | None) -> None:
        """Set the API URL based on the base URL.

        Args:
            base_url: The base URL of the service.
            api_url: The API URL of the service.
        """
        if api_url:
            self.api_url = api_url
        elif base_url is None or urllib.parse.urlparse(base_url).netloc == "github.com":
            self.api_url = "https://api.github.com"
        else:
            self.api_url = urllib.parse.urljoin(base_url, "api/v3")
