from datetime import date
from pydantic import BaseModel
class Post(BaseModel):
    id = int
    name = str
    content = str
    type = str
    # url = str
    # rating = str

    class Config:
        orm_mode = True