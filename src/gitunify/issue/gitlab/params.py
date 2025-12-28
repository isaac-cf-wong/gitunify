"""Parameters for calling GitLab Issue API."""

from __future__ import annotations

from pydantic import AliasChoices, Field, field_validator, model_validator

from gitunify.issue.params import ListIssuesParams


class GitLabListIssuesParams(ListIssuesParams):
    """Parameters for listing GitLab issues."""

    assignee: str | None = Field(
        default=None,
        description="Filter issues by assignee. Use '*' for issues assigned to any user, 'none' for unassigned issues.",
        validation_alias=AliasChoices("assignee", "assignee_username"),
    )
    """Filter issues by assignee. Use '*' for issues assigned to any user, 'none' for unassigned issues."""

    sort: str | None = Field(
        default=None,
        description=(
            "Sort issues by a specific field. "
            "Can be either 'created', 'updated', 'priority', 'due_date', "
            "'relative_position', 'label_priority', 'milestone_due', 'popularity', 'weight'."
        ),
    )
    """Sort issues by a specific field.
    Can be either 'created', 'updated', 'priority', 'due_date',
    'relative_position', 'label_priority', 'milestone_due', 'popularity', 'weight'."""

    since: str | None = Field(
        default=None,
        description=(
            "Only issues updated at or after this time are returned. "
            "This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ."
        ),
        validation_alias=AliasChoices("since", "updated_after"),
    )
    """Only issues updated at or after this time are returned.
    This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ."""

    assignee_id: int | None = Field(
        default=None,
        description=(
            "Return issues assigned to the given user id. "
            "Mutually exclusive with assignee. "
            "'None' returns unassigned issues. "
            "'Any' returns issues with an assignee."
        ),
    )
    """Return issues assigned to the given user id.
    Mutually exclusive with assignee.
    'None' returns unassigned issues.
    'Any' returns issues with an assignee."""

    author_id: int | None = Field(
        default=None,
        description=(
            "Return issues created by the given user id. "
            "Mutually exclusive with `author_username`. "
            "Combine with `scope=all` or `scope=assigned_to_me`."
        ),
    )
    """Return issues created by the given user id.
    Mutually exclusive with `author_username`.
    Combine with `scope=all` or `scope=assigned_to_me`."""

    author_username: str | None = Field(
        default=None,
        description=(
            "Return issues created by the given username. "
            "Similar to `author_id` and mutually exclusive with `author_id`."
        ),
    )
    """Return issues created by the given username.
    Similar to `author_id` and mutually exclusive with `author_id`."""

    confidential: bool | None = Field(default=None, description="Filter confidential or public issues.")
    """Filter confidential or public issues."""

    created_before: str | None = Field(
        default=None,
        description=(
            "Return issues created on or before the given time. "
            "Expected in ISO 8601 format (`2019-03-15T08:00:00Z`)."
        ),
    )
    """Return issues created on or before the given time.
    Expected in ISO 8601 format (`2019-03-15T08:00:00Z`)."""

    due_date: str | None = Field(
        default=None,
        description=(
            "Return issues that have no due date, are overdue, "
            "or whose due date is this week, this month, "
            "or between two weeks ago and next month. "
            "Accepts: `0` (no due date), `any`, `today`, `tomorrow`, "
            "`overdue`, `week`, `month`, `next_month_and_previous_two_weeks`."
        ),
    )
    """Return issues that have no due date, are overdue,
    or whose due date is this week, this month,
    or between two weeks ago and next month.
    Accepts: `0` (no due date), `any`, `today`, `tomorrow`,
    `overdue`, `week`, `month`, `next_month_and_previous_two_weeks`."""

    epic_id: int | None = Field(
        default=None,
        description=(
            "Return issues associated with the given epic ID. "
            "`None` returns issues that are not associated with an epic. "
            "`Any` returns issues that are associated with an epic. "
            "Premium and Ultimate only."
        ),
    )
    """Return issues associated with the given epic ID.
    `None` returns issues that are not associated with an epic.
    `Any` returns issues that are associated with an epic.
    Premium and Ultimate only."""

    iids: list[int] | None = Field(default=None, description="Return only the issues having the given iid.")
    """Return only the issues having the given iid."""

    issue_type: str | None = Field(
        default=None, description="Filter to a given type of issue. One of `issue`, `incident`, `test_case` or `task`."
    )
    """Filter to a given type of issue. One of `issue`, `incident`, `test_case` or `task`."""

    iteration_id: int | None = Field(
        default=None,
        description=(
            "Return issues assigned to the given iteration ID. "
            "None returns issues that do not belong to an iteration. "
            "Any returns issues that belong to an iteration. "
            "Mutually exclusive with `iteration_title`. "
            "Premium and Ultimate only."
        ),
    )
    """Return issues assigned to the given iteration ID.
    None returns issues that do not belong to an iteration.
    Any returns issues that belong to an iteration.
    Mutually exclusive with `iteration_title`.
    Premium and Ultimate only."""

    iteration_title: str | None = Field(
        default=None,
        description=(
            "Return issues assigned to the iteration with the given title. "
            "Similar to `iteration_id` and mutually exclusive with `iteration_id`. "
            "Premium and Ultimate only."
        ),
    )
    """Return issues assigned to the iteration with the given title.
    Similar to `iteration_id` and mutually exclusive with `iteration_id`.
    Premium and Ultimate only."""

    my_reaction_emoji: str | None = Field(
        default=None,
        description=(
            "Return issues reacted by the authenticated user by the given `emoji`. "
            "`None` returns issues not given a reaction. "
            "`Any` returns issues given at least one reaction."
        ),
    )
    """Return issues reacted by the authenticated user by the given `emoji`.
    `None` returns issues not given a reaction.
    `Any` returns issues given at least one reaction."""

    not_: str | None = Field(
        default=None,
        description=(
            "Return issues that do not match the parameters supplied. "
            "Accepts: `labels`, `milestone`, `author_id`, `author_username`, "
            "`assignee_id`, `assignee_username`, `my_reaction_emoji`, `search`, `in`."
        ),
        alias="not",
        validation_alias="not",
    )
    """Return issues that do not match the parameters supplied.
    Accepts: `labels`, `milestone`, `author_id`, `author_username`,
    `assignee_id`, `assignee_username`, `my_reaction_emoji`, `search`, `in`."""

    scope: str | None = Field(
        default=None,
        description="Return issues for the given scope: `created_by_me`, `assigned_to_me` or `all`. Defaults to `all`.",
    )
    """Return issues for the given scope: `created_by_me`, `assigned_to_me` or `all`. Defaults to `all`."""

    search: str | None = Field(
        default=None, description="Search project issues against their `title` and `description`."
    )
    """Search project issues against their `title` and `description`."""

    updated_before: str | None = Field(
        default=None,
        description=(
            "Return issues updated on or before the given time. "
            "Expected in ISO 8601 format (`2019-03-15T08:00:00Z`)."
        ),
    )
    """Return issues updated on or before the given time. "
    "Expected in ISO 8601 format (`2019-03-15T08:00:00Z`)."""

    weight: int | None = Field(
        default=None,
        description=(
            "Return issues with the specified `weight`. "
            "`None` returns issues with no weight assigned. "
            "`Any` returns issues with a weight assigned. "
            "Premium and Ultimate only."
        ),
    )
    """Return issues with the specified `weight`.
    `None` returns issues with no weight assigned.
    `Any` returns issues with a weight assigned.
    Premium and Ultimate only."""

    with_labels_details: bool | None = Field(
        default=None,
        description=(
            "If `true`, the response returns more details for each label in labels field: "
            "`:name`, `:color`, `:description`, `:description_html`, `:text_color`. Default is `false`."
        ),
    )
    """If `true`, the response returns more details for each label in labels field: "
    "`:name`, `:color`, `:description`, `:description_html`, `:text_color`. Default is `false`."""

    @field_validator("sort", mode="before")
    @classmethod
    def validate_sort(cls, value: str | None) -> str | None:
        """Validate the sort field.

        Args:
            v: The sort field value.

        Returns:
            The validated sort field value.

        Raises:
            ValueError: If the sort field value is invalid.
        """
        valid_sorts = {
            "created",
            "updated",
            "priority",
            "due_date",
            "relative_position",
            "label_priority",
            "milestone_due",
            "popularity",
            "weight",
        }
        if value is not None and value not in valid_sorts:
            raise ValueError(f"Invalid sort value: {value}. Must be one of {valid_sorts}.")
        return value

    @field_validator("issue_type", mode="before")
    @classmethod
    def validate_issue_type(cls, value: str | None) -> str | None:
        """Validate the issue_type field.

        Args:
            value: The issue_type value to validate.

        Returns:
            The validated issue_type value.
        """
        valid_types = {"issue", "incident", "test_case", "task"}
        if value is not None and value not in valid_types:
            raise ValueError(f"Invalid issue_type: {value}. Must be one of {valid_types}.")
        return value

    @field_validator("not_", mode="before")
    @classmethod
    def validate_not_(cls, value: str | None) -> str | None:
        """Validate the not_ field.

        Args:
            value: The not_ value to validate.

        Returns:
            The validated not_ value.
        """
        valid_not_values = {
            "labels",
            "milestone",
            "author_id",
            "author_username",
            "assignee_id",
            "assignee_username",
            "my_reaction_emoji",
            "search",
            "in",
        }
        if value is not None and value not in valid_not_values:
            raise ValueError(f"Invalid not_ value: {value}. Must be one of {valid_not_values}.")
        return value

    @field_validator("scope", mode="before")
    @classmethod
    def validate_scope(cls, value: str | None) -> str | None:
        """Validate the scope field.

        Args:
            value: The scope value to validate.

        Returns:
            The validated scope value.
        """
        valid_scopes = {"created_by_me", "assigned_to_me", "all"}
        if value is not None and value not in valid_scopes:
            raise ValueError(f"Invalid scope: {value}. Must be one of {valid_scopes}.")
        return value

    @model_validator(mode="after")
    def check_mutually_exclusive_fields(self) -> GitLabListIssuesParams:
        """Check for mutually exclusive fields.

        Returns:
            The validated GitLabListIssuesParams instance.
        """
        if self.assignee is not None and self.assignee_id is not None:
            raise ValueError("assignee and assignee_id are mutually exclusive.")
        if self.author_id is not None and self.author_username is not None:
            raise ValueError("author_id and author_username are mutually exclusive.")
        if self.iteration_id is not None and self.iteration_title is not None:
            raise ValueError("iteration_id and iteration_title are mutually exclusive.")

        return self
