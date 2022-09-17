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
Model exists :: mysql
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.protocol.postgresql.postgresql_datastore import PostgreSQLDatastore

from dore.protocol.postgresql.config.postgresql_model_properties_config import PostgreSQLModelPropertiesConfig

from pypika import Table, PostgreSQLQuery, Criterion

LOGGER = logging.getLogger(__name__)

def postgresql_model_exists(datastore: PostgreSQLDatastore, model: Model) -> bool:
    connection = datastore.connection()
    model_properties = model.config().properties(PostgreSQLModelPropertiesConfig)
    table_name = model_properties.table_name()
    schema_name = model_properties.schema_name()

    LOGGER.info('checking existence for table [`%s`.`%s`]', schema_name, table_name)

    table = Table('tables', 'information_schema')
    query = PostgreSQLQuery.from_(table) \
        .select('*') \
        .where(Criterion.eq(table.table_schema, schema_name)) \
        .where(Criterion.eq(table.table_name, table_name))
    command = query.get_sql()

    cursor = connection.cursor()
    try:
        cursor.execute(command)
    except Exception as err:
        cursor.close()
        raise err

    result = cursor.fetchone()
    cursor.close()

    # return true if non empty results were received
    return result is not None and len(result) > 0
