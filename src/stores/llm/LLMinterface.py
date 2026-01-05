from abc import ABC, abstractmethod

class LLMinterface(ABC):
    """
    Abstract Base Class for Large Language Model (LLM) interfaces.
    Defines the standard operations for interacting with various LLM providers.
    """

    @abstractmethod
    def set_generation_model(self, model_id: str):
        """
        Sets the model identifier to be used for text generation.

        Args:
            model_id (str): The specific ID or name of the generation model.
        """
        pass 

    @abstractmethod
    def set_embedding_model(self, model_id: str):
        """
        Sets the model identifier to be used for generating embeddings.

        Args:
            model_id (str): The specific ID or name of the embedding model.
        """
        pass 

    @abstractmethod
    def generate_text(self, prompt: str, max_output_tokens: int,chat_history:list=[], temperature: float = None):
        """
        Generates text based on the provided prompt using the configured generation model.

        Args:
            prompt (str): The input text prompt for the model.
            max_output_tokens (int): The maximum number of tokens to generate in the response.
            temperature (float, optional): Sampling temperature to control randomness. Defaults to None.

        Returns:
            str: The generated text response.
        """
        pass 

    @abstractmethod
    def embed_text(self, text: str, document_type: str=None):
        """
        Generates an embedding vector for the provided text.

        Args:
            text (str): The input text to be embedded.
            document_type (str): The type of document (e.g., 'query', 'document').

        Returns:
            list[float]: The resulting embedding vector.
        """
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        """
        Constructs a formatted prompt string including role-specific instructions.

        Args:
            prompt (str): The core content of the prompt.
            role (str): The role associated with the prompt (e.g., 'system', 'user').

        Returns:
            str: The formatted prompt string.
        """
        pass