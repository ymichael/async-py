import redis


QUEUE_NAME = 'async-queue'
_redis_conn = None
_q = None

def get_queue():
    global _q
    if _q is None:
        _q = Queue(QUEUE_NAME)
    return _q


def get_redis_conn():
    global _redis_conn
    if _redis_conn is None:
        _redis_conn = redis.StrictRedis()
    return _redis_conn


class Base(object):
    def __init__(self, name, redis_conn=None):
        self.name = name
        self.redis_conn = redis_conn or get_redis_conn()
        self.key = ':'.join([self.__class__.__name__, self.name])

    def __str__(self):
        return self.__class__.__name__ + '(' + self.name + ')'


class Queue(Base):
    """A simple redis queue."""
    def add(self, item):
        self.redis_conn.rpush(self.key, item)

    def remove(self):
        return self.redis_conn.lpop(self.key)

    def __len__(self):
        return self.redis_conn.llen(self.key)
