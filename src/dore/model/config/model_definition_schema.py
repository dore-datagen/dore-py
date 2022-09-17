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
Model Definition schema
"""

from dore.model.config.persistence_level import PersistenceLevel
from dore.model.config.model_properties_schema import model_properties_schema
from dore.attribute.config.attribute_container_schema import attribute_container_schema

model_definition_schema = {
    'type': 'object',
    'properties': {
        'persistence': {
            'type': 'string',
            'enum': [PL.name for PL in PersistenceLevel]
        },
        'records': {
            'type': 'integer'
        },
        'datastore': {
            'type': 'string'
        },
        'properties': {**model_properties_schema},
        'attributes': {**attribute_container_schema}
    },
    'required': ['attributes'],
    'additionalProperties': False
}
