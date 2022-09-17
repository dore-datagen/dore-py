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
Model Properties schema
"""

from dore.protocol.mysql.config.mysql_model_properties_schema import mysql_model_properties_schema
from dore.protocol.mongodb.config.mongodb_model_properties_schema import mongodb_model_properties_schema
from dore.protocol.postgresql.config.postgresql_model_properties_schema import postgresql_model_properties_schema
from dore.protocol.elasticsearch.config.elasticsearch_model_properties_schema \
    import elasticsearch_model_properties_schema

model_properties_schema = \
{
    'type': 'object',
    'oneOf': [
        {**mysql_model_properties_schema},
        {**postgresql_model_properties_schema},
        {**mongodb_model_properties_schema},
        {**elasticsearch_model_properties_schema}
    ]
}
