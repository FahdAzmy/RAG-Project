from enum import Enum


class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_SIZE_TOO_LARGE = "File size too large"
    FILE_VALIDATED_SUCCESSFULLY = "File validated successfully"
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully"
    FILE_UPLOADED_FAILED = "File uploaded failed"
    FILE_PROCESSED_FAILED="File processed failed"
    FILE_PROCESSED_SUCCESSFULLY="File processed successfully"
    NO_FILES_ERROR="No files found"
    FILE_ID_ERROR="File id not found"