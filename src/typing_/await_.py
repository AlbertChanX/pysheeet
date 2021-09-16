import asyncio
from inspect import isawaitable, iscoroutine
import types


# Awaitable
class SlowObj:
    def __init__(self, n):
        print("__init__")
        self._n = n

    def __await__(self):
        print("__await__ sleep({})".format(self._n))
        # py 3.6-
        # yield from asyncio.sleep(self._n)
        return self


# 把生成器包装为一个协程对象
# @asyncio.coroutine
@types.coroutine
def gen():
    yield from asyncio.sleep(1)
    return 1


async def main():
    obj = await SlowObj(1)
    print(type(obj), obj._n)
    print(f'SlowObj is: {iscoroutine(SlowObj)}')
    print(isawaitable(obj), iscoroutine(obj))

    r = await gen()
    print(f'gen(): {r}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print(f'main() is coroutine: {iscoroutine(main())}')

    # py 3.6+
    loop.run_until_complete(main())
    # py 3.7
    # asyncio.run(main())
