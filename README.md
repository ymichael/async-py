# async-py
Poor man's implementation of a redis backed python task queue.

The basic idea is to save the 'fully qualified' module path and function
name as well as the pickled arguments to a queue somewhere. Worker threads
then pick off tasks from this queue and process them asynchronously.

When a function is decorated with @async, the function invokation now
requires the time taken to pickle the arguments and add the resulting
string to the queue.

## usage
1. Run redis (so tasks can be added to the queue)
2. Run worker thread(s) to start picking off tasks from the queue.
3. Add an `@async` decorator to functions that do not need to run inline.

```py
from async import *


def slow_func():
    ...

@async
def slow_func_async():
    slow_func()

```
