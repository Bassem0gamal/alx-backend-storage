#!/usr/bin/env python3
'''exercise module'''

import redis
import uuid
from typing import Union


def count_calls(method):
    """ Count the number of times a method is called from the cache """
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ My cache class """

    def __init__(self):
        """ Init the cache """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Storing the data in redis """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: callable = None):
        """ Getting the data from redis """
        data = self._redis.get(key)
        if not data:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ Getting the data from redis as string """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """ Getting the data from redis as int """
        return self.get(key, int)
