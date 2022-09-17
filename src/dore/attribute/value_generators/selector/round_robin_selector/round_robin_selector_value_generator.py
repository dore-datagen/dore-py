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
Round Robin Selector Value Generator
"""

from dore.attribute.value_generators.i_attribute_value_generator import IAttributeValueGenerator
from dore.attribute.value_generators.selector.round_robin_selector.config.round_robin_selector_value_generator_config \
    import RoundRobinSelectorValueGeneratorConfig

class RoundRobinSelectorValueGenerator(IAttributeValueGenerator):

    counter = -1
    config: RoundRobinSelectorValueGeneratorConfig = None

    def __init__(self, config: RoundRobinSelectorValueGeneratorConfig):
        super().__init__()
        self.config = config

    def generate_value(self) -> object:
        index = (self.counter + 1) % len(self.config.values())
        self.counter = self.counter + 1
        return self.config.values()[index]
