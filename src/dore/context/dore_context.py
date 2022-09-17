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
Dore Context
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.cache.cache import Cache
    from dore.model.model_container import ModelContainer
    from dore.datastore.datastore_container import DatastoreContainer
    from dore.model.model_dependency_graph import ModelDependencyGraph

class DoreContext:

    _cache: Cache = None
    _model_container: ModelContainer = None
    _datastore_container: DatastoreContainer = None

    # This is set explicitly after the dependencies are initialized.
    _model_dependency_graph: ModelDependencyGraph = None

    def __init__(self,
                 cache: Cache,
                 model_container: ModelContainer,
                 datastore_container: DatastoreContainer):
        self._cache = cache
        self._model_container = model_container
        self._datastore_container = datastore_container

    def cache(self) -> Cache:
        """
        Get application cache from context
        """
        return self._cache

    def model_container(self):
        """
        Get model container from context
        """
        return self._model_container

    def datastore_container(self) -> DatastoreContainer:
        """
        Get datastore container from context
        """
        return self._datastore_container

    def set_model_dependency_graph(self, model_dependency_graph: ModelDependencyGraph) -> None:
        """
        Set model dependency graph in context
        """
        self._model_dependency_graph = model_dependency_graph

    def model_dependency_graph(self) -> ModelDependencyGraph:
        """
        Get model dependency graph
        """
        return self._model_dependency_graph
