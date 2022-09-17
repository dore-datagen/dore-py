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
Attribute Container factory
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.attribute.config.attribute_container_config import AttributeContainerConfig

from dore.attribute.attribute_factory import attribute_factory
from dore.attribute.attribute_container import AttributeContainer

def attribute_container_factory(
        attribute_container_config: AttributeContainerConfig
) -> AttributeContainer:
    """
    Attribute Container Factory
    """

    container = AttributeContainer()

    for attribute_id, attribute_config in attribute_container_config.attribute_config_list():
        attribute = attribute_factory(attribute_config)
        container.add_attribute(attribute_id, attribute)

    return container
