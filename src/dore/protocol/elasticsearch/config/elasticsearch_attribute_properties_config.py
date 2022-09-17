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
Elasticsearch Attribute Properties config class
"""

from jsonschema import validate

from dore.protocol.elasticsearch.config.elasticsearch_attribute_properties_schema \
    import elasticsearch_attribute_properties_schema

class ElasticSearchAttributePropertiesConfig:
    """
    Config class for ElasticSearch Attribute Properties.
    """

    _field_name: str = None
    _field_type: str = None

    def __init__(self, attribute_properties_config: dict):
        validate(attribute_properties_config, elasticsearch_attribute_properties_schema)
        self._field_name = attribute_properties_config['fieldName']
        self._field_type = attribute_properties_config['fieldType']

    def field_name(self) -> str:
        """
        Get ElasticSearch field name for attribute
        """
        return self._field_name

    def field_type(self) -> str:
        """
        Get ElasticSearch field type for attribute
        """
        return self._field_type
