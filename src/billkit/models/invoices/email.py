from .._base import (
    _SendEmailRequest,  # pyright: ignore[reportPrivateUsage]
    _SendEmailResponse,  # pyright: ignore[reportPrivateUsage]
)


class InvoiceSendEmailRequest(_SendEmailRequest): ...


class InvoiceSendEmailResponse(_SendEmailResponse): ...
