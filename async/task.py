import os.path
import pickle
import red


def get_function_module(f):
    """Figure out the module path for the given function

    NOTE: The module might be `__main__` if the function is declared in the main
    script. (We need to handle this special case since the task worker will have
    a different `__main__` than this main script.)
    """
    module = f.__module__
    if module == '__main__':
        import __main__
        module = os.path.splitext(__main__.__file__)[0]
    return module


class AsyncFunc(object):
    """A wrapper around a function to make it async."""
    def __init__(self, f):
        self.original_func = f

    def __call__(self, *args, **kwargs):
        task = self.create_task(*args, **kwargs)
        red.get_queue().add(task.serialize())

    def create_task(self, *args, **kwargs):
        return Task(self.original_func, args, kwargs)


class Task(object):
    """Information required to run a single async function.

    Implements the serialize/deserialize functions to allow for adding and
    removing from the task queue.
    """
    def __init__(self, orignal_func, args, kwargs):
        self.original_func = orignal_func
        self.module = get_function_module(orignal_func)
        self.function_name = orignal_func.__name__
        self.args = args
        self.kwargs = kwargs

    def serialize(self):
        task = (self.module, self.function_name, self.args, self.kwargs)
        return pickle.dumps(task)

    @staticmethod
    def deserialize(task):
        module, function_name, args, kwargs = pickle.loads(task)
        # Import module and get original function.
        module = __import__(module)
        original_func = getattr(module, function_name)
        return Task(original_func, args, kwargs)

    def __call__(self):
        """Execute the task."""
        return self.original_func(*self.args, **self.kwargs)


def async(f):
    """Decorator to wrap a function in the AsyncFunc class.

    The basic idea is to save the 'fully qualified' module path and function
    name as well as the pickled arguments to a queue somewhere. Worker threads
    then pick off tasks from this queue and process them asynchronously.

    When a function is decorated with @async, the function invokation now
    requires the time taken to pickle the arguments and add the resulting
    string to the queue.
    """
    return AsyncFunc(f)
