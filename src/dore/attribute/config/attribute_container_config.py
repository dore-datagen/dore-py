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
Attribute Container config class
"""

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import ItemsView

from jsonschema import validate

from dore.attribute.config.attribute_config import AttributeConfig
from dore.attribute.config.attribute_container_schema import attribute_container_schema

class AttributeContainerConfig:

    container: dict[str, AttributeConfig] = None

    def __init__(self, attribute_container_config: dict):
        validate(attribute_container_config, attribute_container_schema)

        self.container = {}
        for attribute_id, attribute_config in attribute_container_config.items():
            self.container[attribute_id] = AttributeConfig(attribute_id, attribute_config)

    def attribute_config(self, attribute_id) -> AttributeConfig:
        return self.container[attribute_id]

    def has_attribute_config(self, attribute_id: str) -> bool:
        return attribute_id in self.container

    def attribute_config_list(self) -> ItemsView[str, AttributeConfig]:
        return self.container.items()