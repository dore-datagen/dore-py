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
Datastore Definition schema
"""

from dore.protocol.dore_protocol import DoreProtocol
from dore.protocol.mysql.config.mysql_datastore_properties_schema import mysql_datastore_properties_schema
from dore.protocol.mongodb.config.mongodb_datastore_properties_schema import mongodb_datastore_properties_schema
from dore.protocol.postgresql.config.postgresql_datastore_properties_schema \
    import postgresql_datastore_properties_schema
from dore.protocol.elasticsearch.config.elasticsearch_datastore_properties_schema \
    import elasticsearch_datastore_properties_schema

datastore_definition_schema = {
    'type': 'object',
    'properties': {
        'protocol': {
            'type': 'string',
            'enum': [protocol.name.casefold() for protocol in DoreProtocol]
        },
        'properties': {
            'anyOf': [
                {**mysql_datastore_properties_schema},
                {**postgresql_datastore_properties_schema},
                {**mongodb_datastore_properties_schema},
                {**elasticsearch_datastore_properties_schema},
            ]
        },
    },
    'required': ['protocol', 'properties'],
    'additionalProperties': False
}
