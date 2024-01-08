import os
from functools import lru_cache
from typing import Optional

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

from utils.ml_logging import get_logger

# Initialize logging
logger = get_logger()


class AzureDocumentIntelligenceManager:
    """
    A class to interact with Azure's Document Analysis Client.
    """

    def __init__(
        self, azure_endpoint: Optional[str] = None, azure_key: Optional[str] = None
    ):
        """
        Initialize the class with configurations for Azure's Document Analysis Client.

        :param azure_endpoint: Endpoint URL for Azure's Document Analysis Client.
        :param azure_key: API key for Azure's Document Analysis Client.
        """
        self.azure_endpoint = azure_endpoint
        self.azure_key = azure_key

        if not self.azure_endpoint or not self.azure_key:
            self.load_environment_variables_from_env_file()

        if not self.azure_endpoint or not self.azure_key:
            raise ValueError(
                "Azure endpoint and key must be provided either as parameters or in a .env file."
            )

        self.document_analysis_client = DocumentAnalysisClient(
            endpoint=self.azure_endpoint, credential=AzureKeyCredential(self.azure_key)
        )

    @lru_cache(maxsize=1)
    def load_environment_variables_from_env_file(self):
        """
        Loads required environment variables for the application from a .env file.

        This method should be called explicitly if environment variables are to be loaded from a .env file.
        """
        load_dotenv()

        self.azure_endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.azure_key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

        # Check for any missing required environment variables
        required_vars = {
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT": self.azure_endpoint,
            "AZURE_DOCUMENT_INTELLIGENCE_KEY": self.azure_key,
        }

        missing_vars = [var for var, value in required_vars.items() if not value]

        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

    def analyze_document(
        self, document_input: str, model_type: str = "prebuilt-layout"
    ) -> dict:
        """
        Analyzes a document using Azure's Document Analysis Client with pre-trained models.

        :param document_input: URL or file path of the document to analyze.
        :param model_type: Type of pre-trained model to use for analysis. Defaults to 'prebuilt-layout'.
               Options include:
            - 'prebuilt-document': Generic document understanding.
            - 'prebuilt-layout': Extracts text, tables, selection marks, and structure elements.
            - 'prebuilt-read': Extracts print and handwritten text.
            - 'prebuilt-tax': Processes US tax documents.
            - 'prebuilt-invoice': Automates processing of invoices.
            - 'prebuilt-receipt': Scans sales receipts for key data.
            - 'prebuilt-id': Processes identity documents.
            - 'prebuilt-businesscard': Extracts information from business cards.
            - 'prebuilt-contract': Analyzes contractual agreements.
            - 'prebuilt-healthinsurancecard': Processes health insurance cards.
            Additional custom and composed models are also available. See the documentation for more details
              `https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-model-overview?view=doc-intel-4.0.0`
        :return: Analysis result.
        """
        if document_input.startswith("http://") or document_input.startswith(
            "https://"
        ):
            poller = self.document_analysis_client.begin_analyze_document_from_url(
                model_type, document_input
            )
        else:
            with open(document_input, "rb") as f:
                poller = self.document_analysis_client.begin_analyze_document(
                    model_type, f
                )

        return poller.result()
