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
Create mapping :: elasticsearch7
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model

from dore.protocol.elasticsearch.config.elasticsearch_attribute_properties_config import ElasticSearchAttributePropertiesConfig

def elasticsearch8_create_mapping(model: Model) -> dict:
    mapping = {'properties': {}}

    for _, attribute in model.attribute_container().attributes():
        attribute_properties = attribute.config().properties(ElasticSearchAttributePropertiesConfig)
        field_name = attribute_properties.field_name()
        field_type = attribute_properties.field_type()

        # the syntax for mapping payload varies a bit when it comes to simple and complex types
        # so we need to handle it differently.
        if isinstance(field_type, dict):
            mapping['properties'][field_name] = field_type

        else:
            mapping['properties'][field_name] = {'type': field_type}

    return mapping
