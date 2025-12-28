"""GitHub Issue API client implementation."""

from __future__ import annotations

import urllib.parse

from gitunify.api.github import GitHubAPI
from gitunify.issue.base import Issue
from gitunify.issue.github.params import GitHubListIssuesParams
from gitunify.issue.params import ListIssuesParams


class GitHubIssue(GitHubAPI, Issue):
    """GitHub Issue API client."""

    _list_issues_params: type[ListIssuesParams] = GitHubListIssuesParams

    def __init__(
        self, token: str, base_url: str | None = None, api_url: str | None = None, headers: dict | None = None
    ) -> None:
        """Initialize the GitHub Issue API client.

        Args:
            token: Authentication token.
            base_url: The base URL of the service.
            api_url: The API URL of the service.
            headers: Additional headers to include in requests.
        """
        super().__init__(token=token, base_url=base_url, api_url=api_url, headers=headers)

    def _build_list_issues_url(self, owner: str, repository: str) -> str:
        """Build the URL for listing issues.

        Args:
            owner: Repository owner.
            repository: Repository name.

        Returns:
            The URL for listing issues.
        """
        return urllib.parse.urljoin(self.api_url, f"/repos/{owner}/{repository}/issues")
