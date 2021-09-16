"""
async with lock:  <==> with (yield from lock):
wait coro() <==> yield from coro()
"""


async def async_fun():
    return 1


async def generator_async_fun():
    yield 1


async def async_fun2():
    async for i in generator_async_fun():
        print(i)


if __name__ == '__main__':
    print(async_fun())  # <coroutine object fun>
    # print(async_fun().send(None))  # StopIteration: 1
    try:
        async_fun().send(None)
    except StopIteration as e:
        print(e.value)  # return 1

    print('\n')
    async_fun2().send(None)
