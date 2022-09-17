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
Ref Value Generator config class
"""

from dore.attribute.value_generators.dependency import Dependency

class RefValueGeneratorConfig:
    """
    Config class for Ref Value Generator
    """

    _dependency: Dependency = None

    def __init__(self, config: dict):
        self._dependency = Dependency(config['ref'])

    def dependency(self) -> Dependency:
        return self._dependency
