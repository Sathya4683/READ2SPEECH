from pydantic import BaseModel

class LinkSaved(BaseModel):
    status:str
    savedlink:str

