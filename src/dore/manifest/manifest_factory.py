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
Manifest factory
"""

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.config.manifest_config import ManifestConfig

import json
import logging

from dore.manifest.manifest import Manifest
from dore.manifest.resolve_manifest import resolve_manifest
from dore.utils.file.read_file_as_string import read_file_as_string

LOGGER = logging.getLogger(__name__)

def manifest_factory(manifest_config: ManifestConfig) -> Manifest:

    # read the file
    manifest_file_str = read_file_as_string(manifest_config.file_path())

    # parse file contents to json dict
    manifest_json = json.loads(manifest_file_str)

    # resolve referenced files and variables.
    resolved_manifest = resolve_manifest(manifest_json, manifest_config.manifest_vars())

    manifest = Manifest(resolved_manifest)

    LOGGER.info('successfully loaded manifest [%s] located at [%s]', manifest.id(), manifest_config.file_path())

    return manifest
