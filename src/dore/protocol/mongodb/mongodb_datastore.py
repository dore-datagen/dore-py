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
Datastore :: mongodb
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.datastore.config.datastore_config import DatastoreConfig

from pymongo import MongoClient

from dore.datastore.datastore import Datastore
from dore.protocol.batched_writer import BatchedWriter
from dore.protocol.mongodb.mongodb_model_exists import mongodb_model_exists
from dore.protocol.mongodb.mongodb_delete_model import mongodb_delete_model
from dore.protocol.mongodb.mongodb_datastore_exists import mongodb_datastore_exists
from dore.protocol.mongodb.mongodb_batched_writer import MongoDBBatchedWriter
from dore.protocol.mongodb.mongodb_all_records_for_model import mongodb_all_records_for_model
from dore.protocol.mongodb.config.mongodb_datastore_properties_config import MongoDBDatastorePropertiesConfig

LOGGER = logging.getLogger(__name__)

class MongoDBDatastore(Datastore):

    mongo_client: MongoClient = None

    def __init__(self, datastore_config: DatastoreConfig):
        super().__init__(datastore_config)
        self.__init_mongo_client__()

    def __init_mongo_client__(self):
        properties_config = self._config.properties(MongoDBDatastorePropertiesConfig)
        connection_string = f"mongodb://{properties_config.user()}:" \
                            + f"{properties_config.password()}@" \
                            + f"{properties_config.host()}:" \
                            + f"{properties_config.port()}/"
        self.mongo_client = MongoClient(connection_string)

    def client(self) -> MongoClient:
        return self.mongo_client

    def create(self) -> None:
        """
        Do Nothing. Databases are automatically created when they are written to.
        """
        pass

    def exists(self) -> bool:
        return mongodb_datastore_exists(self)

    def create_model(self, model: Model) -> None:
        """
        Do Nothing. Collections are automatically created when they are written to.
        """
        pass

    def delete_model(self, model: Model) -> None:
        return mongodb_delete_model(self, model)

    def model_exists(self, model: Model) -> bool:
        return mongodb_model_exists(self, model)

    def all_records_for_model(self, model: Model) -> list[dict]:
        return mongodb_all_records_for_model(self, model)

    def get_batched_writer(self, model: Model) -> BatchedWriter:
        return MongoDBBatchedWriter(self, model)
