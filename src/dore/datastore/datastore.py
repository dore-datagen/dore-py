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

from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dore.model.model import Model
    from dore.protocol.batched_writer import BatchedWriter
    from dore.datastore.config.datastore_config import DatastoreConfig

from abc import ABC, abstractmethod
from dore.cache.cache_factory import cache_factory

class Datastore(ABC):
    """
    Abstract class representing a datastore. All protocol specific datastores must
    inherit this class.
    """

    _id = None
    _config: DatastoreConfig = None

    def __init__(self, datastore_config: DatastoreConfig):
        self._id = datastore_config.id()
        self._config = datastore_config

    def id(self) -> str:
        """
        Get datastore id
        """
        return self._id

    def config(self) -> DatastoreConfig:
        """
        Get datastore config
        """
        return self._config

    @abstractmethod
    def create(self) -> None:
        """
        Create datastore in underlying database system.
        """

    @abstractmethod
    def exists(self) -> bool:
        """
        Checks if datastore exists in underlying database system.
        :return: True if datastore exists, False otherwise
        """

    @abstractmethod
    def create_model(self, model: Model) -> None:
        """
        Creates a model in the underlying database system.

        :param model: Model to be cretaed
        """

    @abstractmethod
    def delete_model(self, model: Model) -> None:
        """
        Deletes a model from the underlying database system

        :param model: Model to be deleted
        """

    @abstractmethod
    def model_exists(self, model: Model) -> bool:
        """
        Checks if model exists in the underlying database system

        :param model: model whose existence is to be checked
        :return: True if model exists, False otherwse
        """

    @abstractmethod
    def all_records_for_model(self, model: Model) -> list[dict]:
        """
        Gets all records for a model

        :param model: Model for which records are to be extracted.
        :return: List of all records for the model.
        """

    @abstractmethod
    def get_batched_writer(self, model: Model) -> BatchedWriter:
        """
        Create and return a batched writer.

        :param model: Model for which record is to be inserted.
        """


    def record_for_model(self, model: Model, criteria: dict = None) -> dict:
        """
        Get a record from model based on criteria.
        If no criteria is provided, retrieve a random record for the model
        """
        cache = cache_factory()
        return cache.get_random_elem_from_list(model.config().id())
