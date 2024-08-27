# `backports.asyncio.queues`: Backport of the standard library module `asyncio.queues`

Python 3.13 adds a `shutdown` method to `asyncio.queue.Queue`. This package ports the feature to Python 3.9 through 3.12.

Consult the [3.13 specific documentation on Queue](https://docs.python.org/3.13/library/asyncio-queue.html#queue) for usage.

## Installation and depending on this library

This module is called [`backports.asyncio.queues`](https://pypi.org/project/backports.asyncio.queues) on PyPI. To install it in your local environment, use:

```
pip install backports.asyncio.queues
```

## Use

The `backports.asyncio.queues` module should be a drop-in replacement for the Python 3.13 standard library module `asyncio.queue`. If you do not support anything earlier than Python 3.13, **you do not need this library**; you may want to use this idiom to "fall back" to ``backports.asyncio.queues``:

```python
try:
    from asyncio.queues import Queue, QueueShutDown
except ImportError:
    from backports.asyncio.queues import Queue, QueueShutDown
```

You must import `QueueShutDown` in order for this pattern to work, as it doesn't exist on Python 3.12 and earlier.

Alternatively, you can use `sys.version_info` explicitly:

```python
import sys

if sys.version_info >= (3, 13):
    from asyncio.queues import Queue
else:
    from backports.asyncio.queues import Queue
```