from collections import Iterable, Iterator, Generator
from inspect import isgenerator, isgeneratorfunction, iscoroutine


class FakeIterable:
    def __iter__(self):
        return 1


class FakeIterator:
    def __iter__(self):
        return 1

    def __next__(self):
        return self.__iter__()


if __name__ == '__main__':
    """
    str list tuple dict
    1. Iterable 实现了__iter__方法
    2. Iterator 实现了 __iter__、__next__方法
    """
    s = 'test'
    print(isinstance(s, Iterable))  # True
    print(hasattr(s, '__iter__'))  # True
    print(isinstance(s, Iterator))  # False
    print(hasattr(s, '__next__'))  # False

    print(isinstance(iter(s), Iterator))  # True
    print(isinstance(FakeIterable(), Iterable))  # True
    print(isinstance(FakeIterator(), Iterator))  # True


    def gen():
        for i in range(10):
            print(f'\nbefore yield: i={i}')
            n = yield i
            if n is not None:
                return 'stop'
            print(f'after yield: n={n}\n')


    g = gen()
    print(isgenerator(g), isgeneratorfunction(gen), iscoroutine(g))
    # send()的作用是在next()的基础上，多了个给xx赋值的功能。 next <==> send(None)
    print(f'next(g): {next(g)}')
    print(f'g.__next__(): {g.__next__()}')
    print(f'g.send(None): {g.send(None)}')
    # g.throw(ValueError)
    g.close()
    try:
        v = g.send(1)
    except StopIteration as e:
        print(f'{repr(e)}: {e.value}')
    print(isinstance(g, Generator))
    print(isinstance(g, Iterator))
