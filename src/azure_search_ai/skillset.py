import json
import os
from typing import Dict, List, Optional, Union

from dotenv import load_dotenv

from src.azure_search_ai.core import AzureAISearchManager
from utils.ml_logging import get_logger

# Load environment variables from .env file
load_dotenv()

# Set up logger
logger = get_logger()


class IndexerManager(AzureAISearchManager):
    """
    A manager class for handling operations related to Azure AI Search.
    """

    def __init__(self, **kwargs):
        """
        Initializes the SkillsManager with necessary configurations.

        :param search_service_name: The name of the search service. If provided, the API will be called immediately. Defaults to None.
        :param kwargs: Other keyword arguments for the parent class.
        :raises ValueError: If any of the required environment variables are not set.
        """
        super().__init__(**kwargs)
        self.skills = []

    def create_skill(
        self,
        odata_type: str,
        name: str,
        description: str,
        context: str,
        resource_uri: Optional[str] = None,
        deployment_id: Optional[str] = None,
        inputs: Optional[Union[Dict, List[Dict]]] = None,
        outputs: Optional[Union[Dict, List[Dict]]] = None,
        uri: Optional[str] = None,
        batch_size: Optional[int] = None,
        degree_of_parallelism: Optional[int] = None,
    ):
        """
        Creates a skill and adds it to the skills list.

        :param odata_type: The type of the skill. Accepts "EmbeddingSkill" or "CustomSkill".
        :param name: The name of the skill.
        :param description: A description of the skill.
        :param context: The context of the skill.
        :param resource_uri: The resource URI for the skill. Required for "EmbeddingSkill".
        :param deployment_id: The deployment ID for the skill. Required for "EmbeddingSkill".
        :param inputs: The inputs for the skill. Can be a dictionary or a list of dictionaries.
        :param outputs: The outputs for the skill. Can be a dictionary or a list of dictionaries.
        :param uri: The URI for the skill. Required for "CustomSkill".
        :param batch_size: The batch size for the skill. Required for "CustomSkill".
        :param degree_of_parallelism: The degree of parallelism for the skill. Required for "CustomSkill".
        """
        odata_type_map = {
            "EmbeddingSkill": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
            "CustomSkill": "#Microsoft.Skills.Custom.WebApiSkill",
        }

        skill = {
            "@odata.type": odata_type_map.get(odata_type),
            "name": name,
            "description": description,
            "context": context,
        }

        if isinstance(inputs, dict):
            inputs = [inputs]
        if isinstance(outputs, dict):
            outputs = [outputs]

        if odata_type == "EmbeddingSkill":
            azure_aoai_key = os.getenv("AZURE_AOAI_KEY")
            azure_aoai_resource_uri = os.getenv("AZURE_AOAI_RESOURCE_URI")
            azure_aoai_deployment_id = os.getenv("AZURE_AOAI_EMBEDDING_DEPLOYMENT_ID")

            if not all(
                [azure_aoai_key, azure_aoai_resource_uri, azure_aoai_deployment_id]
            ):
                raise ValueError(
                    "Please set AZURE_AOAI_KEY, AZURE_AOAI_RESOURCE_URI, and AZURE_AOAI_EMBEDDING_DEPLOYMENT_ID environment variables."
                )

            skill.update(
                {
                    "resourceUri": resource_uri,
                    "apiKey": azure_aoai_key,
                    "deploymentId": deployment_id,
                    "inputs": inputs,
                    "outputs": outputs,
                }
            )

        elif odata_type == "CustomSkill":
            skill.update(
                {
                    "uri": uri,
                    "batchSize": batch_size,
                    "degreeOfParallelism": degree_of_parallelism,
                    "inputs": inputs,
                    "outputs": outputs,
                }
            )

        self.skills.append(skill)

    def create_skillset(
        self, name: str, description: str, skills: Optional[List[Dict]] = None
    ) -> None:
        """
        Creates a skillset with the given name and description.

        :param name: The name of the skillset.
        :param description: A description of the skillset.
        :param skills: The skills to add to the skillset. If not provided, the skills attribute of the class is used.
        :raises ValueError: If the skills list is empty.
        """
        skills = skills or self.skills
        if not skills:
            raise ValueError("No skills have been added to the skillset.")

        body = {"name": name, "description": description, "skills": skills}

        self.call_azure_search_api(
            resource="skillsets",
            method="POST",
            api_version="2023-10-01-Preview",
            body=body,
        )

    def create_indexer(
        self,
        indexer_name: str,
        description: str,
        data_source_name: str,
        skillset_name: str,
        target_index_name: str,
        field_mappings: List[dict],
        output_field_mappings: List[dict],
        parameters: dict,
    ) -> None:
        """
        Creates an indexer in Azure Search.

        :param indexer_name: The name of the indexer.
        :param description: A description of the indexer.
        :param data_source_name: The name of the data source.
        :param skillset_name: The name of the skillset.
        :param target_index_name: The name of the target index.
        :param field_mappings: A list of field mappings.
        :param output_field_mappings: A list of output field mappings.
        :param parameters: The parameters for the indexer.

        :return: None. Logs the response from the API call.
        """
        try:
            body = {
                "name": indexer_name,
                "description": description,
                "dataSourceName": data_source_name,
                "skillsetName": skillset_name,
                "cache": {
                    "storageConnectionString": self.connection_string,
                    "enableReprocessing": True,
                },
                "targetIndexName": target_index_name,
                "fieldMappings": field_mappings,
                "outputFieldMappings": output_field_mappings,
                "parameters": parameters,
            }

            code, response = self.search_api(
                "acs-geba",
                "indexers",
                "POST",
                apiVersion="2021-04-30-Preview",
                body=json.dumps(body),
            )
            print(code, response.json())
        except Exception as e:
            logger.error(f"Failed to create indexer: {e}")
            raise
