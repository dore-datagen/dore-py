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
PostgreSQL Model Properties config class
"""

from jsonschema import validate

from dore.protocol.postgresql.config.postgresql_model_properties_schema import postgresql_model_properties_schema

class PostgreSQLModelPropertiesConfig:
    """
    Config class for PostgreSQL Model Properties.
    """

    _table_name: str = None
    _schema_name: str = None

    def __init__(self, model_properties_config: dict):
        validate(model_properties_config, postgresql_model_properties_schema)
        self._table_name = model_properties_config['tableName']
        self._schema_name = model_properties_config['schemaName']

    def table_name(self) -> str:
        """
        Get PostgreSQL table name for model
        """
        return self._table_name

    def schema_name(self) -> str:
        """
        Get PostgreSQL schema name for model
        """
        return self._schema_name
