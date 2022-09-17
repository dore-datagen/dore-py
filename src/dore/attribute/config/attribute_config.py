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
Attribute Config class
"""

from __future__ import annotations
from jsonschema import validate
from typing import TypeVar, Type

from dore.attribute.config.attribute_schema import attribute_schema
from dore.attribute.value_generators.value_generator_type import ValueGeneratorType


T = TypeVar('T')

class _ConfigUtils:
    @classmethod
    def get_value_generator_type(cls, value_config: dict) -> ValueGeneratorType:
        return ValueGeneratorType.get(list(value_config.keys())[0])

    @classmethod
    def is_dependent_attribute(cls, value_generator_type: ValueGeneratorType) -> bool:
        return value_generator_type is ValueGeneratorType.REF \
               or value_generator_type is ValueGeneratorType.COMPOSITE


class AttributeConfig:

    _id: str = None
    _value_config: dict = None
    _properties_config: dict = None
    _is_dependent_attribute: bool = None
    _value_generator_type: ValueGeneratorType = None

    def __init__(self, attribute_id, attribute_config):
        validate(attribute_config, attribute_schema)

        self._id = attribute_id
        self._value_config = attribute_config['value']
        self._value_generator_type = _ConfigUtils.get_value_generator_type(self._value_config)
        self._is_dependent_attribute = _ConfigUtils.is_dependent_attribute(self._value_generator_type)
        self._properties_config = attribute_config['properties']

    def id(self) -> str:
        """
        Get attribute id
        """
        return self._id

    def value(self, cls: Type[T]) -> T:
        """
        Get value config for attribute
        """
        return cls(self._value_config)

    def properties(self, cls: Type[T]) -> T:
        """
        Get properties config for attribute
        """
        return cls(self._properties_config)

    def is_dependent_attribute(self) -> bool:
        """
        Check whether attribute value is dependent
        on other attributes
        """
        return self._is_dependent_attribute

    def value_generator_type(self) -> ValueGeneratorType:
        """
        Get Value Generator type for Attribute
        """
        return self._value_generator_type
