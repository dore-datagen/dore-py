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
    from dore.protocol.mysql.mysql_datastore import MySQLDatastore

from pypika import Table, MySQLQuery
from MySQLdb._exceptions import ProgrammingError

from dore.protocol.mysql.config.mysql_model_properties_config import MySQLModelPropertiesConfig
from dore.protocol.mysql.config.mysql_datastore_properties_config import MySQLDatastorePropertiesConfig

LOGGER = logging.getLogger(__name__)
ERROR_CODE_TABLE_DOES_NOT_EXIST = 1146

def mysql_model_exists(datastore: MySQLDatastore, model: Model) -> bool:
    connection = datastore.connection()
    table_name = model.config().properties(MySQLModelPropertiesConfig).table_name()
    database_name = datastore.config().properties(MySQLDatastorePropertiesConfig).database()

    LOGGER.info('checking existence for table [`%s`.`%s`]', database_name, table_name)

    table = Table(table_name, database_name)
    query = MySQLQuery.from_(table) \
        .select('*') \
        .limit(1)
    command = query.get_sql()

    cursor = connection.cursor()
    try:
        cursor.execute(command)
    except ProgrammingError as err:
        cursor.close()
        error_code = err.args[0]
        # if it is a table does not exist error, return false
        if error_code == ERROR_CODE_TABLE_DOES_NOT_EXIST:
            return False

        # bubble up the error otherwise
        raise err

    cursor.close()
    return True
