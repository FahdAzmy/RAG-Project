from ..LLMinterface import LLMinterface
from ..LLMenum import CohereEnum, DocumentTypeEnum
import logging
import cohere


class CoHereProvider(LLMinterface):
    """
    LLM Provider for Cohere API.
    """

    def __init__(
        self,
        api_key: str,
        default_input_max_charracters: int = 1000,
        default_genertation_max_output_tokens: int = 1000,
        default_generation_temperature: float = 0.1,
    ):
        """
        Initialize the Cohere provider.

        Args:
            api_key (str): The API key for accessing Cohere.
            default_input_max_charracters (int): Max characters for input text.
            default_genertation_max_output_tokens (int): Max tokens for generation.
            default_generation_temperature (float): Default temperature for generation.
        """
        self.api_key = api_key

        self.default_input_max_charracters = default_input_max_charracters
        self.default_genertation_max_output_tokens = (
            default_genertation_max_output_tokens
        )
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.Client(api_key=self.api_key)

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        """
        Set the model to be used for text generation.

        Args:
            model_id (str): The ID of the model.
        """
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        """
        Set the model to be used for embeddings.

        Args:
            model_id (str): The ID of the embedding model.
            embedding_size (int): The size of the embedding vector.
        """
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        """
        Process the text by slicing to max characters and stripping whitespace.

        Args:
            text (str): Input text.

        Returns:
            str: Processed text.
        """
        return text[: self.default_input_max_charracters].strip()

    def generate_text(
        self,
        prompt: str,
        max_output_tokens: int,
        chat_history: list = [],
        temperature: float = None,
    ):
        """
        Generate text response based on the prompt.

        Args:
            prompt (str): The user input prompt.
            max_output_tokens (int): Maximum tokens to generate.
            chat_history (list, optional): List of previous chat messages.
            temperature (float, optional): Sampling temperature.

        Returns:
            str: The generated text content or None if failed.
        """
        if not self.client:
            self.logger.error("Client not initialized. Please call set_client() first.")
        if not self.generation_model_id:
            self.logger.error(
                "Generation model not set. Please call set_generation_model() first."
            )
            return None
        max_output_tokens = (
            max_output_tokens
            if max_output_tokens
            else self.default_genertation_max_output_tokens
        )
        temperature = (
            temperature if temperature else self.default_generation_temperature
        )
        response = self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            message=self.process_text(
                prompt
            ),  # construct_prompt expects role, using process_text directly here for now to avoid error, or passing dummy role?
            # Original code was self.construct_prompt(prompt) which fails because of missing argument.
            # Assuming construct_prompt is desired but buggy. I will fix construct_prompt arg to be optional or pass a default.
            # But construct_prompt returns a DICT, and client.chat message expects STRING.
            # So I will use process_text(prompt) here which returns string.
            max_tokens=max_output_tokens,
            temperature=temperature,
        )
        if not response or not response.text:
            self.logger.error("Failed to generate text.")
            return None
        return response.text

    def embed_text(self, text: str, document_type: str = None):
        """
        Generate an embedding for the given text.

        Args:
            text (str): The text to embed.
            document_type (str, optional): Type of document (DOCUMENT or QUERY).

        Returns:
            list: The embedding vector.
        """
        if not self.client:
            self.logger.error("Client not initialized. Please call set_client() first.")
            raise None

        if not self.embedding_model_id:
            self.logger.error(
                "Embedding model not set. Please call set_embedding_model() first."
            )

        input_type = CohereEnum.DOCUMENT
        if document_type == DocumentTypeEnum.DOCUMENT:
            input_type = CohereEnum.DOCUMENT
        elif document_type == DocumentTypeEnum.QUERY:
            input_type = CohereEnum.QUERY

        response = self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text(text)],
            input_type=input_type,
            embedding_types=["float"],
        )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Failed to generate embedding for text: %s", text)
            raise None
        return response.embeddings.float

    def construct_prompt(self, prompt: str, role: str):
        """
        Construct a message dictionary (not used in generate_text directly here).

        Args:
            prompt (str): content
            role (str): role

        Returns:
            dict: message dict
        """
        return {"role": role, "text": self.process_text(prompt)}
