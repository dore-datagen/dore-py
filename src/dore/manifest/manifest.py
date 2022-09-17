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
The Manifest class
"""

from dore.model.config.model_container_config import ModelContainerConfig
from dore.datastore.config.datastore_container_config import DatastoreContainerConfig

class Manifest:
    """
    The Manifest Class
    """

    raw = None

    _model_container_config: ModelContainerConfig = None
    _datastore_container_config: DatastoreContainerConfig = None

    def __init__(self, manifest_json: dict):
        self.raw = manifest_json
        self._model_container_config = ModelContainerConfig(self.raw['models'])
        self._datastore_container_config = DatastoreContainerConfig(self.raw['datastores'])

    def id(self):
        return self.raw['id']

    def model_container_config(self) -> ModelContainerConfig:
        return self._model_container_config

    def datastore_container_config(self) -> DatastoreContainerConfig:
        return self._datastore_container_config
