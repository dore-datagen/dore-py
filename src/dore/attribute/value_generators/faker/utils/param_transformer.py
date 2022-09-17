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

import copy

from dore.utils.date import date_utils

from dore.attribute.value_generators.faker.config.faker_value_generator_config import FakerValueGeneratorConfig

def date_between(params: dict) -> dict:
    transformed_params = copy.deepcopy(params)

    if 'start_date' in params.keys():
        start_date_str = params['start_date']
        if date_utils.is_date(start_date_str):
            transformed_params['start_date'] = date_utils.parse(start_date_str)

    if 'end_date' in params.keys():
        end_date_str = params['end_date']
        if date_utils.is_date(end_date_str):
            transformed_params['end_date'] = date_utils.parse(end_date_str)

    return transformed_params

param_transformers = {
    'date_between': date_between
}

def faker_input_transformer(config: FakerValueGeneratorConfig) -> None:
    method_name = config.method_name()
    if method_name in param_transformers:
        transformer = param_transformers[method_name]
        config.set_method_params(transformer(config.method_params()))
