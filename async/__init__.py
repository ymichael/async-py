import task
import red




def get_async_decorator(queue_name='', host=None, port=None, db=None):
    """Returns a decorator that when applied to functions, make them async.

    Allows configuration of various options:
    - How to connect to redis
    - Queue name (to allow multiple task queues to run on the same redis
      instance)
    """
    # Create redis connection.
    if host is None or port is None or db is None:
        redis_conn = red.get_redis_conn()
    else:
        redis_conn = red.get_redis_conn(host, port, db)
    # Create redis queue
    q = red.RedisQueue(queue_name, redis_conn)
    def async_decorator(f):
        return task.AsyncFunc(f, q)
