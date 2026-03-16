from sqlmodel import Session, select
from models.birdspotting import Birdspotting, BirdspottingCreate
from models.birds import Bird
from fastapi import HTTPException

class BirdspottingRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self):
        statement = select(Birdspotting)
        items = self.session.exec(statement).all()
        return items

    def get_one(self, id: int):
        statement = select(Birdspotting).where(Birdspotting.id == id)
        item = self.session.exec(statement).first()
        return item

    def insert(self, payload: BirdspottingCreate):
        # Check if bird exists
        if payload.bird_id not in [bird.id for bird in self.session.exec(select(Bird)).all()]:
            raise HTTPException(
                status_code=404,
                detail=f"Birdspotting with id {payload.bird_id} does not exist"
            )
        item = Birdspotting.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item