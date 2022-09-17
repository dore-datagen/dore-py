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
Ref Value Generator
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.context.dore_context import DoreContext
    from dore.attribute.value_generators.dependency import Dependency

from dore.cache.cache_factory import cache_factory
from dore.attribute.value_generators.d_attribute_value_generator import DAttributeValueGenerator
from dore.attribute.value_generators.ref.config.ref_value_generator_config import RefValueGeneratorConfig

class RefValueGenerator(DAttributeValueGenerator):
    """
    Dependent Attribute Value Generator Type `ref`.
    """
    config: RefValueGeneratorConfig = None

    def __init__(
            self,
            config: RefValueGeneratorConfig,
            context: DoreContext,
    ):
        super().__init__(context)
        self.config = config

    def generate_value(self) -> object:
        dependency = self.config.dependency()
        dependent_model_record = cache_factory() \
            .get_random_elem_from_list(dependency.model_id())
        return dependent_model_record[dependency.attribute_id()]

    def dependencies(self) -> list[Dependency]:
        return [self.config.dependency()]
