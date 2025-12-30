from fastapi import APIRouter, Depends, UploadFile, status,Request
from fastapi.responses import JSONResponse
import os
from src.helpers.config import get_settings, Settings
from src.controllers import DataController, ProjectController,ProcessController
import aiofiles
from src.models import ResponseSignal
import logging
from .schemes.data import ProcessRequset
from src.models.ProjectModel import ProjectModel
from src.models.ChunkModel import ChunkModel
from src.models.db_schemes import DataChunk
logger =logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix="/api/v1/data",
    tags=["api v1", "data"],
)


@router.post("/upload/{project_id}")
async def upload_data(
    request:Request,
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings)
):
    # Initialize the project model and ensure collection/indexes are ready
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)
    # Step 1: Validate file type and size to ensure it's allowed
    data_controller = DataController()
    data_controller.validate_upload_file(file)
    
    # Step 2: Generate a unique name for the file and get its storage path
    file_path, file_id = data_controller.generate_unique_filepath(file.filename, project_id)
    
    # Save file in chunks (handles large files efficiently)
    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            # Walrus operator (:=) reads chunk and checks if not empty in one expression
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
    except Exception as e:
        logger.error(f"Failed to upload file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"signal": ResponseSignal.FILE_UPLOADED_FAILED.value}
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"signal": ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value, "file_id": file_id,"project_id":str(project_id)}
    )
    
@router.post("/process/{project_id}")
async def process_endpoint(
    project_id: str,
    request: Request,
    process_request: ProcessRequset,
    app_settings: Settings = Depends(get_settings)
):
    # Initialize models with the database client from the application state
    # Initialize models and ensure collections/indexes are ready
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

    # Ensure the project exists or create a new one
    project = await project_model.get_project_or_create_one(project_id=project_id)

    # Step 1: Extract processing parameters from the request body
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset
    
    # Step 2: Load the file content based on project and file ID
    process_controller = ProcessController(project_id)
    file_content = process_controller.get_file_content(file_id)
    
    # Step 3: Split content into chunks for RAG processing
    file_chunks = process_controller.process_file_content(file_content, file_id, chunk_size, overlap_size)
    
    # If no chunks were produced, return an error response
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_PROCESSED_FAILED.value}
        )
    
    # Step 4: Map the processed chunks to DataChunk database schema objects
    file_chunks_records = [
        DataChunk(
             chunk_text=chunk.page_content,
             chunk_metadata=chunk.metadata,
             chunk_order=i + 1,
             chunk_project_id=project.id
        )
        for i, chunk in enumerate(file_chunks)
    ]

    # Step 5: If reset is requested, delete existing chunks for this project
    if do_reset == 1:
        await chunk_model.delete_chunks_by_project_id(project_id=project.id)

    # Step 6: Insert the new chunks into the database in bulk
    no_records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.FILE_PROCESSED_SUCCESSFULLY.value, 
            "chunks": no_records
        }
    )