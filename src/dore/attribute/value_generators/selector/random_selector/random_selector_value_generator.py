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
Random Selector Value Generator
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.attribute.value_generators.selector.random_selector.config.random_selector_value_generator_config \
        import RandomSelectorValueGeneratorConfig

from dore.utils.rand.rand_utils_factory import rand_utils_factory
from dore.attribute.value_generators.i_attribute_value_generator import IAttributeValueGenerator

class RandomSelectorValueGenerator(IAttributeValueGenerator):

    config: RandomSelectorValueGeneratorConfig = None
    values_list_len: int = None

    def __init__(self, config: RandomSelectorValueGeneratorConfig):
        super().__init__()
        self.config = config
        self.values_list_len = len(self.config.values())


    def generate_value(self) -> object:
        random_idx = rand_utils_factory().rand_int(0, self.values_list_len - 1)
        return self.config.values()[random_idx]
