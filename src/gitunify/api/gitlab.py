"""GitLab API client implementation."""

from __future__ import annotations

import urllib.parse

from gitunify.api.base import API, SupportPlatforms


class GitLabAPI(API):  # pylint: disable=too-few-public-methods
    """GitLab API client."""

    _platform: SupportPlatforms = "gitlab"
    """Name of the platform."""

    def __init__(
        self, token: str, base_url: str | None = None, api_url: str | None = None, headers: dict | None = None
    ) -> None:
        """Initialize the GitLab API client.

        Args:
            token: Authentication token.
            base_url: The base URL of the GitLab service.
            api_url: The API URL of the GitLab service.
            headers: Additional headers to include in requests.
        """
        default_headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
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
        elif base_url is None or urllib.parse.urlparse(base_url).netloc == "gitlab.com":
            self.api_url = "https://gitlab.com/api/v4"
        else:
            self.api_url = urllib.parse.urljoin(base_url, "api/v4")
