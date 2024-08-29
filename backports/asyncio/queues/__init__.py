__all__ = (
    "Queue",
    "PriorityQueue",
    "LifoQueue",
    "QueueFull",
    "QueueEmpty",
    "QueueShutDown",
)

import warnings


try:
    from asyncio.queues import (
        Queue,
        PriorityQueue,
        LifoQueue,
        QueueFull,
        QueueEmpty,
        QueueShutDown,
    )

    warnings.warn(
        "The 'backports.asyncio.queues' package does nothing on Python 3.13 and later. "
        "Consider using the 'asyncio.queues' module directly.",
        DeprecationWarning,
    )

except ImportError:
    from asyncio.queues import QueueFull, QueueEmpty
    from .compat import Queue, PriorityQueue, LifoQueue, QueueShutDown
