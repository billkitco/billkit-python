# from ..client import ClientDetails
from .._base import _CSVBatchResponse
from ..items import ItemsBase


class InvoiceItem(ItemsBase): ...


class InvoiceCSVBatchResponse(_CSVBatchResponse): ...
