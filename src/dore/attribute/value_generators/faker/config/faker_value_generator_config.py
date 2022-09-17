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
Faker Value Generator config class
"""

from dore.attribute.value_generators.value_generator_type import ValueGeneratorType

class FakerValueGeneratorConfig:
    """
    Config Class for Faker Value Generator
    """

    _method_name: str = None
    _method_params: dict = None

    def __init__(self, config: dict):
        schema_key = ValueGeneratorType.FAKER.schema_key()
        self._method_name = list(config[schema_key].keys())[0]
        self._method_params = config[schema_key][self._method_name]

    def method_name(self) -> str:
        return self._method_name

    def method_params(self) -> dict:
        return self._method_params

    def set_method_params(self, params: dict) -> None:
        self._method_params = params
