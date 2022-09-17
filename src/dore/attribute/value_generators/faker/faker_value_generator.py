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
Faker Value Generator
"""

import logging
import os
from faker import Faker
# import all standard providers
from faker.providers import address, automotive, bank, barcode, color, \
    company, credit_card, currency, date_time, file, geo, internet, isbn, \
    job, lorem, misc, person, phone_number, profile, python, ssn, user_agent

from dore.exceptions.invalid_manifest_exception import InvalidManifestException
from dore.config.dore_config import BIDI_RNG_SEED_VAR
from dore.attribute.value_generators.faker.utils.param_transformer import faker_input_transformer
from dore.attribute.value_generators.i_attribute_value_generator import IAttributeValueGenerator
from dore.attribute.value_generators.faker.config.faker_value_generator_config import FakerValueGeneratorConfig

LOGGER = logging.getLogger(__name__)
FAKE = Faker()

# Maintain a flag to ensure that we `seed` the global FAKER instance only once.
IS_SEEDED = False



def __add_provider_util__(*providers):
    for provider in providers:
        FAKE.add_provider(provider)


__add_provider_util__(
    address,
    automotive,
    bank,
    barcode,
    color,
    company,
    credit_card,
    currency,
    date_time,
    file,
    geo,
    internet,
    isbn,
    job,
    lorem,
    misc,
    person,
    phone_number,
    profile,
    python,
    ssn,
    user_agent
)


class FakerValueGenerator(IAttributeValueGenerator):

    value_generator = None
    value_generator_params = None
    config: FakerValueGeneratorConfig = None

    def __init__(self, config: FakerValueGeneratorConfig):
        # pylint: disable=W0603
        global IS_SEEDED

        super().__init__()
        self.config = config

        if not IS_SEEDED:
            seed = int(os.environ[BIDI_RNG_SEED_VAR])
            FAKE.seed_instance(seed)
            IS_SEEDED = True

        try:
            method_name = config.method_name()
            self.value_generator = getattr(FAKE, method_name)
            faker_input_transformer(config)
            self.value_generator_params = config.method_params()


        except Exception as err:
            raise InvalidManifestException(f'error while creating value generator for config [{self.config}]') from err

    def generate_value(self) -> object:
        try:
            value = self.value_generator(**self.value_generator_params)
        except Exception as err:
            LOGGER.error('error while generating value for config [%s]', self.config, err)
            raise err

        return value
