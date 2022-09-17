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
Attribute Container
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import ItemsView
    from dore.attribute.attribute import Attribute

class AttributeContainer:

    container: dict[str, Attribute] = None

    def __init__(self):
        self.container = {}

    def add_attribute(self, attribute_id: str, attribute: Attribute):
        self.container[attribute_id] = attribute

    def has_attribute(self, attribute_id: str):
        return attribute_id in self.container

    def get_attribute(self, attribute_id: str):
        return self.container[attribute_id]

    def attributes(self) -> ItemsView[str, Attribute]:
        return self.container.items()
