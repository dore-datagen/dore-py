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
Create a postgresql schema for model.
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.protocol.postgresql.postgresql_datastore import PostgreSQLDatastore

from dore.protocol.postgresql.config.postgresql_model_properties_config import PostgreSQLModelPropertiesConfig

LOGGER = logging.getLogger(__name__)

def postgresql_create_schema(datastore: PostgreSQLDatastore, model: Model) -> None:
    connection = datastore.connection()
    schema_name = model.config().properties(PostgreSQLModelPropertiesConfig).schema_name()

    LOGGER.info("creating schema [%s]", schema_name)

    create_datastore_command = f'CREATE SCHEMA "{schema_name}"'

    cursor = connection.cursor()
    try:
        cursor.execute(create_datastore_command)
    except Exception as err:
        cursor.close()
        raise err

    connection.commit()
    cursor.close()
