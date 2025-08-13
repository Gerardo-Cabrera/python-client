# python-client

Typed and tested Python client for https://jsonplaceholder.typicode.com

## Requirements
- Python >= 3.10


## Instalation (dev)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Synchronous use

```python
from python_client import PythonClient

client = PythonClient()
posts = client.get_posts(limit=3)
for p in posts:
    print(p.id, p.title)
```

## Asynchronous use

```python
import asyncio
from python_client.async_client import AsyncPythonClient

async def main():
    async with AsyncPythonClient() as client:
        posts = await client.get_posts(limit=3)
        for p in posts:
            print(p.id, p.title)

asyncio.run(main())
```

## Run tests

Run all tests:

```bash
pytest -q
```

This run automatically the tests `tests/test_client.py` and `tests/test_async_client.py`.

Main dependencies for testing:
- pytest
- pytest-asyncio
- httpx

## Run linters and type-check

```bash
flake8 src/ tests/
mypy src/python_client
```

## Author
**Neo-Gerardo**