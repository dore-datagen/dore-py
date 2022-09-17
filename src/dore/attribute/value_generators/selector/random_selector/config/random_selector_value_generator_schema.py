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
Random Selector Value Generator schema
"""

random_selector_value_generator_schema = {
    'type': 'object',
    'properties': {
        'random': {
            'type': 'object',
            'properties': {
                'items': {
                    'type': 'array',
                    'items': {
                        'oneOf': [
                            {
                                'type': 'string'
                            },
                            {
                                'type': 'number'
                            },
                            {
                                'type': 'object'
                            },
                        ]
                    }
                }
            },
            'required': ['items'],
            'additionalProperties': False,
        },
    },
    'required': ['random'],
    'additionalProperties': False,
}
