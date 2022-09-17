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
Composite Value Generator
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.context.dore_context import DoreContext
    from dore.attribute.value_generators.dependency import Dependency

from dore.cache.cache_factory import cache_factory
from dore.model.config.persistence_level import PersistenceLevel
from dore.attribute.value_generators.d_attribute_value_generator import DAttributeValueGenerator
from dore.attribute.value_generators.composite.config.composite_value_generator_config import CompositeValueGeneratorConfig

class CompositeValueGenerator(DAttributeValueGenerator):
    """
    Composite Value Generator
    """

    config: CompositeValueGeneratorConfig = None

    def __init__(
            self,
            config: CompositeValueGeneratorConfig,
            context: DoreContext
    ):
        super().__init__(context)
        self.config = config

    def dependencies(self) -> list[Dependency]:
        return [self.config.dependency()]

    def generate_value(self) -> object:
        dependent_model_id = self.config.dependency().model_id()
        dependent_model = self.context().model_container().model(dependent_model_id)

        # get value from datastore
        if dependent_model.config().persistence() is PersistenceLevel.FULL:
            datastore_id = dependent_model.config().datastore_id()
            datastore = self.context().datastore_container().datastore(datastore_id)
            return datastore.record_for_model(dependent_model)

        # get value from cache
        elif dependent_model.config().persistence() is PersistenceLevel.MEMORY_ONLY:
            cache = cache_factory()
            return cache.get_random_elem_from_list(dependent_model.config().id())

        else:
            return dependent_model.generate_record()
