__all__ = (
    "Queue",
    "PriorityQueue",
    "LifoQueue",
    "QueueFull",
    "QueueEmpty",
    "QueueShutDown",
)

from asyncio.queues import QueueFull, QueueEmpty
from .compat import Queue, PriorityQueue, LifoQueue, QueueShutDown
