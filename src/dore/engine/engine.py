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
Dore engine
"""

from __future__ import annotations
import logging
import cProfile

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.datastore.datastore import Datastore
    from dore.protocol.batched_writer import BatchedWriter

from tqdm import tqdm

from dore.engine.bootstrap import bootstrap
from dore.model.config.persistence_level import PersistenceLevel
from dore.engine.create_profile_filename import create_profile_filename
from dore.engine.create_records_generation_count import create_records_generation_count

# Constants
LOGGER = logging.getLogger(__name__)

def run(config, context):
    """
    Dore engine
    """

    cache = context.cache()

    for model in context.model_dependency_graph().topologically_sorted_models():
        if model.config().persistence() is PersistenceLevel.FULL:
            LOGGER.info('generating records for model [%s]', model.config().id())

            datastore: Datastore = context.datastore_container().datastore(model.config().datastore_id())
            batched_writer: BatchedWriter = datastore.get_batched_writer(model)
            records_to_generate = create_records_generation_count(model, config)

            for _ in tqdm(range(records_to_generate), ncols=85):
                record = model.generate_record()
                batched_writer.write(record)

            batched_writer.flush()

            LOGGER.info('[%s] records generated for model [%s]', records_to_generate, model.config().id())

            # if this model has other models dependent on it, add the model's records to cache
            if context.model_dependency_graph().model_has_dependent_models(model):
                LOGGER.info('populating cache with records for [%s]', model.config().id())
                for record in datastore.all_records_for_model(model):
                    cache.add_to_list_batched(
                        key=model.config().id(),
                        value=record
                    )

            cache.flush()

        elif model.config().persistence() is PersistenceLevel.MEMORY_ONLY:
            LOGGER.info('generating records for model [%s]', model.config().id())
            records_to_generate = create_records_generation_count(model, config)

            for _ in tqdm(range(records_to_generate), ncols=85):
                record = model.generate_record()
                cache.add_to_list_batched(
                    key=model.config().id(),
                    value=record
                )

            cache.flush()

    LOGGER.info('Clearing cache')
    cache.clear()

def engine():
    config, context = bootstrap()
    if config.profile():
        with cProfile.Profile() as profile:
            LOGGER.info('running with profiling enabled')

            profile_filename = create_profile_filename()
            run(config, context)
            profile.dump_stats(file=profile_filename)

            LOGGER.info('profile output is present at [%s]', profile_filename)
            LOGGER.info('You can now run [snakeviz %s] to view an interfactive profile viz', profile_filename)

    else:
        run(config, context)
