import glob
import os
import tempfile
from typing import Optional
from urllib.parse import urlparse

import fitz

from src.extractors.blob_data_extractor import AzureBlobDataExtractor
from utils.ml_logging import get_logger

logger = get_logger()


class OCRHelper:
    """
    Class for OCR functionalities, particularly extracting images from PDF files.
    """

    def __init__(self, container_name: Optional[str] = None):
        """
        Initialize the OCRHelper with a container name.
        Args:
            container_name (str): Name of the Azure Blob Storage container.
        """
        self.blob_manager = None
        if container_name:
            self.init_blob_manager(container_name)

    def init_blob_manager(self, container_name: str) -> None:
        """
        Initialize the AzureBlobManager with a container name.
        Args:
            container_name (str): Name of the Azure Blob Storage container.
        """
        self.blob_manager = AzureBlobDataExtractor(container_name)

    def extract_images_from_pdf(self, input_path: str, output_path: str) -> None:
        """
        Extracts pages from a PDF file or a folder of PDF files and saves them as pictures.
        Args:
            input_path (str): Path to the PDF file or folder of PDF files.
            output_path (str): Path to the folder where the pictures will be saved.
        """
        is_url = urlparse(input_path).scheme in ["http", "https"]

        if is_url:
            logger.info(f"Input path is a URL: {input_path}")
            with tempfile.TemporaryDirectory() as temp_dir:
                self.blob_manager.download_files_to_folder(input_path, temp_dir)
                self._process_pdf_path(temp_dir, output_path)
        else:
            logger.info(f"Input path is a local file or directory: {input_path}")
            self._process_pdf_path(input_path, output_path)

    def _process_pdf_path(self, input_path: str, output_path: str) -> None:
        """
        Processes a PDF file or all PDF files in a directory.
        Args:
            input_path (str): Path to the PDF file or directory containing PDF files.
            output_path (str): Path to save the extracted images.
        """
        if os.path.isdir(input_path):
            self._process_pdf_directory(input_path, output_path)
        elif os.path.isfile(input_path) and input_path.lower().endswith(".pdf"):
            self._process_single_pdf(input_path, output_path)
        else:
            logger.error("The input path is neither a valid PDF file nor a directory.")

    def _process_pdf_directory(self, directory_path: str, output_path: str) -> None:
        """
        Processes all PDF files in a directory and saves each page as an image.
        Args:
            directory_path (str): Directory containing PDF files.
            output_path (str): Directory where the images will be saved.
        """
        all_files = glob.glob(os.path.join(directory_path, "*.pdf"))
        logger.info(f"Found {len(all_files)} PDF files in {directory_path}")
        for file_path in all_files:
            logger.info(f"Processing file: {file_path}")
            self._process_single_pdf(file_path, output_path)

    def _process_single_pdf(self, file_path: str, output_path: str) -> None:
        """
        Processes a single PDF file and saves each page as an image.
        Args:
            file_path (str): Path to the PDF file.
            output_path (str): Directory where the images will be saved.
        """
        zoom_x = 2.0  # horizontal zoom
        zoom_y = 2.0  # vertical zoom
        mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

        logger.info(f"Opening file: {file_path}")
        doc = fitz.open(file_path)
        base_filename = os.path.splitext(os.path.basename(file_path))[0]

        for page_number, page in enumerate(doc):
            logger.info(f"Processing page {page_number + 1} of {file_path}")
            pix = page.get_pixmap(matrix=mat)
            output_filename = f"{base_filename}-page-{page_number + 1}.png"
            full_output_path = os.path.join(output_path, output_filename)

            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(full_output_path), exist_ok=True)

            pix.save(full_output_path)
            logger.info(f"Saved image: {full_output_path}")
