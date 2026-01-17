"""Parameters for calling GitHub Issue API."""

from __future__ import annotations

from pydantic import Field

from gitunify.issue.params import ListIssuesParams


class GitHubListIssuesParams(ListIssuesParams):
    """Parameters for listing GitHub issues."""

    type: str | None = Field(
        default=None,
        description="Filter issues by type.",
    )
    """Filter issues by type."""
