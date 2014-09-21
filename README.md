# async-py
Poor man's implementation of a redis backed python task queue.

The basic idea is to save the 'fully qualified' module path and function
name as well as the pickled arguments to a queue somewhere. Worker threads
then pick off tasks from this queue and process them asynchronously.

The way to make a function "async" is via a decorator.

When the resulting function is called, it now requires the time taken to pickle
the arguments and add the resulting string to the queue.

## usage
1. Run redis (so tasks can be added to the queue)
2. Run worker thread(s) to start picking off tasks from the queue.
3. Add the decorator to functions that do not need to run inline.

```py
import async

# Configure your redis connection and queue name etc.
delay = get_async_decorator()


def slow_func():
    ...

@delay
def slow_func_async():
    slow_func()

```

## Running the worker
1. Run from the root folder of your application.
2. Specify redis connection information (optional)
3. Specify queue name (to allow multiple applications to use async-py on the same instance of redis)

```sh
$ py async/worker.py -h
usage: worker.py [-h] -q QUEUE [-r HOST] [-p PORT] [-d DB]

async-py task worker

optional arguments:
  -h, --help            show this help message and exit

Worker configuration:
  -q QUEUE, --queue QUEUE
                        The async-py task queue to pull tasks from.

Redis connection information:
  -r HOST, --host HOST  Redis host.
  -p PORT, --port PORT  Redis port.
  -d DB, --db DB        Redis db.
```