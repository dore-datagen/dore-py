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
Model config class
"""

from __future__ import annotations
from jsonschema import validate
from typing import TypeVar, Type

from dore.model.config.persistence_level import PersistenceLevel
from dore.model.config.model_schema import model_schema
from dore.attribute.config.attribute_container_config import AttributeContainerConfig

T = TypeVar('T')

class _ConfigUtils:
    @classmethod
    def should_have_records(cls, persistence_level: PersistenceLevel) -> bool:
        return persistence_level is PersistenceLevel.FULL \
               or persistence_level is PersistenceLevel.MEMORY_ONLY

    @classmethod
    def should_have_datastore(cls, persistence_level: PersistenceLevel) -> bool:
        return persistence_level is PersistenceLevel.FULL

    @classmethod
    def should_have_properties(cls, persistence_level: PersistenceLevel) -> bool:
        return persistence_level is PersistenceLevel.FULL

    @classmethod
    def required_persistence(cls, model_config) -> PersistenceLevel:
        persistence_level = PersistenceLevel.default()
        if 'persistence' in model_config:
            persistence_level = PersistenceLevel[model_config['persistence']]

        return persistence_level


class ModelConfig:
    """
    Config class for model
    """

    _id: str = None
    _records: int = None
    _datastore_id: str = None
    _properties_config: dict = None
    _persistence: PersistenceLevel = None
    _attribute_container_config: AttributeContainerConfig = None

    def __init__(self, model_id, model_config: dict):
        validate(model_config, model_schema)
        self._id = model_id

        # initialize records to generate
        self._persistence = _ConfigUtils.required_persistence(model_config)

        if _ConfigUtils.should_have_records(self._persistence):
            self._records = model_config['records']

        if _ConfigUtils.should_have_datastore(self._persistence):
            self._datastore_id = model_config['datastore']

        if _ConfigUtils.should_have_properties(self._persistence):
            self._properties_config = model_config['properties']

        self._attribute_container_config = AttributeContainerConfig(model_config['attributes'])


    def id(self) -> str:
        """
        Get model id
        """
        return self._id

    def records(self) -> int:
        """
        Get records to generate for model
        """
        return self._records

    def persistence(self) -> PersistenceLevel:
        """
        Get persistence level for model
        """
        return self._persistence

    def datastore_id(self) -> str:
        """
        Get datastore id for model
        """
        return self._datastore_id

    def properties(self, cls: Type[T]) -> T:
        return cls(self._properties_config)

    def attribute_container_config(self) -> AttributeContainerConfig:
        return self._attribute_container_config
