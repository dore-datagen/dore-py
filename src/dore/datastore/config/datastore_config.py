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
Datastore config class
"""

from jsonschema import validate
from typing import TypeVar, Type

from dore.protocol.dore_protocol import DoreProtocol
from dore.datastore.config.datastore_schema import datastore_schema

T = TypeVar("T")

class DatastoreConfig:
    """
    Config class for Datastore
    """

    _id: str = None
    _protocol: DoreProtocol = None
    _properties_config: T = None

    def __init__(self, datastore_id: str, datastore_config: dict = None):
        validate(datastore_config, datastore_schema)

        self._id = datastore_id
        self._properties_config = datastore_config['properties']
        self._protocol = DoreProtocol.get(datastore_config['protocol'])

    def id(self) -> str:
        """
        Get datastore ID
        """
        return self._id

    def protocol(self) -> DoreProtocol:
        """
        Get datastore protocol
        """
        return self._protocol

    def properties(self, cls: Type[T]) -> T:
        """
        Return an instance of properties casted to protocol
        specific datastore properties config types.
        """
        return cls(self._properties_config)
