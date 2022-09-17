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
Get all records for model :: postgresql
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.protocol.postgresql.postgresql_datastore import PostgreSQLDatastore

from pypika import Table, Schema, PostgreSQLQuery

from dore.protocol.postgresql.config.postgresql_model_properties_config import PostgreSQLModelPropertiesConfig
from dore.protocol.postgresql.postgresql_row_to_record_mapper_factory import postgresql_row_to_record_mapper_factory
from dore.protocol.postgresql.config.postgresql_attribute_properties_config import PostgreSQLAttributePropertiesConfig

def postgresql_all_records_for_model(datastore: PostgreSQLDatastore, model: Model) -> list[dict]:
    connection = datastore.connection()
    table_name = model.config().properties(PostgreSQLModelPropertiesConfig).table_name()
    schema_name = model.config().properties(PostgreSQLModelPropertiesConfig).schema_name()

    # maintain list of columns to preserve column wise order or values in each row
    column_name_order_list = []
    # maintain a map of column name -> attribute id to map response back to attribute ids
    column_name_attribute_id_map = {}

    for attribute_id, attribute in model.attribute_container().attributes():
        column_name = attribute.config().properties(PostgreSQLAttributePropertiesConfig).column_name()
        column_name_order_list.append(column_name)
        column_name_attribute_id_map[column_name] = attribute_id

    schema = Schema(schema_name)
    table = Table(table_name, schema)
    query = PostgreSQLQuery.from_(table) \
        .select(*column_name_order_list)
    command = query.get_sql()

    response_mapper = postgresql_row_to_record_mapper_factory(column_name_order_list, column_name_attribute_id_map)

    cursor = connection.cursor()
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
