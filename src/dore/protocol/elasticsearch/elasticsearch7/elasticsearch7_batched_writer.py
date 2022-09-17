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
Batched Writer :: elasticsearch7
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable
    from dore.model.model import Model
    from elasticsearch7 import Elasticsearch
    from dore.protocol.elasticsearch.elasticsearch7.elasticsearch7_datastore import ElasticSearch7Datastore

from elasticsearch7 import helpers
from dore.protocol.batched_writer import BatchedWriter
from dore.protocol.elasticsearch.config.elasticsearch_model_properties_config import ElasticSearchModelPropertiesConfig
from dore.protocol.elasticsearch.config.elasticsearch_attribute_properties_config \
    import ElasticSearchAttributePropertiesConfig

BATCH_SIZE = 1000

def build_buffer_record_mapper(index_name):
    def map_buffer_record_to_index_payload(record):
        return {
            '_index': index_name,
            '_source': record
        }

    return map_buffer_record_to_index_payload


class ElasticSearch7BatchedWriter(BatchedWriter):

    index_name: str = None
    buffer: list[dict] = None
    es_client: Elasticsearch = None
    attribute_id_field_name_map = None
    buffer_record_mapper: Callable[[dict], dict] = None

    def __init__(self, datastore: ElasticSearch7Datastore, model: Model):
        super().__init__(model)
        self.es_client = datastore.client()
        self.buffer = []

        self.index_name = model.config().properties(ElasticSearchModelPropertiesConfig).index_name()

        self.__initialize_attribute_id_field_name_map__()
        self.__initialize_buffer_record_mapper__()

    def __initialize_attribute_id_field_name_map__(self):
        self.attribute_id_field_name_map = {}
        for attribute_id, attribute in self.model.attribute_container().attributes():
            field_name = attribute.config().properties(ElasticSearchAttributePropertiesConfig).field_name()
            self.attribute_id_field_name_map[attribute_id] = field_name

    def __initialize_buffer_record_mapper__(self):
        self.buffer_record_mapper = build_buffer_record_mapper(self.index_name)

    def write(self, record: dict) -> None:
        if len(self.buffer) > BATCH_SIZE:
            self.flush()

        doc = {}
        for attribute_id in record.keys():
            field_name = self.attribute_id_field_name_map[attribute_id]
            field_value = record[attribute_id]
            doc[field_name] = field_value

        self.buffer.append(doc)

    def flush(self) -> None:
        if len(self.buffer) > 0:
            payload = list(map(self.buffer_record_mapper, self.buffer))
            helpers.bulk(self.es_client, payload)
            self.es_client.indices.refresh(index=self.index_name)
            self.buffer = []
