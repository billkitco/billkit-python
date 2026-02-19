from .._base import (
    _SendEmailRequest,  # pyright: ignore[reportPrivateUsage]
    _SendEmailResponse,  # pyright: ignore[reportPrivateUsage]
)


class QuoteSendEmailRequest(_SendEmailRequest): ...


class QuoteSendEmailResponse(_SendEmailResponse): ...
