from pydantic import BaseModel,Field,validator
from typing import Optional
from bson import ObjectId

# Database model for a single text chunk
class DataChunk(BaseModel):
    _id: Optional[ObjectId] # MongoDB internal ID
    chunk_text: str = Field(..., min_length=1) # The actual text content
    chunk_metadata: dict # Associated metadata (e.g., page number)
    chunk_order: int = Field(..., gt=0) # Sequence order of the chunk
    chunk_project_id: ObjectId # Reference to the project it belongs to
  
    class Config:
         arbitrary_types_allowed = True # Allow BSON ObjectId type