from .._base import _BaseDocumentResponse  # pyright: ignore[reportPrivateUsage]


class QuoteDocumentResponse(_BaseDocumentResponse):
    quote_number: str
