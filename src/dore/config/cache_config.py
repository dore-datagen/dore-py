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
Cache config class
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.config.cli_args import CliArgs

from dore.cache.cache_type import CacheType
from dore.config.redis_config import RedisConfig

class CacheConfig:

    _cache_type: CacheType = None
    _redis_config: RedisConfig = None

    def __init__(self, cli_args: CliArgs):
        cache_type_in_cli_args = cli_args.dore_args().cache
        if cache_type_in_cli_args is not None:
            self._cache_type = CacheType.get(cli_args.dore_args().cache)

        self._redis_config = RedisConfig(cli_args)

    def cache_type(self) -> CacheType:
        return self._cache_type

    def redis_config(self) -> RedisConfig:
        return self._redis_config
