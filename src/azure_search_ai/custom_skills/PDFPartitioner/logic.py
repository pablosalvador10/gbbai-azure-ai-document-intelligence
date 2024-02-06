import re
from typing import List

import tiktoken

from utils.ml_logging import get_logger

# Initialize logging
logger = get_logger()


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """
    Calculates the number of tokens in a given text string.

    :param string: The text string to be encoded.
    :param encoding_name: The name of the encoding to use. Defaults to "cl100k_base".
    :return: The number of tokens in the encoded string.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def split_text_by_headings(text: str, section_headings: List[str]) -> List[str]:
    """
    Splits text into chunks based on provided section headings.

    :param text: The text to be split.
    :param section_headings: A list of headings used to split the text.
    :return: List of text chunks.
    """
    pattern = "|".join("(?={})".format(re.escape(sec)) for sec in section_headings)
    chunks = re.split(pattern, text)
    for i, chunk in enumerate(chunks):
        logger.info(f"Number of tokens in chunk {i+1}: {num_tokens_from_string(chunk)}")
    return chunks


def combine_chunks(chunks: List[str], min_length: int) -> List[str]:
    """
    Combines text chunks into larger chunks with a minimum number of tokens.

    :param chunks: List of text chunks to be combined.
    :param min_length: Minimum length of each combined chunk in tokens.
    :return: List of combined text chunks.
    """
    combined_chunks = []
    current_chunk = ""
    for chunk in chunks:
        current_chunk += chunk
        if num_tokens_from_string(current_chunk) >= min_length:
            combined_chunks.append(current_chunk)
            current_chunk = ""
    if current_chunk:
        combined_chunks.append(current_chunk)
    return combined_chunks
