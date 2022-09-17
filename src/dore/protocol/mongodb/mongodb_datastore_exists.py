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
Datastore exists :: mongodb
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.protocol.mongodb.mongodb_datastore import MongoDBDatastore

from dore.protocol.mongodb.config.mongodb_datastore_properties_config import MongoDBDatastorePropertiesConfig

LOGGER = logging.getLogger(__name__)

def mongodb_datastore_exists(datastore: MongoDBDatastore) -> bool:
    client = datastore.client()
    database_name = datastore.config().properties(MongoDBDatastorePropertiesConfig).database()

    LOGGER.info('checking if database [%s] exists', database_name)

    database_name_list = client.list_database_names()
    return database_name in database_name_list
