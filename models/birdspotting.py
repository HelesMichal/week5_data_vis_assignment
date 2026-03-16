from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class BirdspottingBase(SQLModel):
    spotted_at: datetime
    location: str
    observer_name: str

class Birdspotting(BirdspottingBase, table=True):
    # __tablename__ = "birdspotting"
    id: Optional[int] = Field(default=None, primary_key=True)
    bird_id: int = Field(foreign_key="birds.id")
    notes: Optional[str] = None
    # bird: Optional[Bird] = Relationship()

class BirdspottingCreate(BirdspottingBase):
    bird_id: int