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
Get all records for model :: mongodb
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.protocol.mongodb.mongodb_datastore import MongoDBDatastore

from dore.protocol.mongodb.config.mongodb_model_properties_config import MongoDBModelPropertiesConfig
from dore.protocol.mongodb.mongodb_doc_to_record_mapper_factory import mongodb_doc_to_record_mapper_factory
from dore.protocol.mongodb.config.mongodb_datastore_properties_config import MongoDBDatastorePropertiesConfig

def mongodb_all_records_for_model(datastore: MongoDBDatastore, model: Model) -> list[dict]:
    client = datastore.client()
    collection_name = model.config().properties(MongoDBModelPropertiesConfig).collection_name()

    database_name = datastore.config().properties(MongoDBDatastorePropertiesConfig).database()
    response_mapper = mongodb_doc_to_record_mapper_factory(model)

    database = client.get_database(database_name)
    collection = database.get_collection(collection_name)

    for record in map(response_mapper, collection.find()):
        yield record
