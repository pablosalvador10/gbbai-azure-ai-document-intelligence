import os
import traceback
from typing import Any, List, Optional

import requests
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchIndexer,
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection,
    SearchIndexerSkillset,
    SemanticSearch,
    VectorSearch,
)
from dotenv import load_dotenv

from utils.ml_logging import get_logger

# Load environment variables from .env file
load_dotenv()

# Set up logger
logger = get_logger()


class AzureAISearchManager:
    """
    A manager class for handling operations related to Azure AI Search.
    """

    def __init__(self, index_name: str = None, service_endpoint: str = None):
        """
        Initializes the AzureAISearchManager with necessary configurations.

        :param index_name: The name of the index. Defaults to None.
        :param service_endpoint: The service endpoint URL. Defaults to None.
        :raises ValueError: If any of the required environment variables are not set.
        """
        try:
            self.service_endpoint = service_endpoint or os.getenv(
                "AZURE_AI_SEARCH_SERVICE_ENDPOINT"
            )
            self.index_name = index_name or os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
            self.key = os.getenv("AZURE_SEARCH_ADMIN_KEY")
            self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

            if not self.service_endpoint:
                raise ValueError(
                    "Environment variable AZURE_AI_SEARCH_SERVICE_ENDPOINT is not set."
                )
            if not self.index_name:
                raise ValueError(
                    "Environment variable AZURE_AI_SEARCH_INDEX_NAME is not set."
                )
            if not self.key:
                raise ValueError(
                    "Environment variable AZURE_SEARCH_ADMIN_KEY is not set."
                )

            self.search_client = SearchClient(
                self.service_endpoint, self.index_name, AzureKeyCredential(self.key)
            )
            self.index_client = SearchIndexClient(
                endpoint=self.service_endpoint,
                credential=AzureKeyCredential(self.key),
                index_name=self.index_name,
            )
            self.indexer_client = SearchIndexerClient(
                endpoint=self.service_endpoint, credential=AzureKeyCredential(self.key)
            )

        except Exception as e:
            logger.error(f"Failed to initialize AzureAISearchManager: {e}")
            raise

    def call_azure_search_api(
        self,
        resource: str,
        method: str,
        body: dict = None,
        api_version: str = "2023-11-01",
    ):
        """
        Calls the Azure Search API with the given parameters.

        :param resource: The resource to access.
        :param method: The HTTP method to use ("get" or "post").
        :param body: The body of the request for "post" method. Defaults to None.
        :param api_version: The API version to use. Defaults to "2023-11-01".

        :return: The status code and response from the API call.
        """
        url = f"{self.service_endpoint}/{resource}?&api-version={api_version}"
        headers = {
            "Content-Type": "application/json",
            "api-key": os.getenv("AZURE_SEARCH_ADMIN_KEY"),
        }

        response = None

        try:
            if method.lower() == "get":
                response = requests.get(url, headers=headers)
            elif method.lower() == "post":
                response = requests.post(url, headers=headers, data=body)
            else:
                raise ValueError("Invalid method. Expected 'get' or 'post'.")

            response.raise_for_status()
        except requests.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")

            error_response = (
                http_err.response.json()
            )  # Assuming the error response is in JSON format
            logger.error(f"Error code: {http_err.response.status_code}")
            logger.error(
                "Error message:",
                error_response.get("error", {}).get(
                    "message", "No error message available"
                ),
            )
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            traceback.print_exc()

        return (
            response.status_code if response else None,
            response.json() if response else None,
        )

    def create_index(
        self,
        fields: List[Any],
        vector_search: VectorSearch,
        semantic_search: SemanticSearch,
        index_name: Optional[str] = None,
    ):
        """
        Creates or updates an index with the given name, fields, algorithm configuration, and semantic search.

        :param fields: The fields to include in the index.
        :param algorithm_configuration: The algorithm configuration for the index.
        :param semantic_search: The semantic search for the index.
        :param index_name: The name of the index to create or update. Defaults to the class attribute index_name.
        """
        index_name = index_name or self.index_name

        index = SearchIndex(
            name=index_name,
            fields=fields,
            vector_search=vector_search,
            semantic_search=semantic_search,
        )
        try:
            result = self.index_client.create_or_update_index(index)
            logger.info("Index %s created", result.name)
        except Exception as ex:
            logger.error(ex)

    def create_data_source_connection(
        self, name: str, description: str, container_name: str, type: str = "azureblob"
    ):
        """
        Creates a data source in Azure Search.

        :param name: The name of the data source.
        :param description: A description of the data source.
        :param container_name: The name of the Azure Blob Storage container where the data is stored.
        :param type: The type of the data source. Defaults to "azureblob".
            Possible values include: "azuresql","cosmosdb", "azuretable", "mysql", "adlsgen2".

        :raises ValueError: If the storage connection string is not set in the environment variables.

        :return: None. Logs the response code and response from the API call.
        """
        if not self.connection_string:
            raise ValueError(
                "AZURE_STORAGE_CONNECTION_STRING is not set in the environment variables"
            )

        try:
            container = SearchIndexerDataContainer(name=container_name)
            data_source_connection = SearchIndexerDataSourceConnection(
                name=name,
                description=description,
                type=type,
                connection_string=self.connection_string,
                container=container,
            )
            data_source = self.indexer_client.create_or_update_data_source_connection(
                data_source_connection
            )

            logger.info(f"Data source '{data_source.name}' created or updated")
        except AzureError as e:
            logger.error(f"Failed to create or update data source: {e}")
            raise

    def create_or_update_skillset(
        self, skillset_name: str, description: str, skills: List[dict]
    ) -> None:
        """
        Creates or updates a skillset in Azure Search.

        :param skillset_name: The name of the skillset.
        :param description: A description of the skillset.
        :param skills: A list of skills to be included in the skillset.

        :return: None. Logs the response from the API call.
        """
        try:
            skillset = SearchIndexerSkillset(
                name=skillset_name, description=description, skills=skills
            )
            self.indexer_client.create_or_update_skillset(skillset)
            logger.info(f"Skillset '{skillset.name}' created or updated")
        except AzureError as e:
            logger.error(f"Failed to create or update skillset: {e}")
            raise

    def create_or_update_indexer(self, indexer: SearchIndexer) -> None:
        """
        Creates or updates an indexer in Azure Search.

        :param indexer: The SearchIndexer object to be created or updated.

        :return: None. Logs the response from the API call.
        """
        try:
            self.indexer_client.create_or_update_indexer(indexer)
            logger.info(f"Indexer '{indexer.name}' created or updated")
        except AzureError as e:
            logger.error(f"Failed to create or update indexer: {e}")
            raise

    def run_indexer(self, indexer_name: str) -> None:
        """
        Runs an indexer in Azure Search.

        :param indexer_name: The name of the indexer to run.

        :return: None. Logs the response from the API call.
        """
        try:
            self.indexer_client.run_indexer(indexer_name)
            logger.info(f"Indexer '{indexer_name}' run")
        except AzureError as e:
            logger.error(f"Failed to run indexer: {e}")
            raise
