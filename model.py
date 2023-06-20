from pydantic import BaseModel
from typing import List

class Project(BaseModel):
    company: str
    title: str
    slug: str
    summary: str
    description: str
    year: int
    labtimes: str
    lecturetimes: str
    tools: str
    keywords: str
    domain: str
    citizenship_status: str

class Projects(BaseModel):
    project: list[Project] = []