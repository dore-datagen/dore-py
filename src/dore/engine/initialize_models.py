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
Initialize models
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.config.dore_config import DoreConfig
    from dore.context.dore_context import DoreContext

from dore.model.config.persistence_level import PersistenceLevel
from dore.exceptions.model_conflict_exception import ModelConflictException

def initialize_models(config: DoreConfig, context: DoreContext):
    """
    Initialize models
    """

    model_container = context.model_container()
    datastore_container = context.datastore_container()

    for _, model in model_container.models():
        if model.config().persistence() is PersistenceLevel.FULL:
            datastore = datastore_container.datastore(model.config().datastore_id())
            if datastore.model_exists(model):
                if config.drop_conflicting_models():
                    datastore.delete_model(model)

                else:
                    raise ModelConflictException(model.config().id(), datastore.id())

            datastore.create_model(model)
