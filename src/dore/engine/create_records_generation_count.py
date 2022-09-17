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
Create records generation count for model
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.config.dore_config import DoreConfig

SCALE_FACTOR_APPLICATION_THRESHOLD = 10000

def create_records_generation_count(model: Model, config: DoreConfig) -> int:
    """
    Create records generation count for model
    """
    scale_factor = config.scale_factor()
    records_to_generate_for_model = model.get_records_to_generate()
    if records_to_generate_for_model >= SCALE_FACTOR_APPLICATION_THRESHOLD:
        return int(records_to_generate_for_model * scale_factor)

    return records_to_generate_for_model
