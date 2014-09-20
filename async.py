import pickle
import red


def async(f):
    """Decorator to make a function run in a separate task queue.

    The basic idea is to save the 'fully qualified' module path and function
    name as well as the pickled arguments to a queue somewhere. Worker threads
    then pick off tasks from this queue and process them asynchronously.

    When a function is decorated with @async, the function invokation now
    requires the time taken to pickle the arguments and add the resulting
    string to the queue.
    """
    module = f.__module__
    # module might be __main__ if the async decorator is used in the main
    # script being run.
    if module == '__main__':
        import os.path
        import __main__
        module = os.path.splitext(__main__.__file__)[0]
    func_name = f.__name__

    def async_f(*args, **kwargs):
        task = (module, func_name, args, kwargs)
        pickled_task = pickle.dumps(task)
        red.get_queue().add(pickled_task)

    async_f.original_function = f
    return async_f


def exec_task(task):
    module, func_name, args, kwargs = pickle.loads(task)
    print 'PROCESSING', module, func_name
    module = __import__(module)
    func = getattr(module, func_name)
    func.original_function(*args, **kwargs)


