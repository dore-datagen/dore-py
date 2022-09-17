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
Create Model :: postgresql
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.protocol.postgresql.postgresql_datastore import PostgreSQLDatastore

from pypika import Table, Column, Schema, PostgreSQLQuery

from dore.protocol.postgresql.postgresql_schema_exists import postgresql_schema_exists
from dore.protocol.postgresql.postgresql_create_schema import postgresql_create_schema
from dore.protocol.postgresql.config.postgresql_model_properties_config import PostgreSQLModelPropertiesConfig
from dore.protocol.postgresql.config.postgresql_attribute_properties_config import PostgreSQLAttributePropertiesConfig

LOGGER = logging.getLogger(__name__)

def postgresql_create_model(datastore: PostgreSQLDatastore, model: Model) -> None:
    connection = datastore.connection()
    model_properties = model.config().properties(PostgreSQLModelPropertiesConfig)
    table_name = model_properties.table_name()
    schema_name = model_properties.schema_name()

    if not postgresql_schema_exists(datastore, model):
        postgresql_create_schema(datastore, model)

    LOGGER.info('creating table [`%s`.`%s`]', schema_name, table_name)

    columns = []
    for _, attribute in model.attribute_container().attributes():
        attribute_properties = attribute.config().properties(PostgreSQLAttributePropertiesConfig)
        column_name = attribute_properties.column_name()
        column_type = attribute_properties.column_type()
        columns.append(Column(column_name, column_type))

    schema = Schema(schema_name)
    table = Table(table_name, schema)
    query = PostgreSQLQuery \
        .create_table(table) \
        .columns(*columns)
    command = query.get_sql()

    cursor = connection.cursor()

    try:
        cursor.execute(command)
    except Exception as err:
        cursor.close()
        raise err

    connection.commit()
    cursor.close()
