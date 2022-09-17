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
Datastores Container factory
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.datastore.config.datastore_container_config import DatastoreContainerConfig

from dore.datastore.datastore_factory import datastore_factory
from dore.datastore.datastore_container import DatastoreContainer
from dore.datastore.config.datastore_container_config import DatastoreContainerConfig

def datastore_container_factory(datastore_container_config: DatastoreContainerConfig) -> DatastoreContainer:

    datastore_container = DatastoreContainer()

    for datastore_id, datastore_config in datastore_container_config.datastore_config_list():
        datastore = datastore_factory(datastore_config)
        datastore_container.add_datastore(datastore_id, datastore)

    return datastore_container
