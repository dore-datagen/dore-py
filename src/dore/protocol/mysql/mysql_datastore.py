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
Datastore :: mysql
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.datastore.config.datastore_config import DatastoreConfig

import MySQLdb

from dore.datastore.datastore import Datastore
from dore.protocol.batched_writer import BatchedWriter
from dore.protocol.mysql.mysql_model_exists import mysql_model_exists
from dore.protocol.mysql.mysql_create_model import mysql_create_model
from dore.protocol.mysql.mysql_delete_model import mysql_delete_model
from dore.protocol.mysql.mysql_create_datastore import mysql_create_datastore
from dore.protocol.mysql.mysql_datastore_exists import mysql_datastore_exists
from dore.protocol.mysql.mysql_batched_writer import MySQLBatchedWriter
from dore.protocol.mysql.mysql_all_records_for_model import mysql_all_records_for_model
from dore.protocol.mysql.config.mysql_datastore_properties_config import MySQLDatastorePropertiesConfig


LOGGER = logging.getLogger(__name__)

class MySQLDatastore(Datastore):
    """
    MySQL Datastore
    """

    _connection: MySQLdb.Connection = None

    def __init__(self, datastore_config: DatastoreConfig):
        super().__init__(datastore_config)
        self.__init_connection__()

    def __init_connection__(self):
        datastore_properties = self.config().properties(MySQLDatastorePropertiesConfig)
        self._connection = MySQLdb.connect(host=datastore_properties.host(), user=datastore_properties.user(),
                                           port=datastore_properties.port(), passwd=datastore_properties.password())

    def connection(self) -> MySQLdb.Connection:
        return self._connection

    def create(self) -> None:
        return mysql_create_datastore(self)

    def exists(self) -> bool:
        return mysql_datastore_exists(self)

    def create_model(self, model: Model) -> None:
        return mysql_create_model(self, model)

    def delete_model(self, model: Model) -> None:
        return mysql_delete_model(self, model)

    def model_exists(self, model: Model) -> bool:
        return mysql_model_exists(self, model)

    def get_batched_writer(self, model: Model) -> BatchedWriter:
        return MySQLBatchedWriter(self, model)

    def all_records_for_model(self, model: Model) -> list[dict]:
        return mysql_all_records_for_model(self, model)
