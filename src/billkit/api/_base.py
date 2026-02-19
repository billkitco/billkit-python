import os
from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from ..models._base import _BaseItem

if TYPE_CHECKING:
    from io import BytesIO

T = TypeVar("T", bound="_BaseItem")


class _BaseDocuments(ABC, Generic[T]):
    def __init__(self, requester: Callable[..., Any]) -> None:
        self._requester = requester

    @abstractmethod
    def create(
        self,
        *,
        client_name: str,
        client_email: str,
        items: Sequence[T],
        save_to_cloud: bool = True,
        **kwargs: Any,
    ) -> "BytesIO": ...

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
        to: Sequence[str],
        subject: str,
        body: str,
        from_email: str | None = None,
        file_ids: Sequence[str] | None = None,
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

    @abstractmethod
    def list(self, *, limit: int, offset: int) -> Sequence[Any]: ...
