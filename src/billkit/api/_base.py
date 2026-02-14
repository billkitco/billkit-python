from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class _BaseDocuments(ABC):
    def __init__(self, requester: Callable):
        self._requester = requester

    # @abstractmethod
    # def create(self): ...

    # @abstractmethod
    # def list(self): ...

    # @abstractmethod
    # def record(self): ...

    # @abstractmethod
    # def check_storage(self): ...

    @abstractmethod
    def delete(self, file_id: str) -> Any: ...

    # @abstractmethod
    # def create_batch_from_csv(self): ...

    # @abstractmethod
    # def create_batch_from_json(self): ...

    @abstractmethod
    def send_email(
        self,
        to: list[str],
        subject: str,
        body: str,
        from_email: str | None = None,
        file_ids: list[str] | None = None,
    ) -> Any: ...
