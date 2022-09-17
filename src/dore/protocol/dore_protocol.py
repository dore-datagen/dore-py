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
Supported Protocols.
"""

from enum import Enum, unique

@unique
class DoreProtocol(Enum):
    MYSQL = 'mysql'
    MONGODB = 'mongodb'
    POSTGRES = 'postgres'
    ELASTICSEARCH7 = 'elasticsearch7'
    ELASTICSEARCH8 = 'elasticsearch8'

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, schema_key: str):
        self._schema_key = schema_key

    def schema_key(self) -> str:
        return self._schema_key

    @classmethod
    def get(cls, name: str):
        for member in cls:
            if member.name.casefold() == name.casefold():
                return member
