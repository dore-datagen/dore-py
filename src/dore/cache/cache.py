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
Abstract cache class.
"""

from abc import ABC, abstractmethod

class Cache(ABC):

    @abstractmethod
    def get(self, key: str) -> any:
        pass

    @abstractmethod
    def put(self, key: str, value: any) -> None:
        pass

    @abstractmethod
    def create_list(self, key: str) -> None:
        pass

    @abstractmethod
    def add_to_list(self, key: str, value: any) -> None:
        pass

    @abstractmethod
    def get_random_elem_from_list(self, key: str) -> any:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def add_to_list_batched(self, key: str, value: any) -> None:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass
