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
Check if postgresql schema for model exists in db.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.protocol.postgresql.postgresql_datastore import PostgreSQLDatastore

from pypika import Table, PostgreSQLQuery, Criterion

from dore.protocol.postgresql.config.postgresql_model_properties_config import PostgreSQLModelPropertiesConfig

def postgresql_schema_exists(datastore: PostgreSQLDatastore, model: Model) -> bool:
    connection = datastore.connection()
    schema_name = model.config().properties(PostgreSQLModelPropertiesConfig).schema_name()

    table = Table('schemata', 'information_schema')
    query = PostgreSQLQuery.from_(table) \
        .select('*') \
        .where(Criterion.eq(table.schema_name, schema_name))
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
