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
Selector Value Generator schema
"""

from dore.attribute.value_generators.value_generator_type import ValueGeneratorType
from dore.attribute.value_generators.selector.random_selector.config.random_selector_value_generator_schema \
    import random_selector_value_generator_schema
from dore.attribute.value_generators.selector.round_robin_selector.config.round_robin_selector_value_generator_schema \
    import round_robin_selector_value_generator_schema

selector_value_generator_schema = {
    'type': 'object',
    'properties': {
        ValueGeneratorType.SELECTOR.schema_key(): {
            'type': 'object',
            'oneOf': [
                random_selector_value_generator_schema,
                round_robin_selector_value_generator_schema
            ]
        }
    },
    'required': [ValueGeneratorType.SELECTOR.schema_key()],
    'additonalProperties': False
}
