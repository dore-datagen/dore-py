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
Dependency class
"""

SEPARATOR = '.'

class Dependency:

    _model_id: str = None
    _attribute_id: str = None

    def __init__(self, ref_str: str):
        # String has model.attribute reference
        if SEPARATOR in ref_str:
            self._model_id = ref_str.split('.')[0].strip()
            self._attribute_id = ref_str.split('.')[1].strip()

        # String has model reference
        else:
            self._model_id = ref_str.strip()


    def model_id(self) -> str:
        return self._model_id

    def attribute_id(self) -> str:
        return self._attribute_id
