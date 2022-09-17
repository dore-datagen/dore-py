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
ElasticSearch Model Properties config class
"""

from jsonschema import validate

from dore.protocol.elasticsearch.config.elasticsearch_model_properties_schema \
    import elasticsearch_model_properties_schema

class ElasticSearchModelPropertiesConfig:

    _index_name: str = None

    def __init__(self, model_properties_config: dict):
        validate(model_properties_config, elasticsearch_model_properties_schema)
        self._index_name = model_properties_config['indexName']

    def index_name(self) -> str:
        """
        Get ElasticSearch index name for model
        """
        return self._index_name
