from fastapi import FastAPI
from src.routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from src.helpers.config import get_settings
from src.stores.llm.LLMProviderFactory import LLMProviderFactory

app = FastAPI()


# Event that runs when the FastAPI application starts
@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    # Initialize MongoDB client connection
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    # Connect to the specific database
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

    # Initialize LLM providers
    llm_provider_factory = LLMProviderFactory(settings)

    # Generation Client (for text generation)
    app.generation_client = llm_provider_factory.create(settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(settings.GENERATION_MODEL_ID)

    # Embedding Client (for text embeddings)
    app.embedding_client = llm_provider_factory.create(settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(
        settings.EMBEDDING_MODEL_ID, settings.EMBEDDING_MODEL_SIZE
    )


# Event that runs when the FastAPI application stops
@app.on_event("shutdown")
async def shutdown_db_client():
    # Close MongoDB connection
    app.mongo_conn.close()


app.include_router(base.router)
app.include_router(data.router)
