#!/usr/bin/env python3
'''exercise module'''

import redis
import uuid
from typing import Union


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
