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
PostgreSQL Datastore Properties config class
"""

from jsonschema import validate

from dore.protocol.postgresql.config.postgresql_datastore_properties_schema \
    import postgresql_datastore_properties_schema

class PostgreSQLDatastorePropertiesConfig:
    """
    Config class for PostgreSQL Datastore Properties.
    """

    _host: str = None
    _port: int = None
    _user: str = None
    _pass: str = None
    _database: str = None

    def __init__(self, datastore_properties_config):
        validate(datastore_properties_config, postgresql_datastore_properties_schema)
        self._host = datastore_properties_config['host']
        self._port = int(datastore_properties_config['port'])
        self._user = datastore_properties_config['user']
        self._pass = datastore_properties_config['password']
        self._database = datastore_properties_config['database']

    def host(self) -> str:
        """
        Get PostgreSQL host for datastore
        """
        return self._host

    def port(self) -> int:
        """
        Get PostgreSQL port for datastore
        """
        return self._port

    def user(self) -> str:
        """
        Get PostgreSQL user for datastore
        """
        return self._user

    def password(self) -> str:
        """
        Get PostgreSQL password for datastore
        """
        return self._pass

    def database(self) -> str:
        """
        Get PostgreSQL database name for datastore
        """
        return self._database
