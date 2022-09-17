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
Resolve manifest by reading referenced files (if any) and substitute
variables in manifest with provided values.
"""

import json
import pystache
from dore.utils.file.read_file_as_json import read_file_as_json

def __resolve_variables__(dictionary, variables):
    return json.loads(
        pystache.render(
            pystache.parse(json.dumps(dictionary)),
            variables))


def resolve_manifest(manifest_json: dict, manifest_vars: dict) -> dict:
    # Create a deep copy of the original manifest_json dict
    resolved_manifest = json.loads(json.dumps(manifest_json))

    # substitute variables after manifest file is loaded
    resolved_manifest = __resolve_variables__(resolved_manifest, manifest_vars)

    # Resolve linked model files
    for model_id in resolved_manifest['models']:
        model_definition = resolved_manifest['models'][model_id]
        if 'ref' in model_definition:
            model_definition_file = model_definition['ref']
            model_definition_dict = read_file_as_json(model_definition_file)
            resolved_manifest['models'][model_id] = model_definition_dict

    # substitute variables after model files are loaded
    resolved_manifest = __resolve_variables__(resolved_manifest, manifest_vars)

    # Resolve linked attribute files
    for model_id in resolved_manifest['models']:
        model_definition = resolved_manifest['models'][model_id]
        for attribute_id in model_definition['attributes']:
            attribute_definition = model_definition['attributes'][attribute_id]
            if 'ref' in attribute_definition:
                attribute_definition_file = attribute_definition['ref']
                attribute_definition_dict = read_file_as_json(attribute_definition_file)
                model_definition['attributes'][attribute_id] = attribute_definition_dict

    # substitute variables after attribute files are loaded
    resolved_manifest = __resolve_variables__(resolved_manifest, manifest_vars)

    # Resolve linked datastore files
    for datastore_id in resolved_manifest['datastores']:
        datastore_definition = resolved_manifest['datastores'][datastore_id]
        if 'ref' in datastore_definition:
            datastore_definition_file = datastore_definition['ref']
            datastore_definition_dict = read_file_as_json(datastore_definition_file)
            resolved_manifest['datastores'][datastore_id] = datastore_definition_dict

    # substitute variables once all files are loaded
    resolved_manifest = __resolve_variables__(resolved_manifest, manifest_vars)

    return resolved_manifest
