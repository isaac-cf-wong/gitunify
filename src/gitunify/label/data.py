"""Data classes for representing label information."""

from __future__ import annotations

from pydantic import BaseModel, Field


class LabelData(BaseModel):
    """Data class representing a label."""

    # Allow extra fields from API
    model_config = {"extra": "allow"}

    id: int | None = Field(default=None, description="Unique identifier for the label.")
    """Unique identifier for the label."""
    node_id: str | None = Field(default=None, description="Node identifier for the label.")
    """Node identifier for the label."""
    url: str | None = Field(default=None, description="URL of the label.")
    """URL of the label."""
    name: str | None = Field(default=None, description="Name of the label.")
    """Name of the label."""
    description: str | None = Field(default=None, description="Description of the label.")
    """Description of the label."""
    color: str | None = Field(default=None, description="Color code of the label.")
    """Color code of the label."""
    default: bool | None = Field(default=None, description="Whether the label is a default label.")
    """Whether the label is a default label."""


class LabelDataList(BaseModel):
    """Data class representing a list of labels."""

    labels: list[LabelData] = Field(default_factory=list, description="List of LabelData objects.")
    """List of LabelData objects."""

    def __len__(self) -> int:
        """Return the number of labels in the list.

        Returns:
            The number of labels as an integer.
        """
        return len(self.labels)

    def __getitem__(self, index: int) -> LabelData:
        """Get a label by its index.

        Args:
            index: Index of the label to retrieve.

        Returns:
            The LabelData object at the specified index.
        """
        return self.labels[index]
