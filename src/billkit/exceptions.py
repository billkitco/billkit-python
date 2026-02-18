"""BillKit SDK exceptions."""


class BillKitException(Exception):
    """
    Base exception for all BillKit SDK errors.

    Wraps HTTP and transport errors from the API so callers can catch
    a single exception type. The original exception is available as __cause__.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        response_body: str | dict | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body
