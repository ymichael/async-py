from async.task import *
from async.red import BaseQueue
from nose.tools import eq_


def foo(x):
    """Test function with single argument."""
    return x


def bar(x, y):
    """Test function with multiple arguments."""
    return (x, y)


def baz(x, y, z=0):
    """Test function with keyword arguments."""
    return (x, y, z)


class TestQueue(BaseQueue):
    pass


def test_async_func():
    async_foo = AsyncFunc(foo, TestQueue())

    task_foo = async_foo.create_task(5)
    eq_(5, task_foo())

    task_foo = async_foo.create_task([1,2,3])
    eq_([1,2,3], task_foo())

    task_foo = async_foo.create_task({'x':1, 'y':2})
    eq_({'x':1, 'y':2}, task_foo())


def test_async_func_multi():
    async_bar = AsyncFunc(bar, TestQueue())

    task_bar = async_bar.create_task(5, 10)
    eq_((5, 10), task_bar())

    task_bar = async_bar.create_task(5, [10, 20])
    eq_((5, [10, 20]), task_bar())

    task_bar = async_bar.create_task(5, dict())
    eq_((5, dict()), task_bar())


def test_async_func_keyword():
    async_baz = AsyncFunc(baz, TestQueue())

    task_baz = async_baz.create_task(5, 10)
    eq_((5, 10, 0), task_baz())

    task_baz = async_baz.create_task(5, [10, 20], 10)
    eq_((5, [10, 20], 10), task_baz())

    task_baz = async_baz.create_task(x=1, y=2, z=3)
    eq_((1,2,3), task_baz())
