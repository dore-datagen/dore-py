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
Model class
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.config.model_config import ModelConfig
    from dore.attribute.attribute_container import AttributeContainer

from dore.attribute.attribute_container_factory import attribute_container_factory

LOGGER = logging.getLogger(__name__)

class Model:
    """
    Model Class
    """

    _config: ModelConfig = None
    _attribute_container: AttributeContainer = None

    def __init__(self, config: ModelConfig):
        self._config = config
        self._attribute_container = attribute_container_factory(self._config.attribute_container_config())

    def config(self) -> ModelConfig:
        """
        Get model config
        """
        return self._config

    def attribute_container(self) -> AttributeContainer:
        """
        Get attribute container for model
        """
        return self._attribute_container

    def get_records_to_generate(self) -> int:
        """
        Get count of records to generate for the model.
        """
        return self._config.records()


    def generate_record(self) -> dict:
        """
        Generate a record for the model.

        :return: Dictionary of values where keys are attribute ids and
        values are generated values.
        """
        record = {}
        for attribute_id, attribute in self.attribute_container().attributes():
            generated_value = attribute.value_generator().generate_value()
            record[attribute_id] = generated_value

        return record
