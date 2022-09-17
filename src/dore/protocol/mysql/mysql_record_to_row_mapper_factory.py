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
Build request mapper for mysql records
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Callable

def mysql_record_to_row_mapper_factory(
        attribute_id_order_list: list[str]
) -> Callable[[dict], tuple]:

    def mysql_record_to_row_mapper(record: dict) -> tuple:
        row = ()
        for attribute_id in attribute_id_order_list:
            column_value = record[attribute_id]
            row = row + (column_value,)
        return row

    return mysql_record_to_row_mapper
