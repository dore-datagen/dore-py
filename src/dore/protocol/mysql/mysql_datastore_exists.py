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
Datastore exists :: mysql
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.protocol.mysql.mysql_datastore import MySQLDatastore

from pypika import Table, MySQLQuery, Criterion

from dore.protocol.mysql.config.mysql_datastore_properties_config import MySQLDatastorePropertiesConfig

LOGGER = logging.getLogger(__name__)
SCHEMATA_TABLE = 'SCHEMATA'
INFORMATION_SCHEMA = 'information_schema'

def mysql_datastore_exists(datastore: MySQLDatastore) -> bool:
    connection = datastore.connection()
    database_name = datastore.config().properties(MySQLDatastorePropertiesConfig).database()

    LOGGER.info('checking if database [%s] exists', database_name)

    table = Table(SCHEMATA_TABLE, INFORMATION_SCHEMA)
    query = MySQLQuery.from_(table) \
        .select('*') \
        .where(Criterion.eq(table.schema_name, database_name))
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
