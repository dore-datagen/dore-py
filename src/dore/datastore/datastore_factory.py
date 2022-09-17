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
Datastore factory
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.datastore import Datastore
    from dore.datastore.config.datastore_config import DatastoreConfig

from dore.protocol.dore_protocol import DoreProtocol
from dore.exceptions.invalid_manifest_exception import InvalidManifestException
from dore.protocol.mysql.mysql_datastore import MySQLDatastore
from dore.protocol.mongodb.mongodb_datastore import MongoDBDatastore
from dore.protocol.postgresql.postgresql_datastore import PostgreSQLDatastore
from dore.protocol.elasticsearch.elasticsearch7.elasticsearch7_datastore import ElasticSearch7Datastore
from dore.protocol.elasticsearch.elasticsearch8.elasticsearch8_datastore import ElasticSearch8Datastore

LOGGER = logging.getLogger(__name__)

def datastore_factory(datastore_config: DatastoreConfig) -> Datastore:
    """
    Actually create a datastore instance
    """

    LOGGER.info('initializing datastore [%s]', datastore_config.id())
    protocol = datastore_config.protocol()

    if protocol is DoreProtocol.MYSQL:
        return MySQLDatastore(datastore_config)

    elif protocol is DoreProtocol.MONGODB:
        return MongoDBDatastore(datastore_config)

    elif protocol is DoreProtocol.POSTGRES:
        return PostgreSQLDatastore(datastore_config)

    elif protocol is DoreProtocol.ELASTICSEARCH7:
        return ElasticSearch7Datastore(datastore_config)

    elif protocol is DoreProtocol.ELASTICSEARCH8:
        return ElasticSearch8Datastore(datastore_config)

    else:
        raise InvalidManifestException(f'invalid protocol [{protocol}] for config [{datastore_config}]')
