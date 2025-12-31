from pydantic import BaseModel
from typing import Optional
class ProcessRequset(BaseModel):
    file_id:str =None
    chunk_size:Optional[int] = 1000
    overlap_size:Optional[int] = 20
    do_reset:Optional[int]=0
    
