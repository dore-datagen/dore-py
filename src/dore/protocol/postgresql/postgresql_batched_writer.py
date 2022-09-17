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
Batched Writer :: postgresql
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable
    from psycopg import Connection
    from dore.model.model import Model
    from dore.protocol.postgresql.postgresql_datastore import PostgreSQLDatastore

from dore.protocol.batched_writer import BatchedWriter
from dore.protocol.postgresql.postgresql_record_to_row_mapper_factory import postgresql_record_to_row_mapper_factory
from dore.protocol.postgresql.config.postgresql_model_properties_config import PostgreSQLModelPropertiesConfig
from dore.protocol.postgresql.config.postgresql_attribute_properties_config import PostgreSQLAttributePropertiesConfig

LOGGER = logging.getLogger(__name__)
BATCH_SIZE = 1000

class PostgreSQLBatchedWriter(BatchedWriter):

    query: str = None
    buffer: list[tuple[object]] = None
    connection: Connection = None
    column_name_order_list: list[str] = None
    attribute_id_order_list: list[str] = None
    buffer_record_mapper: Callable[[dict], tuple] = None

    def __init__(self, datastore: PostgreSQLDatastore, model: Model):
        super().__init__(model)
        self.buffer: list[dict] = []
        self.connection = datastore.connection()
        self.__initialize_column_names__()
        self.__initialize_query__()
        self.__initialize_buffer_record_mapper()

    # create a list of attribute ids and column names to preserve/infer
    # order of columns / attribute_names during insertion.
    def __initialize_column_names__(self):
        self.column_name_order_list = []
        self.attribute_id_order_list = []
        for attribute_id, attribute in self.model.attribute_container().attributes():
            column_name = attribute.config().properties(PostgreSQLAttributePropertiesConfig).column_name()
            self.column_name_order_list.append(column_name)
            self.attribute_id_order_list.append(attribute_id)


    def __initialize_query__(self):
        model_properties = self.model.config().properties(PostgreSQLModelPropertiesConfig)
        table_name = model_properties.table_name()
        schema_name = model_properties.schema_name()

        column_names_string = ','.join(self.column_name_order_list)
        values_placeholder = ','.join(['%s'] * len(self.column_name_order_list))

        self.query = f'INSERT INTO "{schema_name}"."{table_name}" ({column_names_string}) VALUES ({values_placeholder})'

    def __initialize_buffer_record_mapper(self):
        self.buffer_record_mapper = postgresql_record_to_row_mapper_factory(self.attribute_id_order_list)

    def write(self, record: dict) -> None:
        if len(self.buffer) > BATCH_SIZE:
            self.flush()

        self.buffer.append(record)

    def flush(self) -> None:
        if len(self.buffer) > 0:
            rows = list(map(self.buffer_record_mapper, self.buffer))
            cursor = self.connection.cursor()
            try:
                cursor.executemany(self.query, rows)
            except Exception as err:
                cursor.close()
                LOGGER.error('error while writing to model [%s]', self.model.config().id())
                raise err

            self.connection.commit()
            cursor.close()

            self.buffer = []
