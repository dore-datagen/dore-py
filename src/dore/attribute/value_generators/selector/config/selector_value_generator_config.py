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
Selector Value Generator config class
"""

from typing import TypeVar, Type
from dore.attribute.value_generators.value_generator_type import ValueGeneratorType
from dore.attribute.value_generators.selector.config.selector_type import SelectorType

T = TypeVar('T')

class SelectorValueGeneratorConfig:
    """
    Config class for Round Robin Selector Value Generator
    """

    _selector_type: SelectorType = None
    _selector_config: dict = None

    def __init__(self, config: dict):
        schema_key = ValueGeneratorType.SELECTOR.schema_key()
        self._selector_type = SelectorType.get(list(config[schema_key].keys())[0])
        self._selector_config = config[schema_key]

    def type(self) -> SelectorType:
        return self._selector_type

    def config(self, cls: Type[T]) -> T:
        return cls(self._selector_config)
