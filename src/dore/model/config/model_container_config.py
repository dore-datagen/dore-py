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
Model Container config class
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import ItemsView

from jsonschema import validate, ValidationError

from dore.model.config.model_config import ModelConfig
from dore.model.config.model_container_schema import model_container_schema

LOGGER = logging.getLogger(__name__)

class ModelContainerConfig:

    container: dict[str, ModelConfig] = None

    def __init__(self, model_container_config):
        try:
            validate(model_container_config, model_container_schema)
        except ValidationError as err:
            LOGGER.error('schema validation failed at manifest path: [models/%s]', '/'.join(err.absolute_path))
            raise err

        self.container = {}
        for model_id, model_config in model_container_config.items():
            self.container[model_id] = ModelConfig(model_id, model_config)

    def model_config(self, model_id: str) -> ModelConfig:
        return self.container[model_id]

    def has_model_config(self, model_id: str) -> bool:
        return model_id in self.container

    def model_config_list(self) -> ItemsView[str, ModelConfig]:
        return self.container.items()
