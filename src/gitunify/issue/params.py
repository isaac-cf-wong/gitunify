"""Parameters for API calls related to issues."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ListIssuesParams(BaseModel):
    """Parameters for listing issues in a repository."""

    model_config = ConfigDict(extra="forbid")
    """Forbid extra fields not defined in the model."""

    state: str | None = Field(
        default=None,
        description="Filter issues by state. Can be either 'open', 'closed', or 'all'.",
    )
    """Filter issues by state. Can be either 'open', 'closed', or 'all'."""

    assignee: str | None = Field(
        default=None,
        description="Filter issues by assignee. Use '*' for issues assigned to any user, 'none' for unassigned issues.",
    )
    """Filter issues by assignee. Use '*' for issues assigned to any user, 'none' for unassigned issues."""

    milestone: str | None = Field(
        default=None,
        description=(
            "Filter issues by milestone. Use '*' for issues with any milestone, 'none' for issues with no milestone."
        ),
    )
    """Filter issues by milestone. Use '*' for issues with any milestone, 'none' for issues with no milestone."""

    labels: list[str] | str | None = Field(
        default=None,
        description="Filter issues by labels. Comma-separated list of label names.",
    )
    """Filter issues by labels. Comma-separated list of label names."""

    sort: str | None = Field(
        default=None,
        description="Sort issues by a specific field. Can be either 'created', 'updated', 'comments'.",
    )
    """Sort issues by a specific field. Can be either 'created', 'updated', 'comments'."""

    direction: str | None = Field(
        default=None,
        description="Direction of the sort. Can be either 'asc' or 'desc'.",
    )
    """Direction of the sort. Can be either 'asc' or 'desc'."""

    since: str | None = Field(
        default=None,
        description=(
            "Only issues updated at or after this time are returned. "
            "This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ."
        ),
    )
    """Only issues updated at or after this time are returned.
    This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ."""

    per_page: int = Field(
        default=30,
        ge=1,
        le=100,
        description="Number of results per page (max 100).",
    )
    """Number of results per page (max 100)."""

    page: int = Field(
        default=1,
        ge=1,
        description="Page number of the results to fetch.",
    )
    """Page number of the results to fetch."""

    @field_validator("state", mode="before")
    @classmethod
    def validate_state(cls, value: str | None) -> str | None:
        """Validate the state field.

        Args:
            value: The state value to validate.

        Returns:
            The validated state value.
        """
        valid_states = {"open", "closed", "all"}
        if value is not None and value not in valid_states:
            raise ValueError(f"Invalid state: {value}. Must be one of {valid_states}.")
        return value

    @field_validator("labels", mode="before")
    @classmethod
    def validate_labels(cls, value: list[str] | str | None) -> str | None:
        """Validate and convert the labels field.

        Args:
            value: The labels value to validate.

        Returns:
            The validated labels value as a comma-separated string or None.
        """
        if value is None:
            return None

        # If already a string, return as-is
        if isinstance(value, str):
            return value if value.strip() else None

        # Convert list to comma-separated string
        if isinstance(value, list):
            if not value:
                return None
            # Filter out empty strings and join
            labels = [label.strip() for label in value if label.strip()]
            if not labels:
                return None
            return ",".join(labels)

        raise ValueError("Labels must be a string or a list of strings.")

    @field_validator("sort", mode="before")
    @classmethod
    def validate_sort(cls, value: str | None) -> str | None:
        """Validate the sort field.

        Args:
            value: The sort value to validate.

        Returns:
            The validated sort value.
        """
        valid_sorts = {"created", "updated", "comments"}
        if value is not None and value not in valid_sorts:
            raise ValueError(f"Invalid sort: {value}. Must be one of {valid_sorts}.")
        return value

    @field_validator("direction", mode="before")
    @classmethod
    def validate_direction(cls, value: str | None) -> str | None:
        """Validate the direction field.

        Args:
            value: The direction value to validate.

        Returns:
            The validated direction value.
        """
        valid_directions = {"asc", "desc"}
        if value is not None and value not in valid_directions:
            raise ValueError(f"Invalid direction: {value}. Must be one of {valid_directions}.")
        return value
