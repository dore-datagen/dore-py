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
Attribute
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dore.attribute.config.attribute_config import AttributeConfig
    from dore.attribute.value_generators.dependency import Dependency
    from dore.attribute.attribute_value_generator import AttributeValueGenerator

from dore.attribute.value_generators.value_generator_factory import value_generator_factory


class Attribute:
    _config: AttributeConfig = None
    _is_dependent_attribute: bool = None
    _dependencies: set[Dependency] = None
    _value_generator: AttributeValueGenerator = None

    def __init__(self, attribute_config: AttributeConfig):
        self._config = attribute_config

    def config(self):
        """
        Get Attribute Config
        """
        return self._config

    def value_generator(self) -> AttributeValueGenerator:
        """
        Get Attribute Value Generator
        """
        return self._value_generator

    def register_value_generator(self, context=None) -> None:
        """
        Register value generator for attribute
        """
        self._value_generator = value_generator_factory(self, context)
