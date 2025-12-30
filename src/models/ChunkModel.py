from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne
import logging
class ChunkModel(BaseDataModel):
    """
    Data model for managing data chunks in the database.
    Responsible for individual chunk operations and bulk insertions.
    """
    def __init__(self, db_client: object):
        """
        Initialize the ChunkModel and bind it to the chunks collection.
        :param db_client: The database client instance.
        """
        super().__init__(db_client=db_client)
        # Reference the 'chunks' collection using the name defined in DataBaseEnum
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_chunk(self, chunk: DataChunk):
        """
        Create a single data chunk in the database.
        :param chunk: DataChunk object containing the chunk information.
        :return: The created DataChunk object with its assigned database ID.
        """
        result = await self.collection.insert_one(chunk.dict(by_alias=True,exclude_unset=True))
        chunk._id = result.inserted_id
        return chunk   

    async def get_chunk_by_id(self, chunk_id: str):
        """
        Retrieve a specific chunk by its unique database ObjectId.
        :param chunk_id: The string representation of the MongoDB ObjectId.
        :return: DataChunk object if found, otherwise None.
        """
        record = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        if record is None:
            return None
        return DataChunk(**record)

    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        """
        Insert multiple chunks into the database using bulk operations for efficiency.
        :param chunks: List of DataChunk objects to be inserted.
        :param batch_size: Number of chunks per batch to avoid overloading the database.
        :return: The total number of chunks processed.
        """
        for i in range(0, len(chunks), batch_size):
            # Extract a batch of chunks
            batch = chunks[i:i+batch_size]
            # Convert chunks to Pymongo InsertOne operations
            operations = [InsertOne(chunk.dict(by_alias=True,exclude_unset=True)) for chunk in batch]
            # Execute bulk write operation
            await self.collection.bulk_write(operations)
            
        return len(chunks)
    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        """
        Delete all chunks associated with a specific project.
        :param project_id: The project identifier to which the chunks belong.
        :return: The number of chunks deleted.
        """
        result = await self.collection.delete_many({"chunk_project_id": project_id})
        return result.deleted_count