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
Dore Config class
"""

from __future__ import annotations
import logging
import os
import random

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dore.config.cli_args import CliArgs

from dore.config.cache_config import CacheConfig
from dore.config.manifest_config import ManifestConfig

BIDI_RNG_SEED_VAR = 'BIDI_RNG_SEED'
BIDI_RNG_SEED_LOW = -4294967296  # -2^32
BIDI_RNG_SEED_HIGH = 2147483648  # 2^31
LOGGER = logging.getLogger(__name__)


class DoreConfig:
    _cli_args: CliArgs = None
    _cache_config: CacheConfig = None
    _manifest_config: ManifestConfig = None

    def __init__(self, cli_args: CliArgs):
        # initalize cli args
        self._cli_args = cli_args

        # initialize manifest config
        self._manifest_config = ManifestConfig(cli_args)

        # initialize redis config
        self._cache_config = CacheConfig(cli_args)

        # initialize RNG seed value as env variable
        if self._cli_args.dore_args().seed:
            dore_rng_seed = self._cli_args.dore_args().seed

        else:
            dore_rng_seed = random.randint(BIDI_RNG_SEED_LOW, BIDI_RNG_SEED_HIGH)

        LOGGER.info('executing with seed [%d]', dore_rng_seed)

        os.environ[BIDI_RNG_SEED_VAR] = str(dore_rng_seed)

    def profile(self) -> bool:
        """
        Get profile boolean flag
        """
        return self._cli_args.dore_args().profile

    def scale_factor(self) -> float:
        """
        Get scale factor for record generation counts
        """
        return self._cli_args.dore_args().scale_factor

    def cache_mode(self) -> str:
        """
        Get Cache mode
        """
        return self._cli_args.dore_args().cache

    def manifest_config(self) -> ManifestConfig:
        """
        Get Manifest config
        """
        return self._manifest_config

    def cache_config(self) -> CacheConfig:
        """
        Get redis config
        """
        return self._cache_config

    def drop_conflicting_models(self) -> bool:
        """
        Strategy for handling scenarios where models with same name exist in store
        """
        return self._cli_args.dore_args().drop_conflicting_models

    def seed(self) -> int:
        """
        Get seed value for random generators
        """
        return self._cli_args.dore_args().seed
