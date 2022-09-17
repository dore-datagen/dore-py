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
Generic Graph class
"""

from collections import deque

from dore.exceptions.invalid_manifest_exception import InvalidManifestException

class Graph:
    graph = None

    def __init__(self):
        self.graph = {}

    def add_node(self, node_id: str):
        if node_id not in self.graph:
            self.graph[node_id] = []

    def add_edge(self, src_node_id, dst_node_id):
        if src_node_id not in self.graph:
            self.add_node(src_node_id)

        if dst_node_id not in self.graph:
            self.add_node(dst_node_id)

        self.graph[src_node_id].append(dst_node_id)

    def node_indegree(self, node_id):
        indegree = 0
        for _id in self.graph:
            node_adj_list = self.graph[_id]
            if node_id in node_adj_list:
                indegree += 1

        return indegree



    def is_cyclic(self):
        visited = 'VISITED'
        discovered = 'DISCOVERED'
        not_discovered = 'NOT_DISCOVERED'
        visited_map = {}

        for node_id in self.graph.keys():
            visited_map[node_id] = not_discovered

        def is_cyclic_util(_node_id: str) -> bool:
            visited_map[_node_id] = discovered
            for adjacent_node_id in self.graph[_node_id]:
                if visited_map[adjacent_node_id] == discovered:
                    return True

                if visited_map[adjacent_node_id] == not_discovered:
                    _has_cycles = is_cyclic_util(adjacent_node_id)
                    if _has_cycles:
                        return True

            visited_map[_node_id] = visited
            return False

        for node_id in self.graph:
            if visited_map[node_id] == not_discovered:
                has_cycles = is_cyclic_util(node_id)
                if has_cycles:
                    return True

        return False

    def topologically_sort_vertices(self):
        if self.is_cyclic():
            raise InvalidManifestException('There are cycles in model dependencies')

        visited = 'VISITED'
        discovered = 'DISCOVERED'
        not_discovered = 'NOT_DISCOVERED'
        visited_map = {}

        for node_id in self.graph:
            visited_map[node_id] = not_discovered

        topologically_sorted_vertices = deque()

        def topological_sort_util(_node_id: str) -> None:
            visited_map[_node_id] = discovered
            for adjacent_node_id in self.graph[_node_id]:
                if visited_map[adjacent_node_id] == not_discovered:
                    topological_sort_util(adjacent_node_id)

            visited_map[_node_id] = visited
            topologically_sorted_vertices.append(_node_id)


        for node_id in self.graph:
            if visited_map[node_id] == not_discovered:
                topological_sort_util(node_id)

        return list(topologically_sorted_vertices)
