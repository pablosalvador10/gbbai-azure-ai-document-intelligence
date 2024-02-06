import logging
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from src.azure_search_ai.custom_skills.PDFPartitioner.logic import (
    combine_chunks,
    split_text_by_headings,
)
from src.ocr.document_intelligence import AzureDocumentIntelligenceManager

# Load environment variables
load_dotenv()

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


class RecordData(BaseModel):
    """
    Represents the data part of a record.

    :param url: URL of the document to be processed.
    """

    url: str


class Record(BaseModel):
    """
    Represents a single record.

    :param recordId: Unique identifier for the record.
    :param data: Data associated with the record.
    """

    recordId: str
    data: RecordData


class RequestBody(BaseModel):
    """
    Represents the request body.

    :param values: List of Record objects to be processed.
    """

    values: List[Record]


# Initialize Azure Document Intelligence client
document_intelligence_client = AzureDocumentIntelligenceManager()

# Initialize FastAPI application
app = FastAPI()


@app.post("/chunk")
async def split_pdf(request_body: RequestBody):
    """
    Processes a PDF and splits its content into chunks.

    :param request_body: The request body containing records to be processed.
    :return: A JSON response containing processed chunks.
    """
    json_response = {"values": []}
    for record in request_body.values:
        url = record.data.url
        logger.info(f"Processing record: {record.recordId} with URL: {url}")
        result_ocr = document_intelligence_client.analyze_document(
            document_input=url,
            model_type="prebuilt-layout",
            output_format="markdown",
            features=["OCR_HIGH_RESOLUTION"],
        )
        section_headings = [
            paragraph.content
            for paragraph in result_ocr.paragraphs
            if paragraph.role == "sectionHeading"
        ]
        split_text = split_text_by_headings(result_ocr.content, section_headings)
        chunks = combine_chunks(split_text, 250)
        json_response["values"].append(
            {"recordId": record.recordId, "data": {"chunks": chunks}, "errors": []}
        )
    return json_response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=60)
