from collections.abc import Callable
from typing import Any

from ...models.reports import RevenueReportResponse


class Reports:
    def __init__(self, requester: Callable[..., dict[str, Any]]) -> None:
        self._requester = requester

    def get_revenue(self, currency: str | None = None) -> RevenueReportResponse:
        """
        Fetch the current user's revenue for a given currency.
        If no currency is passed as a param, the saved default current
        from the authenticated user's account is used
        Returns:
            RevenueReportResponse: The authenticated user's revenue report.

        Example:
            report = client.reports.get_revenue("GBP")
            print(report.summary)
        """
        endpoint: str = "reports/revenue"
        if currency is None:
            response_data = self._requester("GET", endpoint)
        else:
            response_data = self._requester("GET", f"{endpoint}?currency={currency}")
        return RevenueReportResponse(**response_data)
