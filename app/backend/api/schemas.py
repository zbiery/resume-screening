from pydantic import BaseModel

class JobText(BaseModel):
    content: str

class ResumeText(BaseModel):
    content: str