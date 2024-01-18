import os
from typing import Dict, List, Optional

from dotenv import load_dotenv
from openai import AzureOpenAI

from utils.ml_logging import get_logger

# Load environment variables from .env file
load_dotenv()

# Set up logger
logger = get_logger()


class AzureOpenAIManager:
    def __init__(self):
        """
        Initializes the Azure OpenAI Manager with necessary configurations.
        """
        self.openai_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2023-05-15",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        )
        self.completion_model_name = os.getenv("COMPLETION_MODEL")
        self.chat_model_name = os.getenv("CHAT_MODEL")
        self.embedding_model_name = os.getenv("EMBEDDING_MODEL")

        self._validate_api_configurations()

    def _validate_api_configurations(self):
        """
        Validates if all necessary configurations are set.
        """
        if not all(
            [
                self.openai_client.api_key,
                self.completion_model_name,
                self.chat_model_name,
                # self.embedding_model_name,
            ]
        ):
            raise ValueError("One or more OpenAI API setup variables are empty.")

    def generate_completion_response(
        self,
        query: str,
        temperature: float = 0.5,
        max_tokens: int = 100,
        model_name: Optional[str] = None,
        top_p: float = 1.0,
        **kwargs,
    ) -> Optional[str]:
        """
        Generates a text completion using Azure OpenAI's Foundation models.

        :param query: The input text query for the model.
        :param temperature: Controls randomness in the output. Default to 0.5.
        :param max_tokens: Maximum number of tokens to generate. Defaults to 100.
        :param model_name: The name of the AI model to use. Defaults to None.
        :param top_p: The cumulative probability cutoff for token selection. Defaults to 1.0.

        :return: The generated text or None if an error occurs.
        """
        try:
            response = self.openai_client.completions.create(
                model=model_name or self.completion_model_name,
                prompt=query,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                **kwargs,
            )

            completion = response.choices[0].text.strip()
            logger.info(f"Generated completion: {completion}")
            return completion

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return None

    def generate_chat_response(
        self,
        conversation_history: List[Dict[str, str]],
        query: str,
        system_message_content: str = "You are an AI assistant that helps people find information. Please be precise, polite, and concise.",
        temperature: float = 0.7,
        max_tokens: int = 150,
        seed: int = 42,
        top_p: float = 1.0,
        **kwargs,
    ) -> Optional[str]:
        """
        Generates a text response considering the conversation history.

        :param conversation_history: A list of message dictionaries representing the conversation history.
        :param query: The latest query to generate a response for.
        :param system_message_content: The content of the system message. Defaults to "You are an AI assistant that helps people find information. Please be precise, polite, and concise."
        :param temperature: Controls randomness in the output. Defaults to 0.7.
        :param max_tokens: Maximum number of tokens to generate. Defaults to 150.
        :param seed: Random seed for deterministic output. Defaults to 42.
        :param top_p: The cumulative probability cutoff for token selection. Defaults to 1.0.

        :return: The generated text response or None if an error occurs.
        """
        try:
            system_message = {"role": "system", "content": system_message_content}
            if not conversation_history or conversation_history[0] != system_message:
                conversation_history.insert(0, system_message)

            messages_for_api = conversation_history + [
                {"role": "user", "content": query}
            ]
            logger.info(f"Sending request to OpenAI with query: {query}")

            response = self.openai_client.chat.completions.create(
                model=self.chat_model_name,
                messages=messages_for_api,
                temperature=temperature,
                max_tokens=max_tokens,
                seed=seed,
                top_p=top_p,
                **kwargs,
            )

            response_content = response.choices[0].message.content
            logger.info(f"Received response from OpenAI: {response_content}")

            conversation_history.append({"role": "user", "content": query})
            conversation_history.append({"role": "system", "content": response_content})

            return response_content

        except Exception as e:
            logger.error(f"Contextual response generation error: {e}")
            return None

    def generate_embedding(
        self, input_text: str, model_name: Optional[str] = None, **kwargs
    ) -> Optional[str]:
        """
        Creates an embedding using Azure OpenAI's Foundation models.
        """
        try:
            response = self.openai_client.embeddings.create(
                input=input_text,
                model=model_name or self.embedding_model_name,
                kwargs=kwargs,
            )

            embedding = response.model_dump_json(indent=2)
            logger.info(f"Created embedding: {embedding}")
            return embedding

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return None
