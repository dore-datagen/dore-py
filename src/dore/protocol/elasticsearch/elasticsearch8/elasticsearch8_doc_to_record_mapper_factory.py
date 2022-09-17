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
Build response mapper for elasticsearch8 docs.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable
    from dore.model.model import Model

from dore.protocol.elasticsearch.config.elasticsearch_attribute_properties_config \
    import ElasticSearchAttributePropertiesConfig

def elasticsearch8_doc_to_record_mapper_factory(model: Model) -> Callable[[dict], dict]:
    field_name_attribute_id_map = {}
    for attribute_id, attribute in model.attribute_container().attributes():
        field_name = attribute.config().properties(ElasticSearchAttributePropertiesConfig).field_name()
        field_name_attribute_id_map[field_name] = attribute_id

    def elasticsearch8_doc_to_record_mapper(hit: dict) -> dict:
        record = {}
        source_doc = hit['_source']
        for _field_name in source_doc.keys():
            field_value = source_doc[_field_name]
            _attribute_id = field_name_attribute_id_map[_field_name]
            record[_attribute_id] = field_value

        return record


    return elasticsearch8_doc_to_record_mapper
