import io
import json
import os
import pickle
from typing import Any, List, Dict

from azure.storage.blob import BlobServiceClient
from docx import Document
from dotenv import load_dotenv

from src.extractors.pdf_data_extractor import PDFHelper
from utils.ml_logging import get_logger

logger = get_logger()
pdf_helper = PDFHelper()


class AzureBlobManager:
    """
    Class for managing interactions with Azure Blob Storage. It provides functionalities
    to read and write data to blobs, especially focused on handling various file formats.

    Attributes:
        container_name (str): Name of the Azure Blob Storage container.
        service_client (BlobServiceClient): Azure Blob Service Client.
        container_client: Azure Container Client specific to the container.
    """

    def __init__(self, container_name: str):
        """
        Initialize the AzureBlobManager with a container name.

        Args:
            container_name (str): Name of the Azure Blob Storage container.
        """
        try:
            load_dotenv()
            connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
            if connect_str is None:
                logger.error(
                    "AZURE_STORAGE_CONNECTION_STRING not found in environment variables."
                )
                raise EnvironmentError(
                    "AZURE_STORAGE_CONNECTION_STRING not found in environment variables."
                )
            self.service_client = BlobServiceClient.from_connection_string(connect_str)
            self.container_client = self.service_client.get_container_client(
                container_name
            )
            logger.info(f"Initialized AzureBlobManager with container {container_name}")
        except Exception as e:
            logger.error(f"Error initializing AzureBlobManager: {e}")
            raise

    def change_container(self, new_container_name: str):
        """
        Changes the Azure Blob Storage container.

        Args:
            new_container_name (str): The name of the new container.
        """
        self.container_client = self.service_client.get_container_client(
            new_container_name
        )
        logger.info(f"Container changed to {new_container_name}")

    def load_object(self, file_name: str) -> Any:
        """
        Loads an object from Azure Blob Storage based on the file extension.
        Supported file formats are CSV, JSON, Pickle, Parquet, DOCX, PDF, and plain text.

        Args:
            file_name (str): The name of the file to read from.

        Returns:
            Any: The object read from the file, typically a Pandas DataFrame for structured data files,
                or a string for DOCX, PDF, and text files.

        Raises:
            ValueError: If the file format is unsupported or not recognized.
        """
        try:
            # Extract file format from the file name
            _, file_extension = os.path.splitext(file_name)
            file_format = file_extension.lstrip(".").lower()

            blob_client = self.container_client.get_blob_client(file_name)
            downloader = blob_client.download_blob()
            content = downloader.readall()
            if file_format == "json":
                data = json.loads(content)
                logger.info(f"Successfully loaded JSON file {file_name}")
            elif file_format == "pickle":
                data = pickle.loads(content)
                logger.info(f"Successfully loaded Pickle file {file_name}")
            elif file_format == "docx":
                doc = Document(io.BytesIO(content))
                data = "\n".join([para.text for para in doc.paragraphs])
                logger.info(f"Successfully loaded DOCX file {file_name}")
            elif file_format == "pdf":
                data = pdf_helper.extract_text_from_pdf_bytes(content)
                metadata = pdf_helper.extract_metadata_from_pdf_bytes(content)
                logger.info(f"Successfully loaded PDF file {metadata}")
            elif file_format == "txt":
                data = content.decode()
                logger.info(f"Successfully loaded TXT file {file_name}")
            else:
                logger.error(f"Unsupported file format: {file_format}")
                raise ValueError("Unsupported file format: " + file_format)

            return data
        except Exception as e:
            logger.error(f"Error loading object from blob: {e}")
            raise

    def download_files_to_folder(self, folder_path: str, local_dir: str) -> None:
        """
        Downloads all files from a specified folder in Azure Blob Storage to a local directory.

        Args:
            folder_path (str): The path to the folder within the blob container.
            local_dir (str): The local directory to which the files will be downloaded.
        """
        try:
            # Ensure folder path ends with a '/'
            if not folder_path.endswith('/'):
                folder_path += '/'
                logger.info(f"Folder path {folder_path}")

            blob_list = self.container_client.list_blobs()
            for blob in blob_list:
                logger.info(f"{blob.name}")
                local_file_path = os.path.join(local_dir, os.path.basename(blob.name))
                blob_client = self.container_client.get_blob_client(blob.name)
                with open(local_file_path, "wb") as file:
                    downloader = blob_client.download_blob()
                    file.write(downloader.readall())

                logger.info(f"Downloaded {blob.name} to {local_file_path}")

        except Exception as e:
            logger.error(f"An error occurred while downloading files: {e}")
            raise

    def load_files_from_folder(self, folder_path: str) -> List[Dict[str, bytes]]:
        """
        Loads all files from a specified folder in Azure Blob Storage.

        Args:
            folder_path (str): The path to the folder within the blob container.
        Returns:
            List[Dict[str, bytes]]: A list of dictionaries where each dictionary has the file name as the key and the file content as the value.
        """
        try:
            # Ensure folder path ends with a '/'
            if not folder_path.endswith('/'):
                folder_path += '/'

            # List all blobs in the specified folder
            blob_list = self.container_client.list_blobs(name_starts_with=folder_path)
            files = [blob.name for blob in blob_list]

            if not files:
                logger.info(f"No files found in folder: {folder_path}")
                return []

            logger.info(f"Found {len(files)} files in {folder_path}")

            # Load each file
            loaded_files = []
            for file_name in files:
                loaded_files.append({file_name: self.load_object(file_name)})
                logger.info(f"Loaded file: {file_name}")

            return loaded_files

        except Exception as e:
            logger.error(f"An error occurred while loading files from folder: {e}")
            raise
