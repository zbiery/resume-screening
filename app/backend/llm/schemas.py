from pydantic import BaseModel

class JobSchema(BaseModel):
    job_name: str
    job_description: str

class MatchingSchema(BaseModel):
    candidate: dict
    job: dict

class ResponseSchema(BaseModel):
    degree: list
    experience: list
    technical_skill: list
    responsibility: list
    certificate: list
    soft_skill: list