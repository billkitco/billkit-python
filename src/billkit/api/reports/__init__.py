from collections.abc import Callable
from ...models.reports import RevenueReportResponse


class Reports:
    def __init__(self, requester: Callable):
        self.requester = requester

    def get_revenue(self, currency: str | None = None):
        endpoint: str = "reports/revenue"
        if (
            currency is None
        ):  # When no currency is added, behaviour defaults to using default currency of the authenticated account
            response_data = self.requester("GET", endpoint)
        else:
            response_data = self.requester("GET", f"{endpoint}?currency={currency}")
        return RevenueReportResponse(**response_data)
