from asyncio.queues import (
    Queue as BaseQueue,
    PriorityQueue as BasePriorityQueue,
    LifoQueue as BaseLifoQueue,
)

from typing import Generic, TypeVar


class QueueShutDown(Exception):
    """Raised when putting on to or getting from a shut-down Queue."""

    pass


_T = TypeVar("_T")


class _ShutDownMixin(Generic[_T]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_shutdown = False

    def _format(self, *args, **kwargs) -> str:
        result = super()._format(*args, **kwargs)
        if self._is_shutdown:
            result += " shutdown"
        return result

    # Because the _is_shutdown conditional is inside a loop buried in the
    # method, the entire method is copied, and re-implemented.
    # Types will not be correctly inferred without annotations, which have
    # been provided here
    async def put(self, item: _T) -> None:
        """Put an item into the queue.

        Put an item into the queue. If the queue is full, wait until a free
        slot is available before adding item.

        Raises QueueShutDown if the queue has been shut down.
        """
        while self.full():
            if self._is_shutdown:
                raise QueueShutDown
            putter = self._get_loop().create_future()
            self._putters.append(putter)
            try:
                await putter
            except:
                putter.cancel()  # Just in case putter is not done yet.
                try:
                    # Clean self._putters from canceled putters.
                    self._putters.remove(putter)
                except ValueError:
                    # The putter could be removed from self._putters by a
                    # previous get_nowait call or a shutdown call.
                    pass
                if not self.full() and not putter.cancelled():
                    # We were woken up by get_nowait(), but can't take
                    # the call.  Wake up the next in line.
                    self._wakeup_next(self._putters)
                raise
        return self.put_nowait(item)

    def put_nowait(self, item: _T) -> None:
        if self._is_shutdown:
            raise QueueShutDown
        super().put_nowait(item)

    # Because the _is_shutdown conditional is inside a loop buried in the
    # method, the entire method is copied, and re-implemented.
    # Types will not be correctly inferred without annotations, which have
    # been provided here
    async def get(self) -> _T:
        """Remove and return an item from the queue.

        If queue is empty, wait until an item is available.

        Raises QueueShutDown if the queue has been shut down and is empty, or
        if the queue has been shut down immediately.
        """
        while self.empty():
            if self._is_shutdown and self.empty():
                raise QueueShutDown
            getter = self._get_loop().create_future()
            self._getters.append(getter)
            try:
                await getter
            except:
                getter.cancel()  # Just in case getter is not done yet.
                try:
                    # Clean self._getters from canceled getters.
                    self._getters.remove(getter)
                except ValueError:
                    # The getter could be removed from self._getters by a
                    # previous put_nowait call, or a shutdown call.
                    pass
                if not self.empty() and not getter.cancelled():
                    # We were woken up by put_nowait(), but can't take
                    # the call.  Wake up the next in line.
                    self._wakeup_next(self._getters)
                raise
        return self.get_nowait()

    def get_nowait(self) -> _T:
        if self.empty() and self._is_shutdown:
            raise QueueShutDown
        return super().get_nowait()

    def shutdown(self, immediate: bool = False) -> None:
        """Shut-down the queue, making queue gets and puts raise QueueShutDown.

        By default, gets will only raise once the queue is empty. Set
        'immediate' to True to make gets raise immediately instead.

        All blocked callers of put() and get() will be unblocked. If
        'immediate', a task is marked as done for each item remaining in
        the queue, which may unblock callers of join().
        """
        self._is_shutdown = True
        if immediate:
            while not self.empty():
                self._get()
                if self._unfinished_tasks > 0:
                    self._unfinished_tasks -= 1
            if self._unfinished_tasks == 0:
                self._finished.set()
        # All getters need to re-check queue-empty to raise ShutDown
        while self._getters:
            getter = self._getters.popleft()
            if not getter.done():
                getter.set_result(None)
        while self._putters:
            putter = self._putters.popleft()
            if not putter.done():
                putter.set_result(None)


class Queue(_ShutDownMixin[_T], BaseQueue[_T]):
    pass


class PriorityQueue(_ShutDownMixin[_T], BasePriorityQueue[_T]):
    pass


class LifoQueue(_ShutDownMixin[_T], BaseLifoQueue[_T]):
    pass
