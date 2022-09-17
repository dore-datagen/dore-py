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

import os
from dore.utils.rand.rand_utils import RandUtils
from dore.config.dore_config import BIDI_RNG_SEED_VAR

INSTANCE: RandUtils = None

def rand_utils_factory() -> RandUtils:
    # pylint: disable=W0603
    global INSTANCE

    if INSTANCE is None:
        seed = int(os.environ[BIDI_RNG_SEED_VAR])
        INSTANCE = RandUtils(seed)

    return INSTANCE
