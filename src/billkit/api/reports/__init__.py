from collections.abc import Callable


class Reports:
    def __init__(self, requester: Callable):
        self.requester = requester

    def get_revenue(self, currency: str | None = None):
        endpoint: str = "reports/revenue"
        if currency is None:
            return self.requester("GET", endpoint)
        return self.requester("GET", f"{endpoint}?currency={currency}")
