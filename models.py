from pydantic import BaseModel
from typing import List

class ProjectBase(BaseModel):
    project_pdf: str
    title: str
    slug: str
    summary: str
    description: str
    year: int
    restricted: bool
    registration_status: bool
    deafpods_bool: bool

class ProjectCreate(ProjectBase):
    company: int
    labtimes: List[int]
    lecturetimes: List[int]
    tools: List[int]
    keywords: List[int]
    domain: int
    citizenship_status: int

class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: str
    updated_at: str