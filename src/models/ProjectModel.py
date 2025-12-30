from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum
import logging

# Define logger to show results in uvicorn terminal
logger = logging.getLogger("uvicorn.error")


class ProjectModel(BaseDataModel):
    """
    Project Data Model.
    Responsible for performing CRUD operations for projects in the database.
    """
    def __init__(self, db_client: object):
        """
        Initialize the project model and bind it to the projects collection.
        """
        super().__init__(db_client=db_client)
        # Access the projects collection using its name defined in the Enum
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Create a new instance of the model and initialize the collection.
        :param db_client: The database client instance.
        :return: An initialized instance of ProjectModel.
        """
        instance = cls(db_client=db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        """
        Initialize the collection by creating it if it doesn't exist and setting up indexes.
        """
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            # Create collection explicitly to apply indexes immediately
            await self.db_client.create_collection(DataBaseEnum.COLLECTION_PROJECT_NAME.value)
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(index["key"], unique=index["unique"], name=index["name"])

    async def create_project(self, project: Project):
        """
        Create a new project in the database.
        :param project: Project object containing project data.
        :return: The project object after adding the generated database ID.
        """
        result = await self.collection.insert_one(project.dict(by_alias=True,exclude_unset=True))
        project._id = result.inserted_id
        return project

    async def get_project_or_create_one(self, project_id: str):
        """
        Search for a project by project_id; if not found, create it.
        :param project_id: Unique project identifier.
        :return: Project object (either existing or newly created).
        """
        # Search for the document in the database

        record = await self.collection.find_one({"project_id": project_id})     
        # debug here the record 
        logger.info(f"Project Record: {record}")
        logger.info(f"Project ID: {project_id}")
        if record is None:
            # If not found, create a new project
            project = Project(project_id=project_id)
            project = await self.create_project(project) 
            return project
            
        # If found, convert the dictionary to a Project object
        return Project(**record)    

    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        """
        Retrieve a list of all projects with pagination support.
        :param page: The requested page number.
        :param page_size: The number of projects per page.
        :return: List of project objects and the total number of pages.
        """
        # Count total number of documents
        total_documents = await self.collection.count_documents({})
        
        # Calculate total pages
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1
            
        # Fetch data using skip and limit for pagination
        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(Project(**document))
            
        return projects, total_pages    