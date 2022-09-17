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
Build request mapper for mongodb records
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model

import datetime

from dore.protocol.mongodb.config.mongodb_attribute_properties_config import MongoDBAttributePropertiesConfig

def mongodb_record_to_doc_mapper_factory(model: Model):
    attribute_id_to_field_name_map = {}
    for attribute_id, attribute in model.attribute_container().attributes():
        field_name = attribute.config().properties(MongoDBAttributePropertiesConfig).field_name()
        attribute_id_to_field_name_map[attribute_id] = field_name

    def mongodb_record_to_doc_mapper(record: dict):
        doc = {}
        for _attribute_id in record.keys():
            _field_name = attribute_id_to_field_name_map[_attribute_id]
            field_value = record[_attribute_id]

            # pymongo doesn't support saving date instances so cast it to datetime before saving
            # @see https://stackoverflow.com/a/44273588/6304483 for more info.
            if isinstance(field_value, datetime.date):
                field_value = datetime.datetime.combine(field_value, datetime.time.min)

            doc[_field_name] = field_value

        return doc

    return mongodb_record_to_doc_mapper