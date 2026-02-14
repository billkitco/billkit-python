# from ..client import ClientDetails
from .._base import CSVBatchResponse
from ..items import ItemsBase


class InvoiceItem(ItemsBase): ...


class InvoiceCSVBatchResponse(CSVBatchResponse): ...
