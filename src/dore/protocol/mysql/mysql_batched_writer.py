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
    from dore.model.model import Model
    from dore.protocol.mysql.mysql_datastore import MySQLDatastore

from dore.protocol.batched_writer import BatchedWriter
from dore.protocol.mysql.config.mysql_model_properties_config import MySQLModelPropertiesConfig
from dore.protocol.mysql.mysql_record_to_row_mapper_factory import mysql_record_to_row_mapper_factory
from dore.protocol.mysql.config.mysql_attribute_properties_config import MySQLAttributePropertiesConfig
from dore.protocol.mysql.config.mysql_datastore_properties_config import MySQLDatastorePropertiesConfig


BATCH_SIZE = 1000

class MySQLBatchedWriter(BatchedWriter):

    query: str = None
    buffer: list[dict] = None
    datastore: MySQLDatastore = None
    column_name_order_list: list[str] = None
    attribute_id_order_list: list[str] = None
    buffer_record_mapper: Callable[[dict], tuple] = None

    def __init__(self, datastore: MySQLDatastore, model: Model):
        super().__init__(model)
        self.buffer: list[dict] = []
        self.datastore = datastore
        self.__initialize_column_names__()
        self.__initialize_query__()
        self.__initialize_buffer_record_mapper()

    # create a list of attribute ids and column names to preserve/infer
    # order of columns / attribute_names during insertion.
    def __initialize_column_names__(self):
        self.column_name_order_list = []
        self.attribute_id_order_list = []
        for attribute_id, attribute in self.model.attribute_container().attributes():
            column_name = attribute.config().properties(MySQLAttributePropertiesConfig).column_name()
            self.column_name_order_list.append(column_name)
            self.attribute_id_order_list.append(attribute_id)


    def __initialize_query__(self):
        table_name = self.model.config().properties(MySQLModelPropertiesConfig).table_name()
        database_name = self.datastore.config().properties(MySQLDatastorePropertiesConfig).database()

        column_names_string = ','.join(self.column_name_order_list)
        values_placeholder = ','.join(['%s'] * len(self.column_name_order_list))

        self.query = f'INSERT INTO `{database_name}`.`{table_name}` ({column_names_string}) VALUES ({values_placeholder})'

    def __initialize_buffer_record_mapper(self):
        self.buffer_record_mapper = mysql_record_to_row_mapper_factory(self.attribute_id_order_list)

    def write(self, record: dict) -> None:
        if len(self.buffer) > BATCH_SIZE:
            self.flush()

        self.buffer.append(record)

    def flush(self) -> None:

        connection = self.datastore.connection()

        if len(self.buffer) > 0:
            rows = list(map(self.buffer_record_mapper, self.buffer))
            cursor = connection.cursor()
            try:
                cursor.executemany(self.query, rows)
            except Exception as err:
                cursor.close()
                raise err

            connection.commit()
            cursor.close()

            self.buffer = []
