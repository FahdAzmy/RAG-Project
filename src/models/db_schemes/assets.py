from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id: Optional[object] = Field(None, alias="_id")
    asset_project_id: object
    asset_type: str = Field(..., min_length=1, description="Type of the asset")
    asset_name: str = Field(..., min_length=1, description="Name of the asset")
    asset_size: Optional[int] = Field(None, ge=0)
    asset_pushed_at: datetime = Field(default_factory=datetime.utcnow, description="Date and time when the asset was pushed")
    asset_config: dict = Field(default_factory=dict)
      
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        extra = "allow"

    @classmethod
    def get_indexes(cls):
        """
        Define the database indexes for the assets collection.
        :return: A list of index specifications.
        """
        return [
            {
                "key": [
                    ("asset_project_id", 1)
                ],
                "unique": False,
                "name": "asset_project_id_index_1"
            },
            {
                "key": [
                    ("asset_project_id", 1),
                    ("asset_name", 1)
                ],
                "unique": True,
                "name": "asset_project_id_asset_name_index_1"
            }
        ]