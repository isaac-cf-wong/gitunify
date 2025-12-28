"""Module defining the UserData data class for representing user information."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class UserData(BaseModel):
    """Data class representing a user."""

    # Allow extra fields from API
    model_config = ConfigDict(extra="allow")

    login: str | None = Field(default=None, description="Username of the user.")
    """Username of the user."""
    id: int | None = Field(default=None, description="Unique identifier for the user.")
    """Unique identifier for the user."""
    node_id: str | None = Field(default=None, description="Node identifier for the user.")
    """Node identifier for the user."""
    avatar_url: str | None = Field(default=None, description="URL of the user's avatar.")
    """URL of the user's avatar."""
    gravatar_id: str | None = Field(default=None, description="Gravatar ID of the user.")
    """Gravatar ID of the user."""
    url: str | None = Field(default=None, description="API URL of the user.")
    """API URL of the user."""
    html_url: str | None = Field(default=None, description="HTML URL of the user's profile.")
    """HTML URL of the user's profile."""
    followers_url: str | None = Field(default=None, description="URL for the user's followers.")
    """URL for the user's followers."""
    following_url: str | None = Field(default=None, description="URL for the users the user is following.")
    """URL for the users the user is following."""
    gists_url: str | None = Field(default=None, description="URL for the user's gists.")
    """URL for the user's gists."""
    starred_url: str | None = Field(default=None, description="URL for the user's starred repositories.")
    """URL for the user's starred repositories."""
    subscriptions_url: str | None = Field(default=None, description="URL for the user's subscriptions.")
    """URL for the user's subscriptions."""
    organizations_url: str | None = Field(default=None, description="URL for the user's organizations.")
    """URL for the user's organizations."""
    repos_url: str | None = Field(default=None, description="URL for the user's repositories.")
    """URL for the user's repositories."""
    events_url: str | None = Field(default=None, description="URL for the user's events.")
    """URL for the user's events."""
    received_events_url: str | None = Field(default=None, description="URL for the events received by the user.")
    """URL for the events received by the user."""
    type: str | None = Field(default=None, description="Type of the user (e.g., User, Organization).")
    """Type of the user (e.g., User, Organization)."""
    site_admin: bool | None = Field(default=None, description="Whether the user is a site administrator.")
    """Whether the user is a site administrator."""


class UserDataList(BaseModel):
    """Data class representing a list of users."""

    users: list[UserData] | None = Field(default=None, description="List of UserData objects.")
    """List of UserData objects."""

    def __len__(self) -> int:
        """Return the number of users in the list.

        Returns:
            The number of users as an integer.
        """
        if self.users is None:
            return 0
        return len(self.users)

    def __getitem__(self, index: int) -> UserData:
        """Get a user by its index.

        Args:
            index: Index of the user to retrieve.

        Returns:
            The UserData object at the specified index.
        """
        if self.users is None:
            raise IndexError("UserDataList is empty.")
        return self.users[index]
