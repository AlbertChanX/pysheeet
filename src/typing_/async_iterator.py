import asyncio

"""
实现了__aiter__()和__anext__()方法的对象，必须返回一个awaitable对象。
async_for支持处理异步迭代器的__anext__()方法返回的可等待对象。
"""


class AsyncIter:
    def __init__(self, it):
        self._it = iter(it)

    def __aiter__(self):
        return self

    async def __anext__(self):
        await asyncio.sleep(1)
        try:
            return next(self._it)
        except StopIteration:
            raise StopAsyncIteration


async def foo():
    running = True
    it = AsyncIter([1, 2, 3])

    async for i in it:
        if i == 1:
            print(i)
            break

    while running:
        try:
            res = await it.__anext__()
            print(res)
        except StopAsyncIteration:
            running = False


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop.create_task(foo()))
