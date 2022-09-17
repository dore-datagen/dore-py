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
Dependent Attribute Value Generator
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.context.dore_context import DoreContext

from abc import abstractmethod

from dore.attribute.attribute_value_generator import AttributeValueGenerator

class DAttributeValueGenerator(AttributeValueGenerator):

    _context: DoreContext = None

    def __init__(
            self,
            context: DoreContext,
    ):
        super().__init__()
        self._context = context

    def context(self):
        return self._context

    @abstractmethod
    def generate_value(self) -> object:
        pass
