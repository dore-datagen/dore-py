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
Model Container class
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import ItemsView
    from dore.model.model import Model
    from dore.model.model_dependency_graph import ModelDependencyGraph

class ModelContainer:

    container: dict[str, Model] = None
    dependency_graph: ModelDependencyGraph = None

    def __init__(self):
        self.container = {}

    def add_model(self, model_id: str, model: Model) -> None:
        self.container[model_id] = model

    def has_model(self, model_id: str) -> bool:
        return model_id in self.container

    def model(self, model_id: str) -> Model:
        return self.container[model_id]

    def models(self) -> ItemsView[str, Model]:
        """
        Iterator over models in the container based on topological ordering
        """
        return self.container.items()
