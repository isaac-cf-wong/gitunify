"""Base class for Issue API clients."""

from __future__ import annotations

from abc import abstractmethod

from pydantic import ValidationError

from gitunify.issue.data import IssueData, IssueDataList
from gitunify.issue.params import ListIssuesParams
from gitunify.utils.validation import log_validation_errors


class Issue:  # pylint: disable=too-few-public-methods
    """Base class for Issue API clients."""

    _list_issues_params: type[ListIssuesParams] = ListIssuesParams

    def __init__(self, **kwargs) -> None:
        """Initialize the Issue API client."""

    def list_issues(  # pylint: disable=too-many-arguments, too-many-positional-arguments, too-many-locals
        self,
        owner: str,
        repository: str,
        state: str | None = None,
        assignee: str | None = None,
        milestone: str | None = None,
        labels: list[str] | None = None,
        sort: str | None = None,
        direction: str | None = None,
        since: str | None = None,
        per_page: int = 30,
        page: int = 1,
        return_raw: bool = False,
        **kwargs,
    ) -> IssueDataList:
        """List issues for a repository.

        Args:
            owner: Repository owner.
            repository: Repository name.
            state: Filter by state (e.g., 'open', 'closed', 'all').
            assignee: Filter by assignee username.
            milestone: Filter by milestone title.
            labels: Filter by labels (list of label names).
            sort: Sort field (e.g., 'created', 'updated', 'comments').
            direction: Sort direction ('asc' or 'desc').
            since: Only issues updated at or after this time are returned (ISO 8601 format).
            per_page: Number of issues per page (default is 30).
            page: Page number of the results to fetch (default is 1).
            return_raw: If True, return the raw JSON response.
            **kwargs: Additional parameters specific to the platform.
        """
        # Create parameter object (handles validation automatically)
        try:
            params_obj = self._list_issues_params(
                state=state,
                assignee=assignee,
                milestone=milestone,
                labels=labels,
                sort=sort,
                direction=direction,
                since=since,
                per_page=per_page,
                page=page,
                **kwargs,
            )
        except ValidationError as e:
            log_validation_errors(e, self._list_issues_params)
            raise

        # Convert to dict, excluding None values
        params = params_obj.model_dump(exclude_none=True)

        # Transform generic parameters to platform-specific parameters
        transformed_params = self._transform_list_issues_params(**params)

        url = self._build_list_issues_url(owner=owner, repository=repository)
        response = self._request(  # pylint: disable=no-member
            method="GET",
            url=url,
            headers=self.headers,  # pylint: disable=no-member
            params=transformed_params,
        )
        if return_raw:
            return response.json()
        return self._parse_json_response(data=response.json(), per_page=per_page, page=page)

    @abstractmethod
    def _build_list_issues_url(self, owner: str, repository: str) -> str:
        """Build the URL for listing issues.

        Args:
            owner: Repository owner.
            repository: Repository name.

        Returns:
            The URL as a string.
        """

    def _transform_list_issues_params(self, **kwargs) -> dict:
        """Transform generic parameters to platform-specific parameters.

        Args:
            kwargs: Generic parameters.

        Returns:
            Transformed parameters as a dictionary.
        """
        return kwargs

    def _parse_json_response(self, data: dict, per_page: int, page: int) -> IssueDataList:
        """Parse the JSON response into an IssueDataList.

        Args:
            data: The JSON data from the response.
            per_page: Number of issues per page.
            page: Current page number.

        Returns:
            An IssueDataList object.
        """
        issues = [IssueData(**item, platform=self._platform) for item in data]  # pylint: disable=no-member
        return IssueDataList(issues=issues, page=page, per_page=per_page)
