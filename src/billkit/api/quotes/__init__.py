from collections.abc import Callable

from ...models.quotes import QuoteDeleteResponse
from .._base import _BaseDocuments


class Quotes(_BaseDocuments):
    def __init__(self, requester: Callable):
        super().__init__(requester)

    def delete(self, file_id: str):
        response_data = self._requester("DELETE", f"quotes?file_id={file_id}")
        return QuoteDeleteResponse(**response_data)
