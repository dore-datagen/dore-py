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
Datastore Container config class
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import ItemsView

from jsonschema import validate, ValidationError

from dore.datastore.config.datastore_config import DatastoreConfig
from dore.datastore.config.datastore_container_schema import datastore_container_schema

LOGGER = logging.getLogger(__name__)

class DatastoreContainerConfig:
    """
    Config class for Datastore container
    """

    container: dict[str, DatastoreConfig] = None

    def __init__(self, datastore_container_config: dict):
        try:
            validate(datastore_container_config, datastore_container_schema)
        except ValidationError as err:
            LOGGER.error('schema validation failed at manifest path: [datastores/%s]', '/'.join(err.absolute_path))

        self.container = {}
        for datastore_id, datastore_config in datastore_container_config.items():
            self.container[datastore_id] = DatastoreConfig(datastore_id, datastore_config)

    def has_datastore_config(self, datastore_id: str) -> bool:
        return datastore_id in self.container

    def datastore_config(self, datastore_id: str) -> DatastoreConfig:
        return self.container[datastore_id]

    def datastore_config_list(self) -> ItemsView[str, DatastoreConfig]:
        return self.container.items()
