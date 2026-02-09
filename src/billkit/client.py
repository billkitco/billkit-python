import os
import httpx
from typing import Any


class BillkitClient:
    """
    client for Billkitco invoicing API.

    Usage:
        client = BillkitClient()  # Uses BILLKITCO_API_KEY env var
        client = BillkitClient(api_key="sk_...")
    """

    def __init__(
        self, api_key: str | None = None, base_url: str = "https://api.billkit.co/v1"
    ) -> None:
        # Check env var first if no param
        if api_key is None:
            api_key = os.getenv("BILLKITCO_API_KEY")

        if not api_key:
            raise ValueError(
                "API key required. Pass to BillkitClient(api_key='sk_...') "
                "or set BILLKITCO_API_KEY environment variable."
            )

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=30.0,
        )

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> dict:
        """Internal proxy to backend API endpoints."""
        url: str = f"{self.base_url}/{endpoint.lstrip('/')}"
        resp: httpx.Response = self._client.request(method, url, **kwargs)
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            return resp.text
