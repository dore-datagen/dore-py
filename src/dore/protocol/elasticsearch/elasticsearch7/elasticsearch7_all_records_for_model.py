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
Get all records for model :: elasticsearch7
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.protocol.elasticsearch.elasticsearch7.elasticsearch7_datastore import ElasticSearch7Datastore

from dore.protocol.elasticsearch.config.elasticsearch_model_properties_config import ElasticSearchModelPropertiesConfig
from dore.protocol.elasticsearch.elasticsearch7.elasticsearch7_doc_to_record_mapper_factory \
    import elasticsearch7_doc_to_record_mapper_factory


def elasticsearch7_all_records_for_model(datastore: ElasticSearch7Datastore, model: Model):
    client = datastore.client()
    index_name = model.config().properties(ElasticSearchModelPropertiesConfig).index_name()

    response_mapper = elasticsearch7_doc_to_record_mapper_factory(model)

    body = {
        'query': {
            'match_all': {}
        }
    }

    response = client.search(index=index_name, body=body)
    for record in map(response_mapper, response['hits']['hits']):
        yield record
