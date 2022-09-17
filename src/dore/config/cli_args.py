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
Class for parsing and accessing cli args
"""

import re
import os
import logging
import argparse

LOGGER = logging.getLogger(__name__)
MANIFEST_CLI_ARG_REGEX = re.compile(''.join([
    '--',  # prefix
    '(?P<name>[^=]+)'  # variable name
    '='  # separator
    '(?P<value>[^=]+)',  # variable value
]))

def parse_manifest_arg(cli_manifest_arg) -> dict:
    matched_data = re.match(MANIFEST_CLI_ARG_REGEX, cli_manifest_arg)

    # if no matches were found
    if matched_data is None:
        LOGGER.error('error while parsing manifest args from cli args')
        raise Exception(f'invalid cli arg [{cli_manifest_arg}] passed')

    matched_data_dict = matched_data.groupdict()

    # if both name and value were not parsed
    if not (matched_data_dict['name'] and matched_data_dict['value']):
        LOGGER.error('error while parsing manifest args from cli args')
        raise Exception(f'invalid cli arg [{cli_manifest_arg}] passed')

    # convert it into a dict
    return matched_data_dict

def parse_manifest_args(cli_manifest_args_list) -> dict:
    manifest_args = {}
    for cli_manifest_arg in cli_manifest_args_list:
        name_value_dict = parse_manifest_arg(cli_manifest_arg)
        manifest_args[name_value_dict['name']] = name_value_dict['value']

    return manifest_args

class CliArgs:

    _dore_args: argparse.Namespace = None
    _manifest_vars: dict = None

    def __init__(self):
        parser = argparse.ArgumentParser(description='DorePy: Your smart fake data generator')

        parser.add_argument('--manifest',
                            help='Absolute path to manifest file',
                            type=str,
                            required=True)
        parser.add_argument('--scale-factor',
                            help='Scale factor for records to be generated',
                            type=float,
                            default=1,
                            required=False)
        parser.add_argument('--cache',
                            help='Cache mode (redis|local). Defaults to local',
                            type=str,
                            required=False)
        parser.add_argument('--redis-host',
                            help='Redis host (required when -c|--cache is redis)',
                            type=str,
                            required=False)
        parser.add_argument('--redis-port',
                            help='Redis port (required when -c|--cache is redis)',
                            type=int,
                            required=False)
        parser.add_argument('--profile',
                            help='Run with profiling. Output is generated in \'dore-run.prof\' file',
                            action='store_true')
        parser.add_argument('--drop-conflicting-models',
                            help='Drop existing models with the same name in the datastore',
                            action='store_true')
        parser.add_argument('--seed',
                            help='Seed for all random value generations',
                            type=int,
                            required=False)

        parsed_args = parser.parse_known_args()

        self._dore_args = parsed_args[0]

        # check for existence of manifest args
        if len(parsed_args) > 1:
            cli_manifest_args_list = parsed_args[1]
            self._manifest_vars = parse_manifest_args(cli_manifest_args_list)

    def dore_args(self) -> argparse.Namespace:
        return self._dore_args

    def manifest_vars(self) -> dict:
        return self._manifest_vars
