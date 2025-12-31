from .BaseController import BaseController
from .ProjectController import ProjectController
from  src.models import ProcessingEnum
import os 
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        # Get the directory path where this project's files are stored
        self.project_path = ProjectController().get_project_path(project_id)
    def get_file_extension(self, file_id: str):
        # Extract file extension (e.g., .txt or .pdf)
        return os.path.splitext(file_id)[-1]
    
    def get_file_laoder(self, file_id: str):
        file_extension = self.get_file_extension(file_id)
        # Construct the full absolute path to the file within the project directory
        file_path = os.path.join(self.project_path, file_id)
        

        # Ensure the file actually exists before trying to load it
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Return the appropriate loader based on file extension
        if file_extension == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        elif file_extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        else:
            raise ValueError("Unsupported file type", file_extension)
        return None
    def get_file_content(self, file_id: str): 
        # Initialize the loader and read the file content
        loader = self.get_file_laoder(file_id)
        # Return the loader if it was successfully created
        if loader :
            return loader.load()
        
        # Return None if no suitable loader could be initialized
        return None      
    def process_file_content(self, file_content: list, file_id: str, chunk_size: int = 200, overlap_size: int = 20):
        # Split the loaded document into smaller chunks for easier processing
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap_size, length_function=len)
        
        # Extract text content from each page/record
        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]
        
        # Maintain metadata (like page numbers) for each chunk
        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]
        
        # Create the final list of chunked documents
        chunks = text_splitter.create_documents(file_content_texts, metadatas=file_content_metadata)
        return chunks