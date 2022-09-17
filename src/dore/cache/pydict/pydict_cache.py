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
Python dictionary cache.
"""

from dore.cache.cache import Cache
from dore.utils.rand.rand_utils_factory import rand_utils_factory

class PydictCache(Cache):

    store: dict = None

    def __init__(self):
        self.store = {}

    def get(self, key: str) -> any:
        return self.store[key]

    def put(self, key: str, value: any):
        self.store[key] = value

    def create_list(self, key: str) -> None:
        self.store[key] = []

    def add_to_list(self, key: str, value: str) -> None:
        if key not in self.store:
            self.create_list(key)

        self.store[key].append(value)

    def get_random_elem_from_list(self, key: str) -> any:
        list_len = len(self.store[key])
        idx = rand_utils_factory().rand_int(0, list_len - 1)
        return self.store[key][idx]

    def clear(self) -> None:
        pass

    def add_to_list_batched(self, key: str, value: any) -> None:
        self.add_to_list(key, value)

    def flush(self) -> None:
        pass
