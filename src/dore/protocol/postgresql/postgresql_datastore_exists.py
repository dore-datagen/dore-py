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
Datastore exists :: postgresql
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.protocol.postgresql.postgresql_datastore import PostgreSQLDatastore

from pypika import Table, PostgreSQLQuery, Criterion

from dore.protocol.postgresql.config.postgresql_datastore_properties_config import PostgreSQLDatastorePropertiesConfig

LOGGER = logging.getLogger(__name__)
PG_DATABASE_TABLE = 'pg_database'
PG_CATALOG_DATABASE = 'pg_catalog'

def postgresql_datastore_exists(datastore: PostgreSQLDatastore) -> bool:
    connection = datastore.connection()
    database_name = datastore.config().properties(PostgreSQLDatastorePropertiesConfig).database()

    LOGGER.info('checking if database [%s] exists', database_name)

    table = Table(PG_DATABASE_TABLE, PG_CATALOG_DATABASE)
    query = PostgreSQLQuery.from_(table) \
        .select('*') \
        .where(Criterion.eq(table.datname, database_name))
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
