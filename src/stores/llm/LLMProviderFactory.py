from .LLMenum import LLMenum
from .providers import OpenAiProvider, CoHereProvider, OpenRouterProvider


class LLMProviderFactory:
    """
    Factory class for creating LLM providers.

    Supports:
    - OPENAI: Direct OpenAI API access
    - COHERE: Direct Cohere API access
    - OPENROUTER: Unified access to OpenAI, Cohere, and many other models via OpenRouter
    """

    def __init__(self, config=dict):
        self.config = config

    def create(self, provider: str):
        """
        Create an LLM provider instance based on the provider type.

        Args:
            provider (str): The provider type (OPENAI, COHERE, or OPENROUTER)

        Returns:
            LLMinterface: An instance of the specified provider, or None if invalid.
        """
        if provider == LLMenum.OPENAI.value:
            return OpenAiProvider(
                api_key=self.config.OPENAI_API_KEY,
                url=self.config.OPENAI_API_URL,
                default_input_max_charracters=self.config.INPUT_DEFUALT_MAX_CHARACTERS,
                default_genertation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPRATURE,
            )
        if provider == LLMenum.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_charracters=self.config.INPUT_DEFUALT_MAX_CHARACTERS,
                default_genertation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPRATURE,
            )
        if provider == LLMenum.OPENROUTER.value:
            # Unified provider using OpenRouter - supports OpenAI, Cohere, and more
            # Use model IDs like: 'openai/gpt-4', 'cohere/command-r', etc.
            # Note: Using OPENAI_API_KEY which contains the OpenRouter API key
            return OpenRouterProvider(
                api_key=self.config.OPENAI_API_KEY,
                url=self.config.OPENAI_API_URL,  # OpenRouter URL: https://openrouter.ai/api/v1
                default_input_max_charracters=self.config.INPUT_DEFUALT_MAX_CHARACTERS,
                default_genertation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPRATURE,
            )
        return None
