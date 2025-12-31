from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums.DataBaseEnum import DataBaseEnum
import logging
from bson import ObjectId
class AssetsModel(BaseDataModel):
    """
    Data model for managing assets in the database.
    """
    def __init__(self, db_client: object):
        """
        Initialize the AssetsModel with the database client.
        """
        super().__init__(db_client=db_client)
        # Point to the assets collection
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Create a new instance of the model and initialize the collection/indexes.
        :param db_client: The database client instance.
        :return: An initialized instance of AssetsModel.
        """
        instance = cls(db_client=db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        """
        Initialize the assets collection and create indexes if they don't exist.
        """
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            await self.db_client.create_collection(DataBaseEnum.COLLECTION_ASSET_NAME.value)
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(index["key"], unique=index["unique"], name=index["name"])

    async def create_asset(self, asset: Asset):
        """
        Create a new asset record in the database.
        :param asset: Asset object to store.
        :return: The stored asset object with its database ID.
        """
        result = await self.collection.insert_one(asset.model_dump(by_alias=True, exclude_none=True))
        asset.id = result.inserted_id
        return asset

    async def get_all_project_assets(self, asset_project_id: str, asset_type:str):
        """
        Retrieve all assets for a specific project.
        :param asset_project_id: Project identifier.
        :return: List of Assets.
        """
        records = await self.collection.find({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
            "asset_type": asset_type
        }).to_list(length=None)
        return [
            Asset(**record)
            for record in records
        ]
    async def get_asset_record(self,asset_project_id:str , asset_name:str ):
        record = await self.collection.find_one({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
            "asset_name": asset_name
        }) 
        if record:
            return Asset(**record)
        return None