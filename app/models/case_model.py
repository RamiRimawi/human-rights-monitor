from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Location(BaseModel):
    country: str
    region: Optional[str]
    coordinates: Optional[dict] 

class Perpetrator(BaseModel):
    name: str
    type: str

class Evidence(BaseModel):
    type: str
    url: str
    description: Optional[str]
    date_captured: Optional[datetime]

class CaseCreate(BaseModel):
    case_id: str
    title: str
    description: Optional[str]
    violation_types: List[str]
    status: str = "new"
    priority: Optional[str]
    location: Location
    date_occurred: datetime
    date_reported: datetime
    victims: Optional[List[str]]
    perpetrators: Optional[List[Perpetrator]]
    evidence: Optional[List[Evidence]]
    created_by: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime]
