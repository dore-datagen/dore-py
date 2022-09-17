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
Initialize attributes
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.context.dore_context import DoreContext

def initialize_attributes(context: DoreContext):
    """
    Initialize attributes
    """
    # Register all independent attribute value generators
    for _, model in context.model_container().models():
        for _, attribute in model.attribute_container().attributes():
            if not attribute.config().is_dependent_attribute():
                attribute.register_value_generator()

    # Register all dependent attribute value generators
    for _, model in context.model_container().models():
        for _, attribute in model.attribute_container().attributes():
            if attribute.config().is_dependent_attribute():
                attribute.register_value_generator(context=context)
