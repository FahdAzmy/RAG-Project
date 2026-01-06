from enum import Enum


class LLMenum(Enum):

    OPENAI = "OPENAI"
    COHERE = "COHERE"
    OPENROUTER = (
        "OPENROUTER"  # Unified provider for accessing multiple models via OpenRouter
    )


class OpenAiEnum(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class CohereEnum(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"

    DOCUMENT = "search_document"
    QUERY = "search_query"


class DocumentTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"
