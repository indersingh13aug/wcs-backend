from pydantic import BaseModel
from typing import List

class AccessUpdate(BaseModel):
    role_id: int
    page_ids: List[int]
