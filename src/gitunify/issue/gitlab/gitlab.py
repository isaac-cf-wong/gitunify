"""GitLab Issue API client implementation."""

from __future__ import annotations

from gitunify.api.gitlab import GitLabAPI
from gitunify.issue.base import Issue
from gitunify.issue.gitlab.params import GitLabListIssuesParams
from gitunify.issue.params import ListIssuesParams


class GitLabIssue(GitLabAPI, Issue):
    """GitLab Issue API client."""

    _list_issues_params: type[ListIssuesParams] = GitLabListIssuesParams

    def __init__(
        self, token: str, base_url: str | None = None, api_url: str | None = None, headers: dict | None = None
    ) -> None:
        """Initialize the GitLab Issue API client.

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
        project_path = f"{owner}/{repository}".replace("/", "%2F")
        return f"{self.api_url}/projects/{project_path}/issues"

    def _transform_list_issues_params(self, **kwargs) -> dict:
        """Transform list issues parameters to GitLab format.

        Args:
            **kwargs: Original list issues parameters.

        Returns:
            Transformed list issues parameters.
        """
        params = kwargs.copy()

        state = params.pop("state", None)
        if state == "open":
            params["state"] = "opened"

        assignee = params.pop("assignee", None)
        if assignee is not None:
            params["assignee_username"] = assignee

        milestone = params.pop("milestone", None)
        if milestone == "*":
            params["milestone"] = "Any"
        elif milestone == "none":
            params["milestone"] = "None"

        sort = params.pop("sort", None)
        if sort is not None:
            if sort == "created":
                params["order_by"] = "created_at"
            elif sort == "updated":
                params["order_by"] = "updated_at"
            else:
                params["order_by"] = sort

        direction = params.pop("direction", None)
        if direction is not None:
            params["sort"] = direction

        not_ = params.pop("not_", None)
        if not_ is not None:
            params["not"] = not_

        return params
