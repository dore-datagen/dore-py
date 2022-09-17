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
Value Generator Factory
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.attribute.attribute import Attribute
    from dore.context.dore_context import DoreContext

from dore.exceptions.invalid_manifest_exception import InvalidManifestException
from dore.attribute.value_generators.faker.faker_value_generator \
    import FakerValueGenerator
from dore.attribute.value_generators.faker.config.faker_value_generator_config \
    import FakerValueGeneratorConfig
from dore.attribute.value_generators.selector.selector_value_generator \
    import SelectorValueGenerator
from dore.attribute.value_generators.composite.config.composite_value_generator_config \
    import CompositeValueGeneratorConfig
from dore.attribute.value_generators.composite.composite_value_generator \
    import CompositeValueGenerator

from dore.attribute.value_generators.selector.config.selector_value_generator_config \
    import SelectorValueGeneratorConfig
from dore.attribute.value_generators.ref.ref_value_generator import RefValueGenerator
from dore.attribute.value_generators.ref.config.ref_value_generator_config import RefValueGeneratorConfig
from dore.attribute.value_generators.i_attribute_value_generator import IAttributeValueGenerator
from dore.attribute.value_generators.value_generator_type import ValueGeneratorType

def value_generator_factory(attribute: Attribute,
                            context: DoreContext = None) -> IAttributeValueGenerator or None:
    value_generator_type = attribute.config().value_generator_type()

    if value_generator_type is ValueGeneratorType.FAKER:
        config = attribute.config().value(FakerValueGeneratorConfig)
        return FakerValueGenerator(config)

    if value_generator_type is ValueGeneratorType.SELECTOR:
        attribute_config = attribute.config().value(SelectorValueGeneratorConfig)
        return SelectorValueGenerator(attribute_config)


    if value_generator_type is ValueGeneratorType.REF:
        attribute_config = attribute.config().value(RefValueGeneratorConfig)
        return RefValueGenerator(attribute_config, context)

    if value_generator_type is ValueGeneratorType.COMPOSITE:
        attribute_config = attribute.config().value(CompositeValueGeneratorConfig)
        return CompositeValueGenerator(attribute_config, context)

    raise InvalidManifestException(f'invalid value generator type [{value_generator_type}] '
                                     f'in config [{attribute.config().id()}]')
