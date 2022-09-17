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
Attribute Value schema
"""

from dore.attribute.value_generators.faker.config.faker_value_generator_schema \
    import faker_value_generator_schema
from dore.attribute.value_generators.ref.config.ref_value_generator_schema \
    import ref_value_generator_schema
from dore.attribute.value_generators.composite.config.composite_value_generator_schema \
    import composite_value_generator_schema
from dore.attribute.value_generators.selector.config.selector_value_generator_schema \
    import selector_value_generator_schema

attribute_value_schema = \
{
    'type': 'object',
    'oneOf': [
        faker_value_generator_schema,
        selector_value_generator_schema,
        ref_value_generator_schema,
        composite_value_generator_schema,
    ]
}
