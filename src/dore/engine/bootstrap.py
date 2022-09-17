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
Bootstrap Dore
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.config.dore_config import DoreConfig
    from dore.context.dore_context import DoreContext

from dore.config.config_factory import config_factory
from dore.context.context_factory import context_factory
from dore.engine.initialize_models import initialize_models
from dore.engine.initialize_datastores import initialize_datastores
from dore.engine.initialize_attributes import initialize_attributes
from dore.engine.initialize_model_dependencies import initialize_model_dependencies

def bootstrap() -> tuple[DoreConfig, DoreContext]:
    config = config_factory()
    context = context_factory(config)

    initialize_datastores(context)
    initialize_models(config, context)
    initialize_attributes(context)
    initialize_model_dependencies(context)

    return config, context
