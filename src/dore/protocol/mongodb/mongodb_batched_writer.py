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
Batched Writer :: mongodb
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable
    from pymongo import MongoClient
    from dore.model.model import Model
    from dore.protocol.mongodb.mongodb_datastore import MongoDBDatastore

from dore.protocol.batched_writer import BatchedWriter
from dore.protocol.mongodb.config.mongodb_model_properties_config import MongoDBModelPropertiesConfig
from dore.protocol.mongodb.mongodb_record_to_doc_mapper_factory import mongodb_record_to_doc_mapper_factory
from dore.protocol.mongodb.config.mongodb_datastore_properties_config import MongoDBDatastorePropertiesConfig
from dore.protocol.mongodb.config.mongodb_attribute_properties_config import MongoDBAttributePropertiesConfig

BATCH_SIZE = 1000

class MongoDBBatchedWriter(BatchedWriter):

    buffer: list[dict] = None
    database_name: str = None
    collection_name: str = None
    mongo_client: MongoClient = None
    attribute_id_field_name_map: dict[str, str] = None
    buffer_record_mapper: Callable[[dict], dict] = None

    def __init__(self, datastore: MongoDBDatastore, model: Model):
        super().__init__(model)
        self.mongo_client = datastore.client()
        self.collection_name = model.config().properties(MongoDBModelPropertiesConfig).collection_name()
        self.database_name = datastore.config().properties(MongoDBDatastorePropertiesConfig).database()
        self.buffer = []
        self.__initialize_buffer_record_mapper()
        self.__initialize_attribute_id_field_name_map__()

    def __initialize_buffer_record_mapper(self):
        self.buffer_record_mapper = mongodb_record_to_doc_mapper_factory(self.model)

    def __initialize_attribute_id_field_name_map__(self):
        self.attribute_id_field_name_map = {}
        for attribute_id, attribute in self.model.attribute_container().attributes():
            field_name = attribute.config().properties(MongoDBAttributePropertiesConfig).field_name()
            self.attribute_id_field_name_map[attribute_id] = field_name

    def write(self, record: dict) -> None:
        if len(self.buffer) > BATCH_SIZE:
            self.flush()

        self.buffer.append(record)

    def flush(self) -> None:
        if len(self.buffer) > 0:
            database = self.mongo_client.get_database(self.database_name)
            collection = database.get_collection(self.collection_name)
            payload = list(map(self.buffer_record_mapper, self.buffer))
            collection.insert_many(payload)

            self.buffer = []
