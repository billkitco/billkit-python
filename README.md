# BillKit Python SDK

Official Python SDK for [BillKit](https://billkit.co)—invoice and quote generator for freelancers/small businesses.

[![PyPI](https://badge.fury.io/py/billkit.svg)](https://pypi.org/project/billkit/)

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
