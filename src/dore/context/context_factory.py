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
Context factory
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.config import DoreConfig

from dore.cache.cache_factory import cache_factory
from dore.context.dore_context import DoreContext
from dore.manifest.manifest_factory import manifest_factory
from dore.model.model_container_factory import model_container_factory
from dore.datastore.datastore_container_factory import datastore_container_factory

CONTEXT_INSTANCE: DoreContext = None

def context_factory(dore_config: DoreConfig) -> DoreContext:

    global CONTEXT_INSTANCE

    # initialize only once
    if CONTEXT_INSTANCE is None:

        # create and initialize cache
        cache = cache_factory(dore_config.cache_config())

        # create manifest
        manifest = manifest_factory(dore_config.manifest_config())

        # create datastore container
        datastore_container = datastore_container_factory(manifest.datastore_container_config())

        # create model container
        model_container = model_container_factory(manifest.model_container_config())

        # save global context
        CONTEXT_INSTANCE = DoreContext(
            cache=cache,
            model_container=model_container,
            datastore_container=datastore_container
        )

    return CONTEXT_INSTANCE
