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
Datastore :: postgresql
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.datastore.config.datastore_config import DatastoreConfig

import re
import psycopg

from dore.datastore.datastore import Datastore
from dore.protocol.batched_writer import BatchedWriter
from dore.protocol.postgresql.postgresql_model_exists import postgresql_model_exists
from dore.protocol.postgresql.postgresql_delete_model import postgresql_delete_model
from dore.protocol.postgresql.postgresql_create_model import postgresql_create_model
from dore.protocol.postgresql.postgresql_datastore_exists import postgresql_datastore_exists
from dore.protocol.postgresql.postgresql_create_datastore import postgresql_create_datastore
from dore.protocol.postgresql.postgresql_batched_writer import PostgreSQLBatchedWriter
from dore.protocol.postgresql.postgresql_all_records_for_model import postgresql_all_records_for_model
from dore.protocol.postgresql.config.postgresql_datastore_properties_config import PostgreSQLDatastorePropertiesConfig

LOGGER = logging.getLogger(__name__)

def is_database_not_exists_error(err):
    if err.args is not None:
        error_message = err.args[0]
        return re.search('database \".*\" does not exist', error_message) is not None

class PostgreSQLDatastore(Datastore):
    """
    PostgreSQL Datastore
    """

    _connection: psycopg.Connection = None

    def __init__(self, datastore_config: DatastoreConfig):
        super().__init__(datastore_config)
        self.__init_connection__()

    def __init_connection__(self):
        datastore_properties = self._config.properties(PostgreSQLDatastorePropertiesConfig)

        conn_string = f"postgresql://{datastore_properties.user()}:" + \
                      f"{datastore_properties.password()}@" + \
                      f"{datastore_properties.host()}:" + \
                      f"{datastore_properties.port()}/" + \
                      f"{datastore_properties.database()}"

        try:
            # try connecting to database
            self._connection = psycopg.connect(conn_string)

        # database does not exist, so create it
        except psycopg.OperationalError as err:
            if is_database_not_exists_error(err):
                # create connection without initializing db name
                conn_string_wo_dbname = f"postgresql://{datastore_properties.user()}:" \
                                        + f"{datastore_properties.password()}@" \
                                        + f"{datastore_properties.host()}:" \
                                        + f"{int(datastore_properties.port())}"

                self._connection = psycopg.connect(conn_string_wo_dbname)

                # set autocommit to true.
                # ref: https://stackoverflow.com/a/68112827
                # ref: https://github.com/psycopg/psycopg2/issues/1201
                self._connection.autocommit = True

                # create database
                self.create()

        # retry connection to database
        self._connection = psycopg.connect(conn_string)

    def connection(self) -> psycopg.Connection:
        return self._connection

    def exists(self) -> bool:
        return postgresql_datastore_exists(self)

    def create(self) -> None:
        return postgresql_create_datastore(self)

    def create_model(self, model: Model) -> None:
        return postgresql_create_model(self, model)

    def delete_model(self, model: Model) -> None:
        return postgresql_delete_model(self, model)

    def model_exists(self, model: Model) -> bool:
        return postgresql_model_exists(self, model)

    def all_records_for_model(self, model: Model) -> list[dict]:
        return postgresql_all_records_for_model(self, model)

    def get_batched_writer(self, model: Model) -> BatchedWriter:
        return PostgreSQLBatchedWriter(self, model)
