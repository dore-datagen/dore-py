# Copyright 2022 Bhargav KN
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""
Redis cache
"""

import redis

from dore.cache.cache import Cache
from dore.utils.rand.rand_utils_factory import rand_utils_factory
from dore.cache.redis.redis_val_serializer import redis_val_serializer
from dore.cache.redis.redis_val_deserializer import redis_val_deserializer

# We can cache the list length values for keys to avoid calling
# redis repeatedly as we won't be adding or removing stuff from
# the cache by the time we make this call.
LIST_LEN_CACHE = {}

BATCHED_WRITE_BUFFER_SIZE = 10000

class RedisCache(Cache):

    pipe = None
    client = None

    def __init__(self, host, port):
        self.client = redis.Redis(
            host=host, port=port,
            charset="utf-8", decode_responses=True
        )
        # clear redis cache during bootstrap_deleteme
        self.clear()

        # Create command pipe
        self.pipe = self.client.pipeline()

    def get(self, key: str) -> any:
        return self.client.get(key)

    def put(self, key: str, value: any):
        pass

    def create_list(self, key: str) -> None:
        pass

    # write lpush operation to pipeline.
    def add_to_list_batched(self, key: str, value: any) -> None:
        if len(self.pipe) > BATCHED_WRITE_BUFFER_SIZE:
            self.flush()

        self.pipe.lpush(key, redis_val_serializer(value))

    # execute operations in pipeline and reset pipeline.
    def flush(self) -> None:
        self.pipe.execute()
        self.pipe = self.client.pipeline()


    def add_to_list(self, key: str, value: str) -> None:
        # need to map object to json string for storing in redis
        json_string = redis_val_serializer(value)
        self.client.lpush(key, json_string)


    def get_random_elem_from_list(self, key: str) -> any:
        if key not in LIST_LEN_CACHE:
            LIST_LEN_CACHE[key] = self.client.llen(key)

        list_len = LIST_LEN_CACHE[key]
        idx = rand_utils_factory().rand_int(0, list_len - 1)
        elem = self.client.lindex(key, idx)

        return redis_val_deserializer(elem)

    def clear(self):
        # delete all keys in db
        self.client.flushdb()
