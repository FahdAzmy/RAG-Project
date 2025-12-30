from pydantic import BaseModel,Field,validator
from typing import Optional
from bson import ObjectId

# Database model for a Project
class Project(BaseModel):
    id: Optional[ObjectId]=Field(None,alias="_id")  # MongoDB internal ID
    project_id: str = Field(..., min_length=1) # User-defined project identifier
    
    # Custom validator for project_id
    @validator("project_id")
    def project_id_must_be_unique(cls, v):
        if not v.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return v

    class Config:
         arbitrary_types_allowed = True # Allow BSON ObjectId type