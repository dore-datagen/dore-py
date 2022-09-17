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
Create or return the global cache instance.
Creation happens only once.
"""

from __future__ import annotations
import logging

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.cache.cache import Cache
    from dore.config.cache_config import CacheConfig

from dore.cache.cache_type import CacheType
from dore.cache.redis.redis_cache import RedisCache
from dore.cache.pydict.pydict_cache import PydictCache
from dore.exceptions.invalid_manifest_exception import InvalidManifestException

LOGGER = logging.getLogger(__name__)

# global cache instance
CACHE_INSTANCE = None

def cache_factory(cache_config: CacheConfig = None) -> Cache:
    # pylint: disable=W0603
    global CACHE_INSTANCE

    # initialize only once
    if CACHE_INSTANCE is None:

        required_cache_type = cache_config.cache_type()

        if required_cache_type is None:
            required_cache_type = CacheType.default()

        if required_cache_type is CacheType.LOCAL:
            CACHE_INSTANCE = PydictCache()

        elif required_cache_type == CacheType.REDIS:
            CACHE_INSTANCE = RedisCache(
                cache_config.redis_config().host(),
                cache_config.redis_config().port()
            )

        else:
            raise InvalidManifestException(f'invalid cache_type [{required_cache_type}]')

        LOGGER.info('using cache type [%s]', required_cache_type)

    return CACHE_INSTANCE
