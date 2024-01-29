from fastapi import FastAPI
import logging
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import tiktoken
import re
from src.ocr.document_intelligence import AzureDocumentIntelligenceManager

# load environment variables
load_dotenv()

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

class RecordData(BaseModel):
    url: str

class Record(BaseModel):
    recordId: str
    data: RecordData

class RequestBody(BaseModel):
    values: List[Record]

document_intelligence_client = AzureDocumentIntelligenceManager()
app = FastAPI()

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def split_text_by_headings(text, section_headings):
    # Create a regex pattern that matches any of the section headings
    pattern = '|'.join('(?={})'.format(re.escape(sec)) for sec in section_headings)
    
    # Split the text by the section headings
    chunks = re.split(pattern, text)

    # Print the number of tokens in each chunk
    for i, chunk in enumerate(chunks):
        tokens = num_tokens_from_string(chunk)
        print(f"Number of tokens in chunk pre {i+1}: {tokens}")
    
    return chunks

def combine_chunks(chunks, min_length):
    combined_chunks = []
    current_chunk = ""

    for chunk in chunks:
        current_chunk += chunk
        tokens = num_tokens_from_string(current_chunk)
        if tokens >= min_length:
            combined_chunks.append(current_chunk)
            current_chunk = ""

    # If there's any text left in current_chunk after the loop, add it to combined_chunks
    if current_chunk:
        combined_chunks.append(current_chunk)

    # Print the number of tokens in each combined chunk
    for i, chunk in enumerate(combined_chunks):
        tokens = num_tokens_from_string(chunk)
        print(f"Number of tokens in chunk {i+1}: {tokens}")

    return combined_chunks

class RecordData(BaseModel):
    url: str

class Record(BaseModel):
    recordId: str
    data: RecordData

class RequestBody(BaseModel):
    values: List[Record]

@app.post("/vectorize")
async def vectorize(request_body: RequestBody):
    # json response
    json_response = {
        "values": []
    }

    # skill can receive multiple records at a time
    for record in request_body.values:
        url = record.data.url
        logger.info(f"Processing record: {record.recordId}")
        logger.info(f"Input url: {url}")

        # getting vector for image in url
        logger.info("Getting vector...")
        result_ocr = document_intelligence_client.analyze_document(
            document_input=url,
            model_type="prebuilt-layout",
            output_format='markdown',
            features=["OCR_HIGH_RESOLUTION"]
        )
        logger.info("Vector obtained successfully.")

        section_headings = [paragraph.content for paragraph in result_ocr.paragraphs if paragraph.role == "sectionHeading"]
        logger.info(f"Section headings: {section_headings}")
        split_text = split_text_by_headings(result_ocr.content,section_headings)
        chunks= combine_chunks(split_text, 250)
        logger.info(f"Number of chunks: {len(chunks)}")

        # add json to json_response values
        json_response["values"].append({
            "recordId": record.recordId,
            "data": {
                "chunks": chunks,
            },
            "errors": []
        })
        logger.info(f"Record {record.recordId} processed successfully.")

    return json_response

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=60)