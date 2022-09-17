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
Manifest schema.
"""

from dore.model.config.model_container_schema import model_container_schema
from dore.datastore.config.datastore_container_schema import datastore_container_schema

manifest_schema = {
    'type': 'object',
    'properties': {
        'id': {
            'type': 'string',
            'required': True
        },
        'datastores': {**datastore_container_schema},
        'models': {**model_container_schema},
    },
    'additionalProperties': False,
    'required': ['id', 'models', 'datastores']
}
