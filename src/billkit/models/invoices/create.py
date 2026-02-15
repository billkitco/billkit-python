# from ..client import ClientDetails
from .._base import _BaseHeader, _BaseItem, _CSVBatchResponse


class InvoiceItem(_BaseItem): ...


class InvoiceCSVBatchResponse(_CSVBatchResponse): ...


class InvoiceHeader(_BaseHeader): ...
