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
Get all records for model :: mysql
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.protocol.mysql.mysql_datastore import MySQLDatastore

from pypika import Table, MySQLQuery

from dore.protocol.mysql.config.mysql_model_properties_config import MySQLModelPropertiesConfig
from dore.protocol.mysql.mysql_row_to_record_mapper_factory import mysql_row_to_record_mapper_factory
from dore.protocol.mysql.config.mysql_datastore_properties_config import MySQLDatastorePropertiesConfig
from dore.protocol.mysql.config.mysql_attribute_properties_config import MySQLAttributePropertiesConfig

def mysql_all_records_for_model(datastore: MySQLDatastore, model: Model) -> list[dict]:
    table_name = model.config().properties(MySQLModelPropertiesConfig).table_name()
    database_name = datastore.config().properties(MySQLDatastorePropertiesConfig).database()

    table = Table(table_name, database_name)

    # maintain list of columns to preserve column wise order or values in each row
    columns = []

    # maintain a map of column name -> attribute id to map response back to attribute ids
    column_name_attribute_id_map = {}
    for attribute_id, attribute in model.attribute_container().attributes():
        col_name = attribute.config().properties(MySQLAttributePropertiesConfig).column_name()
        columns.append(col_name)
        column_name_attribute_id_map[col_name] = attribute_id

    response_mapper = mysql_row_to_record_mapper_factory(columns, column_name_attribute_id_map)

    query = MySQLQuery.from_(table) \
        .select(*columns)
    command = query.get_sql()

    cursor = datastore.connection().cursor()

    try:
        cursor.execute(command)
    except Exception as err:
        cursor.close()
        raise err

    # iterate over results and yield it
    row = cursor.fetchone()
    while row:
        yield response_mapper(row)
        row = cursor.fetchone()

    cursor.close()
