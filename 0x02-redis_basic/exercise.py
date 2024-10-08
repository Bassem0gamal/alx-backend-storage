#!/usr/bin/env python3
'''exercise module'''


import redis
import uuid
from typing import Union, Callable
from functools import wraps


def replay(method: Callable) -> None:
    """ Display the history of calls of a particular function """
    r = redis.Redis()
    method_name = method.__qualname__
    inputs = r.lrange(f"{method_name}:inputs", 0, -1)
    outputs = r.lrange(f"{method_name}:outputs", 0, -1)
    print("{} was called {} times:"
          .format(method_name, r.get(method_name).decode('utf-8')))

    for inp, outp in zip(inputs, outputs):
        print("{}(*('{}',)) -> {}"
              .format(method_name, inp.decode('utf-8'), outp.decode('utf-8')))


def count_calls(method: Callable) -> Callable:
    """ Count the number of times a method is called from the cache """
    @wraps(method)
    def wrapper(self, *args, **kwargs):

        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Store the history of inputs and outputs """
    @wraps(method)
    def wrapper(self, *args, **kwargs):

        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", result)
        return result
    return wrapper


class Cache:
    """ My cache class """

    def __init__(self):
        """ Init the cache """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
