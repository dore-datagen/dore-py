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
Datastore Container
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import ItemsView
    from dore.protocol import Datastore

class DatastoreContainer:

    container: dict[str, Datastore] = None

    def __init__(self):
        self.container = {}

    def add_datastore(self, datastore_id: str, datastore: Datastore) -> None:
        self.container[datastore_id] = datastore

    def datastore(self, datastore_id: str) -> Datastore:
        return self.container[datastore_id]

    def has_datastore(self, datastore_id: str) -> bool:
        return datastore_id in self.container

    def datastore_list(self) -> ItemsView[str, Datastore]:
        return self.container.items()
