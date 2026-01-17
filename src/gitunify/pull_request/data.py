"""Data class for pull request information."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class PullRequestData(BaseModel):
    """Data class representing a pull request."""

    # Allow extra fields from API
    model_config = ConfigDict(extra="allow")

    url: str | None = Field(default=None, description="URL of the pull request.")
    """URL of the pull request."""
    html_url: str | None = Field(default=None, description="HTML URL of the pull request.")
    """HTML URL of the pull request."""
    diff_url: str | None = Field(default=None, description="Diff URL of the pull request.")
    """Diff URL of the pull request."""
    patch_url: str | None = Field(default=None, description="Patch URL of the pull request.")
    """Patch URL of the pull request."""
