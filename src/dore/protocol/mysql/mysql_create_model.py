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
Create Model :: mysql
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.protocol.mysql.mysql_datastore import MySQLDatastore

from pypika import Table, MySQLQuery, Column

from dore.protocol.mysql.config.mysql_model_properties_config import MySQLModelPropertiesConfig
from dore.protocol.mysql.config.mysql_attribute_properties_config import MySQLAttributePropertiesConfig
from dore.protocol.mysql.config.mysql_datastore_properties_config import MySQLDatastorePropertiesConfig

LOGGER = logging.getLogger(__name__)

def mysql_create_model(datastore: MySQLDatastore, model: Model) -> None:
    connection = datastore.connection()
    table_name = model.config().properties(MySQLModelPropertiesConfig).table_name()
    database_name = datastore.config().properties(MySQLDatastorePropertiesConfig).database()

    LOGGER.info('creating table [`%s`.`%s`]', database_name, table_name)

    columns = []
    for _, attribute in model.attribute_container().attributes():
        attribute_properties = attribute.config().properties(MySQLAttributePropertiesConfig)
        column_name = attribute_properties.column_name()
        column_type = attribute_properties.column_type()
        columns.append(Column(column_name, column_type))

    table = Table(table_name, database_name)
    query = MySQLQuery \
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
