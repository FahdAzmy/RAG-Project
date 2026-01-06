from ..LLMinterface import LLMinterface
from openai import OpenAI
from ..LLMenum import OpenAiEnum
import logging

# OpenRouter base URL - compatible with OpenAI SDK
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class OpenRouterProvider(LLMinterface):
    """
    Unified LLM Provider that uses OpenRouter to access multiple model providers.
    OpenRouter provides an OpenAI-compatible API endpoint.

    Supported models include:
    - OpenAI models: openai/gpt-4, openai/gpt-3.5-turbo, etc.
    - Cohere models: cohere/command, cohere/command-r, etc.
    - And many more providers via OpenRouter
    """

    def __init__(
        self,
        api_key: str,
        url: str = None,
        default_input_max_charracters: int = 1000,
        default_genertation_max_output_tokens: int = 1000,
        default_generation_temperature: float = 0.1,
    ):
        """
        Initialize the OpenRouter provider.

        Args:
            api_key (str): The OpenRouter API key.
            url (str, optional): Base URL for the API. Defaults to OpenRouter if None.
            default_input_max_charracters (int): Max characters for input text.
            default_genertation_max_output_tokens (int): Max tokens for generation.
            default_generation_temperature (float): Default temperature for generation.
        """
        self.api_key = api_key
        # Use OpenRouter base URL by default, or custom URL if provided
        self.url = url if url else OPENROUTER_BASE_URL
        self.default_input_max_charracters = default_input_max_charracters
        self.default_genertation_max_output_tokens = (
            default_genertation_max_output_tokens
        )
        self.default_generation_temperature = default_generation_temperature
        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        # Initialize OpenAI client with OpenRouter's base URL
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.url,
        )

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        """
        Set the model to be used for text generation.

        Args:
            model_id (str): The OpenRouter model ID.
                Examples:
                - OpenAI: 'openai/gpt-4', 'openai/gpt-3.5-turbo'
                - Cohere: 'cohere/command', 'cohere/command-r', 'cohere/command-r-plus'
        """
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        """
        Set the model to be used for embeddings.

        Args:
            model_id (str): The ID of the embedding model.
            embedding_size (int): The size of the embedding vector.

        Note: OpenRouter may have limited embedding support.
              Consider using a dedicated embedding service.
        """
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def generate_text(
        self,
        prompt: str,
        max_output_tokens: int = None,
        chat_history: list = [],
        temperature: float = None,
    ):
        """
        Generate text response based on the prompt and chat history.
        Works with any model available on OpenRouter (OpenAI, Cohere, etc.)

        Args:
            prompt (str): The user input prompt.
            max_output_tokens (int, optional): Maximum tokens to generate.
            chat_history (list, optional): List of previous chat messages.
            temperature (float, optional): Sampling temperature.

        Returns:
            str: The generated text content or None if failed.
        """

        if not self.client:
            self.logger.error("Client not initialized. Please call set_client() first.")
            return None
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

        # Create a copy of chat_history to avoid modifying the original
        messages = chat_history.copy()
        messages.append(
            self.construct_prompt(prompt=prompt, role=OpenAiEnum.USER.value)
        )

        response = self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=messages,
            max_tokens=max_output_tokens,
            temperature=temperature,
        )
        if (
            not response
            or not response.choices
            or not response.choices[0]
            or not response.choices[0].message
            or not response.choices[0].message.content
        ):
            self.logger.error("Failed to generate text for prompt: %s", prompt)
            return None
        return response.choices[0].message.content

    def embed_text(self, text: str, document_type: str = None):
        """
        Generate an embedding for the given text.

        Args:
            text (str): The text to embed.
            document_type (str, optional): Type of document (unused in this provider).

        Returns:
            list: The embedding vector.

        Note: OpenRouter may have limited embedding support.
              Consider using a dedicated embedding service like OpenAI directly.
        """
        if not self.client:
            self.logger.error("Client not initialized. Please call set_client() first.")
            return None

        if not self.embedding_model_id:
            self.logger.error(
                "Embedding model not set. Please call set_embedding_model() first."
            )
            return None

        response = self.client.embeddings.create(
            model=self.embedding_model_id, input=[text]
        )

        if (
            not response
            or not response.data
            or not response.data[0]
            or not response.data[0].embedding
        ):
            self.logger.error("Failed to generate embedding for text: %s", text)
            return None
        return response.data[0].embedding

    def construct_prompt(self, prompt: str, role: str):
        """
        Construct a message dictionary for the chat API.

        Args:
            prompt (str): The content of the message.
            role (str): The role of the sender (e.g., 'user', 'system').

        Returns:
            dict: formatted message with role and content.
        """
        return {"role": role, "content": self.process_text(prompt)}

    def process_text(self, text: str):
        """
        Process the text by slicing to max characters and stripping whitespace.

        Args:
            text (str): Input text.

        Returns:
            str: Processed text.
        """
        return text[: self.default_input_max_charracters].strip()
