from sqlmodel import Session, select
from models.birds import Bird, BirdCreate
from models.species import Species
from fastapi import HTTPException

class BirdRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self):
        statement = select(Bird)
        items = self.session.exec(statement).all()
        return items

    def insert(self, payload: BirdCreate):
        # Check if bird exists
        if payload.species_id not in [species.id for species in self.session.exec(select(Species)).all()]:
            raise HTTPException(
                status_code=404,
                detail=f"Species with id {payload.species_id} does not exist"
            )
        if payload is None:
            raise HTTPException(
                status_code=404,
                detail=f"Bird with id {payload.species_id} does not exist"
            )
        item = Bird.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item