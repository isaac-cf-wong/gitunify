"""Data classes for representing milestone information."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from gitunify.user.data import UserData


class MilestoneData(BaseModel):
    """Data class representing a milestone."""

    # Allow extra fields from API
    model_config = ConfigDict(extra="allow")

    url: str | None = Field(default=None, description="URL of the milestone.")
    """URL of the milestone."""
    html_url: str | None = Field(default=None, description="HTML URL of the milestone.")
    """HTML URL of the milestone."""
    labels_url: str | None = Field(default=None, description="Labels URL of the milestone.")
    """Labels URL of the milestone."""
    id: int | None = Field(default=None, description="Unique identifier for the milestone.")
    """Unique identifier for the milestone."""
    node_id: str | None = Field(default=None, description="Node identifier for the milestone.")
    """Node identifier for the milestone."""
    number: int | None = Field(default=None, description="Milestone number.")
    """Milestone number."""
    state: str | None = Field(default=None, description="State of the milestone (e.g., open, closed).")
    """State of the milestone (e.g., open, closed)."""
    title: str | None = Field(default=None, description="Title of the milestone.")
    """Title of the milestone."""
    description: str | None = Field(default=None, description="Description of the milestone.")
    """Description of the milestone."""
    creator: UserData | None = Field(default=None, description="User who created the milestone.")
    """User who created the milestone."""
    open_issues: int | None = Field(default=0, description="Number of open issues in the milestone.")
    """Number of open issues in the milestone."""
    closed_issues: int | None = Field(default=0, description="Number of closed issues in the milestone.")
    """Number of closed issues in the milestone."""
    created_at: str | None = Field(default=None, description="Creation timestamp of the milestone.")
    """Creation timestamp of the milestone."""
    updated_at: str | None = Field(default=None, description="Last updated timestamp of the milestone.")
    """Last updated timestamp of the milestone."""
    closed_at: str | None = Field(default=None, description="Closure timestamp of the milestone.")
    """Closure timestamp of the milestone."""
    due_on: str | None = Field(default=None, description="Due date of the milestone.")
    """Due date of the milestone."""
