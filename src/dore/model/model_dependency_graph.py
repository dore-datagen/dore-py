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
Wrapper around Graph class for working with Models.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.utils.graph.graph import Graph

from dore.utils.graph.graph_factory import graph_factory

class ModelDependencyGraph:

    graph: Graph = None
    node_model_map: dict[str, Model] = None

    def __init__(self):
        self.graph = graph_factory()
        self.node_model_map = {}

    def add_model(self, model: Model):
        self.graph.add_node(model.config().id())
        if model.config().id() not in self.node_model_map:
            self.node_model_map[model.config().id()] = model

    def add_dependency(self, from_model: Model, to_model: Model):
        self.graph.add_edge(from_model.config().id(), to_model.config().id())

    def topologically_sorted_models(self):
        topologically_sorted_models = list(
            map(
                lambda node_id: self.node_model_map[node_id],
                self.graph.topologically_sort_vertices()
            )
        )

        return topologically_sorted_models

    def model_has_dependent_models(self, model: Model):
        return self.graph.node_indegree(model.config().id()) > 0
