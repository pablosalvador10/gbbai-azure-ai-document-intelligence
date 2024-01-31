import os

from utils.ml_logging import get_logger
from typing import List, Optional, Dict, Union
from dotenv import load_dotenv
from src.azure_search_ai.core import AzureAISearchManager
import json

# Load environment variables from .env file
load_dotenv()

# Set up logger
logger = get_logger()

class AzureIndexerManager(AzureAISearchManager):
    """
    A manager class for handling operations related to Azure AI Search.
    """
    def __init__(self, 
                 index_name: str = None, 
                 service_endpoint: str = None):
        """
        Initializes the AzureAISearchManager with necessary configurations.

        :param index_name: The name of the index. Defaults to None.
        :param service_endpoint: The service endpoint URL. Defaults to None.
        """
        super().__init__(index_name=index_name, service_endpoint=service_endpoint)
        self.skills = []

    def add_built_in_skill(self, odata_type: str, 
                     name: str, 
                     description: str, 
                     context: str, 
                     defaultLanguageCode: Optional[str] = None,
                     textSplitMode: Optional[str] = None,
                     maximumPageLength: Optional[int] = None,
                     pageOverlapLength: Optional[int] = None,
                     maximumPagesToTake: Optional[int] = None,
                     inputs: Optional[Union[Dict, List[Dict]]] = None, 
                     outputs: Optional[Union[Dict, List[Dict]]] = None):
        """
        Creates a built-in skill and adds it to the skills list.

        :param odata_type: The type of the skill. Accepts "SplitSkill".
        :param name: The name of the skill.
        :param description: A description of the skill.
        :param context: The context of the skill.
        :param defaultLanguageCode: The default language code for the skill. Only applicable for "SplitSkill".
        :param textSplitMode: The text split mode for the skill. Only applicable for "SplitSkill".
        :param maximumPageLength: The maximum page length for the skill. Only applicable for "SplitSkill".
        :param pageOverlapLength: The page overlap length for the skill. Only applicable for "SplitSkill".
        :param maximumPagesToTake: The maximum pages to take for the skill. Only applicable for "SplitSkill".
        :param inputs: The inputs for the skill. Can be a dictionary or a list of dictionaries.
        :param outputs: The outputs for the skill. Can be a dictionary or a list of dictionaries.
        :param batch_size: The batch size for the skill. Not applicable for "SplitSkill".
        :param degree_of_parallelism: The degree of parallelism for the skill. Not applicable for "SplitSkill".
        """
        odata_type_map = {
            "EmbeddingSkill": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
            "SplitSkill": "#Microsoft.Skills.Text.SplitSkill"
        }

        skill = {
            "@odata.type": odata_type_map.get(odata_type),
            "name": name,
            "description": description,
            "context": context
        }

        if isinstance(inputs, dict):
            inputs = [inputs]
        if isinstance(outputs, dict):
            outputs = [outputs]

        if odata_type == "SplitSkill":
            skill.update({
                "defaultLanguageCode": defaultLanguageCode,
                "textSplitMode": textSplitMode,
                "maximumPageLength": maximumPageLength,
                "pageOverlapLength": pageOverlapLength,
                "maximumPagesToTake": maximumPagesToTake,
                "inputs": inputs,
                "outputs": outputs
            })

        elif odata_type == "EmbeddingSkill":
            azure_aoai_key = os.getenv('AZURE_OPENAI_KEY')
            azure_aoai_resource_uri = os.getenv('AZURE_OPENAI_API_ENDPOINT')
            azure_aoai_deployment_id = os.getenv('AZURE_AOAI_EMBEDDING_MODEL_DEPLOYMENT_ID')

            if not all([azure_aoai_key, azure_aoai_resource_uri, azure_aoai_deployment_id]):
                raise ValueError("Please set AZURE_OPENAI_KEY, AZURE_OPENAI_API_ENDPOINT, and AZURE_AOAI_EMBEDDING_MODEL_DEPLOYMENT_ID environment variables.")
            
            skill.update({
                "resourceUri": azure_aoai_resource_uri,
                "apiKey": azure_aoai_key,
                "deploymentId": azure_aoai_deployment_id,
                "inputs": inputs,
                "outputs": outputs
            })

        self.skills.append(skill)

    def add_custom_skill(self, 
                         name: str, 
                         description: str, 
                         context: str, 
                         inputs: Optional[Union[Dict, List[Dict]]] = None, 
                         outputs: Optional[Union[Dict, List[Dict]]] = None, 
                         uri: Optional[str] = None, 
                         batch_size: Optional[int] = None, 
                         degree_of_parallelism: Optional[int] = None):
        """
        Creates a custom skill and adds it to the skills list.

        :param name: The name of the skill.
        :param description: A description of the skill.
        :param context: The context of the skill.
        :param inputs: The inputs for the skill. Can be a dictionary or a list of dictionaries.
        :param outputs: The outputs for the skill. Can be a dictionary or a list of dictionaries.
        :param uri: The URI for the skill. Required for "CustomSkill".
        :param batch_size: The batch size for the skill. Required for "CustomSkill".
        :param degree_of_parallelism: The degree of parallelism for the skill. Required for "CustomSkill".
        """

        skill = {
            "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
            "name": name,
            "description": description,
            "context": context
        }
            
        skill.update({
                "uri": uri,
                "batchSize": batch_size,
                "degreeOfParallelism": degree_of_parallelism,
                "inputs": inputs,
                "outputs": outputs
            })

        self.skills.append(skill)

    def create_skillset(self, 
                        name: str,
                        description: str, 
                        skills: Optional[List[Dict]] = None) -> None:
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

        self.skillset = {
            "name": name,
            "description": description,
            "skills": skills
        }

                
        # Ensure that 'skills' is a list
        assert isinstance(self.skillset["skills"], list), "'skills' should be a list"

        # Ensure that each item in 'skills' is a dictionary
        for skill in self.skillset["skills"]:
            assert isinstance(skill, dict), "Each skill should be a dictionary"

        logger.info(f"Skillset: \n{json.dumps(self.skillset, indent=4)}")

        self.call_azure_search_api(resource="skillsets",
                                method="POST", 
                                api_version="2023-10-01-Preview", 
                                body=json.dumps(self.skillset))

    def create_indexer(self, indexer_name: str, 
                       description: str, 
                       data_source_name: str, 
                       skillset_name: str, 
                       target_index_name: str, 
                       field_mappings: List[dict], 
                       output_field_mappings: List[dict], 
                       parameters: dict) -> None:
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
                "cache" : {
                    "storageConnectionString" : self.connection_string,
                    "enableReprocessing": True
                },
                "targetIndexName": target_index_name,
                "fieldMappings": field_mappings,
                "outputFieldMappings": output_field_mappings,
                "parameters": parameters
            }

            _, _ = self.call_azure_search_api(resource="indexers",
                                   method="POST",
                                   api_version="2021-04-30-Preview", 
                                   body=json.dumps(body))
        except Exception as e:
            logger.error(f"Failed to create indexer: {e}")
            raise
 