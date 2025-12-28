"""Module for managing issues across different platforms."""

from __future__ import annotations

from gitunify.issue.data import IssueData, IssueDataList
from gitunify.issue.github.github import GitHubIssue
from gitunify.issue.gitlab.gitlab import GitLabIssue

__all__ = ["GitHubIssue", "GitLabIssue", "IssueData", "IssueDataList"]
