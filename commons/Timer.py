import asyncio


class Timer:
    def __init__(self, timeout, callback, *args):
        self._timeout = timeout
        self._callback = callback
        self._args = args
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback(self._args)

    def cancel(self):
        self._task.cancel()

    def restart(self):
        self._task.cancel()
        self._task = asyncio.ensure_future(self._job())
