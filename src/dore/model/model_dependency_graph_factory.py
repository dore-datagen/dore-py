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
Model dependency graph factory
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model_container import ModelContainer

from dore.model.model_dependency_graph import ModelDependencyGraph
from dore.exceptions.invalid_manifest_exception import InvalidManifestException

def model_dependency_graph_factory(model_container: ModelContainer) -> ModelDependencyGraph:
    model_dependency_graph = ModelDependencyGraph()

    for _, model in model_container.models():
        model_dependency_graph.add_model(model)
        for _, attribute in model.attribute_container().attributes():
            if attribute.config().is_dependent_attribute():
                for dependency in attribute.value_generator().dependencies():
                    # get dependent model
                    try:
                        referenced_model = model_container.model(dependency.model_id())
                    except KeyError:
                        raise InvalidManifestException(f'invalid reference [{dependency.model_id()}] '
                                                       f'in model [{model.config().id()}]') from KeyError

                    # add dependent model model to the graph
                    model_dependency_graph.add_model(referenced_model)
                    # add an edge from current model to dependent model
                    model_dependency_graph.add_dependency(model, referenced_model)

    return model_dependency_graph
