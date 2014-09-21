import redis


_redis_conn = dict()


def get_redis_conn(host='localhost', port=6379, db=0):
    """Returns a redis connection with the specified options."""
    key = '%s:%s:%s' % (host, port, db)
    if key not in _redis_conn:
        _redis_conn[key] = redis.StrictRedis(host=host, port=port, db=db)
    return _redis_conn[key]


class BaseQueue(object):
    """Base queue interface."""
    def add(self, item):
        raise NotImplementedError()

    def remove(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()


QUEUE_NAME_PREFIX = 'async-py-task-queue:'


class RedisQueue(BaseQueue):
    """A simple redis queue."""
    def __init__(self, name, redis_conn=None):
        self.name = QUEUE_NAME_PREFIX + name
        self.redis_conn = redis_conn or get_redis_conn()
        self.key = ':'.join([self.__class__.__name__, self.name])

    def add(self, item):
        self.redis_conn.rpush(self.key, item)

    def remove(self):
        return self.redis_conn.lpop(self.key)

    def __len__(self):
        return self.redis_conn.llen(self.key)