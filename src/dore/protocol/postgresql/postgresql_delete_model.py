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
Delete Model :: postgresql
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.protocol.postgresql.postgresql_datastore import PostgreSQLDatastore

from dore.protocol.postgresql.config.postgresql_model_properties_config import PostgreSQLModelPropertiesConfig

from pypika import Table, Schema, PostgreSQLQuery

LOGGER = logging.getLogger(__name__)

def postgresql_delete_model(datastore: PostgreSQLDatastore, model: Model) -> None:
    connection = datastore.connection()
    model_properties = model.config().properties(PostgreSQLModelPropertiesConfig)
    table_name = model_properties.table_name()
    schema_name = model_properties.schema_name()

    LOGGER.info('dropping table for table [`%s`.`%s`]', schema_name, table_name)

    schema = Schema(schema_name)
    table = Table(table_name, schema)
    query = PostgreSQLQuery.drop_table(table)
    command = query.get_sql()

    cursor = connection.cursor()
    try:
        cursor.execute(command)
    except Exception as err:
        cursor.close()
        raise err

    connection.commit()
    cursor.close()