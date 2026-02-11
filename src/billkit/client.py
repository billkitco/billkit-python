import httpx
from typing import Any

from ._settings import get_settings


class BillkitClient:
    """
    client for Billkitco invoicing API.

    Usage:
        client = BillkitClient()  # Uses BILLKIT_SECRET_KEY and BASE_URL env vars
        client = BillkitClient(api_key="sk_...", base_url="https://api.billkit.co/v1")  # Or pass in your own API key and base URL
    """

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        # Check env var first if no param
        settings = get_settings()
        if api_key is None:
            api_key = settings.api_key
        if base_url is None:
            base_url = settings.base_url
        if not api_key:
            raise ValueError(
                "API key required. Pass to BillkitClient(api_key='sk_...') "
                "or set BILLKIT_SECRET_KEY environment variable."
            )

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=30.0,
        )

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> dict[str, Any]:
        """Internal proxy to backend API endpoints."""
        url: str = f"{self.base_url}/{endpoint.lstrip('/')}"
        resp: httpx.Response = self._client.request(method, url, **kwargs)
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            return resp.text
