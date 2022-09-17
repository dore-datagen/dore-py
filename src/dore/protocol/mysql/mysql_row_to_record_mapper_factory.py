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
Build response mapper for mysql rows
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable

def mysql_row_to_record_mapper_factory(
        columns: list[str],
        column_name_attribute_id_map: dict[str, str]
) -> Callable[[tuple[object]], dict]:

    def mysql_row_to_record_mapper(row: tuple[object]) -> dict:
        record = {}
        col_idx = 0
        for column_value in row:
            col_name = columns[col_idx]
            attribute_id = column_name_attribute_id_map[col_name]
            record[attribute_id] = column_value
            col_idx += 1
        return record

    return mysql_row_to_record_mapper
