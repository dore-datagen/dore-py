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
Selector Value Generator
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.attribute.value_generators.selector.config.selector_value_generator_config \
        import SelectorValueGeneratorConfig

from dore.attribute.value_generators.selector.config.selector_type import SelectorType
from dore.attribute.value_generators.i_attribute_value_generator import IAttributeValueGenerator
from dore.attribute.value_generators.selector.random_selector.random_selector_value_generator \
    import RandomSelectorValueGenerator
from dore.attribute.value_generators.selector.random_selector.config.random_selector_value_generator_config \
    import RandomSelectorValueGeneratorConfig
from dore.attribute.value_generators.selector.round_robin_selector.round_robin_selector_value_generator \
    import RoundRobinSelectorValueGenerator
from dore.attribute.value_generators.selector.round_robin_selector.config.round_robin_selector_value_generator_config \
    import RoundRobinSelectorValueGeneratorConfig

class SelectorValueGenerator(IAttributeValueGenerator):

    config: SelectorValueGeneratorConfig = None
    selector: IAttributeValueGenerator = None

    def __init__(self, config: SelectorValueGeneratorConfig):
        super().__init__()
        self.config = config

        if self.config.type() is SelectorType.RANDOM:
            selector_config = self.config.config(RandomSelectorValueGeneratorConfig)
            self.selector = RandomSelectorValueGenerator(selector_config)

        elif self.config.type() is SelectorType.ROUNDROBIN:
            selector_config = self.config.config(RoundRobinSelectorValueGeneratorConfig)
            self.selector = RoundRobinSelectorValueGenerator(selector_config)

        else:
            print('we are here')


    def generate_value(self) -> dict:
        return self.selector.generate_value()
