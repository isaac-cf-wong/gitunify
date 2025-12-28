"""Data classes for representing issues and lists of issues."""

from __future__ import annotations

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator

from gitunify.api.base import SupportPlatforms
from gitunify.label.data import LabelData, LabelDataList
from gitunify.milestone.data import MilestoneData
from gitunify.pull_request.data import PullRequestData
from gitunify.user.data import UserData, UserDataList


class IssueData(BaseModel):
    """Data class representing an issue."""

    # Allow extra fields from API and allow both field name and alias
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    # Platform tracking
    platform: SupportPlatforms = Field(
        default="unknown",
        description="Source platform.",
    )
    """Source platform (github, gitlab, gitea, etc.)."""

    id: int | None = Field(default=None, description="Unique identifier for the issue.")
    """Unique identifier for the issue."""

    node_id: str | None = Field(default=None, description="Node identifier for the issue.")
    """Node identifier for the issue."""

    repository_url: str | None = Field(default=None, description="URL of the repository containing the issue.")
    """URL of the repository containing the issue."""

    labels_url: str | None = Field(default=None, description="URL for the labels associated with the issue.")
    """URL for the labels associated with the issue."""

    comments_url: str | None = Field(default=None, description="URL for the comments on the issue.")
    """URL for the comments on the issue."""

    events_url: str | None = Field(default=None, description="URL for the events related to the issue.")
    """URL for the events related to the issue."""

    # GitHub: html_url
    # GitLab: web_url
    html_url: str | None = Field(
        default=None, description="HTML URL of the issue.", validation_alias=AliasChoices("html_url", "web_url")
    )
    """HTML URL of the issue."""

    # GitHub: number
    # GitLab: iid
    number: int | None = Field(
        default=None, description="Issue number.", validation_alias=AliasChoices("number", "iid")
    )
    """Issue number."""

    state: str | None = Field(default=None, description="State of the issue (e.g., open, closed).")
    """State of the issue (e.g., open, closed)."""

    title: str | None = Field(default=None, description="Title of the issue.")
    """Title of the issue."""

    # GitHub: body
    # GitLab: description
    body: str | None = Field(
        default=None, description="Body content of the issue.", validation_alias=AliasChoices("body", "description")
    )
    """Body content of the issue."""

    # GitHub: user
    # GitLab: author
    user: UserData | None = Field(
        default=None, description="User who created the issue.", validation_alias=AliasChoices("user", "author")
    )
    """User who created the issue."""

    labels: LabelDataList | None = Field(default=None, description="Labels associated with the issue.")
    """Labels associated with the issue."""

    assignee: UserData | None = Field(default=None, description="Assignee of the issue.")
    """Assignee of the issue."""

    assignees: UserDataList | None = Field(default=None, description="List of assignees of the issue.")
    """List of assignees of the issue."""

    milestone: MilestoneData | None = Field(default=None, description="Milestone associated with the issue.")
    """Milestone associated with the issue."""

    locked: bool | None = Field(default=None, description="Whether the issue is locked.")
    """Whether the issue is locked."""

    active_lock_reason: str | None = Field(default=None, description="Reason for locking the issue, if applicable.")
    """Reason for locking the issue, if applicable."""

    # GitHub: comments
    # GitLab: user_notes_count
    comments: int | None = Field(
        default=None,
        description="Number of comments on the issue.",
        validation_alias=AliasChoices("comments", "user_notes_count"),
    )
    """Number of comments on the issue."""

    pull_request: PullRequestData | None = Field(
        default=None, description="Pull request data if the issue is a pull request."
    )
    """Pull request data if the issue is a pull request."""

    closed_at: str | None = Field(default=None, description="Closure timestamp of the issue.")
    """Closure timestamp of the issue."""

    created_at: str | None = Field(default=None, description="Creation timestamp of the issue.")
    """Creation timestamp of the issue."""

    updated_at: str | None = Field(default=None, description="Last updated timestamp of the issue.")
    """Last updated timestamp of the issue."""

    closed_by: UserData | None = Field(default=None, description="User who closed the issue.")
    """User who closed the issue."""

    author_association: str | None = Field(default=None, description="Author's association with the repository.")
    """Author's association with the repository."""

    state_reason: str | None = Field(default=None, description="Reason for the current state of the issue.")
    """Reason for the current state of the issue."""

    @field_validator("labels", mode="before")
    @classmethod
    def validate_labels(cls, value) -> LabelDataList | None:
        """Convert labels from different API formats to LabelDataList.

        Handles:
        - GitHub: list of label objects [{'id': 1, 'name': 'bug', ...}]
        - GitLab: list of label strings ['bug', 'feature']
        - None or empty list
        """
        if value is None:
            return None

        if isinstance(value, LabelDataList):
            return value

        if not isinstance(value, list):
            return None

        if len(value) == 0:
            return LabelDataList()

        # Convert list items to LabelData objects
        labels = []
        for item in value:
            if isinstance(item, dict):
                # GitHub format: full label object
                labels.append(LabelData(**item))
            elif isinstance(item, str):
                # GitLab format: label name as string
                labels.append(LabelData(name=item))
            elif isinstance(item, LabelData):
                # Already a LabelData object
                labels.append(item)

        return LabelDataList(labels=labels)

    @field_validator("assignees", mode="before")
    @classmethod
    def validate_assignees(cls, value):
        """Convert list of assignees to UserDataList.

        Args:
            value: The value to validate.
        """
        if value is None:
            return None
        if isinstance(value, list):
            return UserDataList(users=value)
        return value

    # Alias

    @property
    def iid(self) -> int | None:
        """Alias for issue number (iid).

        Returns:
            The issue number.
        """
        return self.number

    @property
    def web_url(self) -> str | None:
        """Alias for HTML URL (web_url).

        Returns:
            The HTML URL.
        """
        return self.html_url

    @property
    def description(self) -> str | None:
        """Alias for body (description).

        Returns:
            The body content.
        """
        return self.body

    @property
    def author(self) -> UserData | None:
        """Alias for user (author).

        Returns:
            The user who created the issue.
        """
        return self.user

    @property
    def user_notes_count(self) -> int | None:
        """Alias for comments (user_notes_count).

        Returns:
            The number of comments.
        """
        return self.comments


class IssueDataList(BaseModel):
    """Data class representing a list of issues."""

    issues: list[IssueData] = Field(default_factory=list, description="List of IssueData objects.")
    """List of IssueData objects."""
    page: int | None = Field(default=None, description="Current page number.")
    """Current page number."""
    per_page: int | None = Field(default=None, description="Number of issues per page.")
    """Number of issues per page."""

    def __len__(self) -> int:
        """Return the number of issues in the list.

        Returns:
            int: The number of issues.
        """
        return len(self.issues)

    def __getitem__(self, index: int) -> IssueData:
        """Get an issue by its index.

        Args:
            index: The index of the issue to retrieve.

        Returns:
            IssueData: The issue at the specified index.
        """
        return self.issues[index]
