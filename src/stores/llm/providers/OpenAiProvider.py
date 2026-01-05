from ..LLMinterface import LLMinterface
from openai import OpenAI
from ..LLMenum import OpenAiEnum
import logging

# OpenRouter base URL - compatible with OpenAI SDK
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

class OpenAiProvider(LLMinterface):
    """
    LLM Provider that uses OpenRouter to access OpenAI models.
    OpenRouter provides an OpenAI-compatible API endpoint.
    """
    
    def __init__(self, api_key: str, url: str = None, default_input_max_charracters: int = 1000,
                 default_genertation_max_output_tokens: int = 1000, default_generation_temperature: float = 0.1):
        
        self.api_key = api_key
        # Use OpenRouter base URL by default, or custom URL if provided
        self.url = url if url else OPENROUTER_BASE_URL
        self.default_input_max_charracters = default_input_max_charracters
        self.default_genertation_max_output_tokens = default_genertation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature
        self.generation_model_id = None
        
        self.embedding_model_id = None
        self.embedding_size = None
        
        # Initialize OpenAI client with OpenRouter's base URL
        # Note: OpenRouter uses 'base_url' parameter (not 'api_url')
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.url,
           
        )
        
        self.logger = logging.getLogger(__name__)
        # self.set_client()
        
        # # OpenRouter uses 'provider/model' format for model names
        # # For OpenAI models via OpenRouter, use 'openai/model-name'
        # self.set_generation_model("openai/gpt-3.5-turbo")  # Updated to modern model
        # self.set_embedding_model("openai/text-embedding-ada-002")
    def set_generation_model(self, model_id: str):
            self.generation_model_id = model_id
    def set_embedding_model(self, model_id: str,embedding_size: int):
            self.embedding_model_id = model_id    
            self.embedding_size = embedding_size    
    def generate_text(self, prompt: str, max_output_tokens: int=None,chat_history:list=[], temperature: float = None):
            
         if not self.client:
          self.logger.error("Client not initialized. Please call set_client() first.")
         if not self.generation_model_id:
          self.logger.error("Generation model not set. Please call set_generation_model() first.")
          return  None
         max_output_tokens= max_output_tokens if max_output_tokens else self.default_genertation_max_output_tokens
         temperature= temperature if temperature else self.default_generation_temperature
         chat_history.append(
            self.construct_prompt(prompt=prompt,role=OpenAiEnum.USER.value)
        )
         response=self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )
         if not response or not response.choices or not response.choices[0] or not response.choices[0].message or not response.choices[0].message.content:
          self.logger.error("Failed to generate text for prompt: %s", prompt)
          return None
         return response.choices[0].message.content
         
    def embed_text(self, text: str, document_type: str=None):
        
        if not self.client:
          self.logger.error("Client not initialized. Please call set_client() first.")
          raise None
         
        if not self.generation_model_id:
          self.logger.error("Generation model not set. Please call set_generation_model() first.")
          raise None
        
        response=self.client.embeddings.create(
            model=self.embedding_model_id,
            input=[text]
        )
        
        if not response or not response.data or not response.data[0] or not response.data[0].embedding:
          self.logger.error("Failed to generate embedding for text: %s", text)
          raise None
        return response.data[0].embedding
         
    def construct_prompt(self, prompt: str, role: str):
       return {
        "role":role,
        "content":self.process_text(prompt)
       } 
    def process_text(self, text: str):
        return text[self.default_input_max_charracters].strip()
       