from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models.birdspotting import Birdspotting, BirdspottingCreate
from repositories.birdspotting import BirdspottingRepository

router = APIRouter(prefix="/birdspotting", tags=["Birdspotting"])

def get_birdspotting_repository(
    session: Annotated[Session, Depends(get_session)],
) -> BirdspottingRepository:
    return BirdspottingRepository(session)

@router.get("/", response_model=List[Birdspotting])
async def get_birdspotting(repo: Annotated[BirdspottingRepository, Depends(get_birdspotting_repository)]):
    return repo.get_all()

@router.get("/{id}", response_model=Birdspotting)
async def get_birdspotting(repo: Annotated[BirdspottingRepository, Depends(get_birdspotting_repository)], id: int):
    item = repo.get_one(id)
    if item is None:
        raise HTTPException(status_code=404, detail="Birdspotting not found")
    return item

@router.post("/", response_model=Birdspotting)
async def add_birdspotting(birdspotting: BirdspottingCreate, repo: Annotated[BirdspottingRepository, Depends(get_birdspotting_repository)]):
    return repo.insert(birdspotting)