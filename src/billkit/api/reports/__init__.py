from collections.abc import Callable
from ...models.reports import RevenueReportResponse


class Reports:
    def __init__(self, requester: Callable):
        self.requester = requester

    def get_revenue(self, currency: str | None = None):
        """
        Fetch the current user's revenue for a given currency. If no currency is passed as a param,
        Returns:
            RevenueReportResponse: The authenticated user's revenue report.

        Example:
            report = client.reports.get_revenue("GBP")
            print(report.summary)
        """
        endpoint: str = "reports/revenue"
        if currency is None:
            response_data = self.requester("GET", endpoint)
        else:
            response_data = self.requester("GET", f"{endpoint}?currency={currency}")
        return RevenueReportResponse(**response_data)
