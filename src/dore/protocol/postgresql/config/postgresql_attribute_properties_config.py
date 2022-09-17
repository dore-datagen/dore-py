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
PostgreSQL Attribute Properties config class
"""

from jsonschema import validate

from dore.protocol.postgresql.config.postgresql_attribute_properties_schema import postgresql_attribute_properties_schema

class PostgreSQLAttributePropertiesConfig:

    _column_name = None
    _column_type = None

    def __init__(self, attribute_properties_config: dict):
        validate(attribute_properties_config, postgresql_attribute_properties_schema)
        self._column_name = attribute_properties_config['columnName']
        self._column_type = attribute_properties_config['columnType']

    def column_name(self):
        """
        Get column name for attribute
        """
        return self._column_name

    def column_type(self):
        """
        Get column type for attribute
        """
        return self._column_type
