import os
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class _BaseDocuments(ABC):
    def __init__(self, requester: Callable) -> None:
        self._requester = requester

    # @abstractmethod
    # def create(self): ...

    # @abstractmethod
    # def list(self): ...

    # @abstractmethod
    # def record(self): ...

    @abstractmethod
    def delete(self, file_id: str) -> Any: ...

    @abstractmethod
    def create_batch_from_csv(
        self,
        data_file_path: os.PathLike[str],
        items_file_path: os.PathLike[str],
    ) -> Any:
        """Create a batch job from two CSV files (data + line items)."""

    @abstractmethod
    def create_batch_from_json(
        self,
        data: dict[str, Any],
    ) -> Any: ...

    @abstractmethod
    def send_email(
        self,
        *,
        to: list[str],
        subject: str,
        body: str,
        from_email: str | None = None,
        file_ids: list[str] | None = None,
    ) -> Any: ...

    def get_batch_status(
        self,
        job_id: str,
    ) -> Any:
        response_data: dict[str, Any] = self._requester(
            "GET",
            f"batch/jobs/{job_id}",
        )
        return response_data
