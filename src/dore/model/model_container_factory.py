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
Model Container factory
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.config.model_container_config import ModelContainerConfig

from dore.model.model_factory import model_factory
from dore.model.model_container import ModelContainer

LOGGER = logging.getLogger(__name__)

def model_container_factory(
        model_container_config: ModelContainerConfig
) -> ModelContainer:

    model_container = ModelContainer()

    for model_id, model_config in model_container_config.model_config_list():
        model = model_factory(model_config)
        model_container.add_model(model_id, model)

    return model_container
