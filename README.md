# BillKit Python SDK

Official Python SDK for [BillKit](https://billkit.co)—invoice and quote generator for freelancers/small businesses.

[![PyPI](https://badge.fury.io/py/billkit.svg)](https://pypi.org/project/billkit/)

## Why BillKit Python?

- **Fully typed** — Full type hints and mypy-checked; great IDE support and fewer runtime surprises.
- **Pydantic models** — Request/response validation and serialisation out of the box.
- **Modern stack** — Python 3.11+, [httpx](https://www.python-httpx.org/) as a fully featured HTTP client (requests-style API, connection pooling, timeouts).
- **Simple API** — Resource-based client (`client.invoices`, `client.quotes`, templates, reports, users) with clear return types.
- **Batch workflows** — Create invoices or quotes from CSV or JSON in one call.
- **MIT licensed** — Use it in any project, commercial or open source.

## Installation
```bash
pip install billkit
```

## Quickstart
```python
import os
from billkit import BillKitClient

client = BillKitClient(api_key=os.getenv("BILLKIT_API_KEY"))

# Batch from CSV
client.invoices.batch_create_from_csv(
    data_file_path="invoices.csv",   # id, due_date, etc.
    items_file_path="items.csv"      # items linked by id
)
```

Supports quotes similarly.

## Resources
- [Full Docs](https://billkit.co/docs/sdk/python)
- Batch CSV format: [Guide](https://billkit.co/docs/batch)

## Development
```bash
pip install -e .[dev]
pytest
```

⭐ [Issues](https://github.com/billkitco/billkit-python/issues)
