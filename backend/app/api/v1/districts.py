from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.location import District
from app.schemas.district import DistrictResponse

router = APIRouter(prefix="/districts", tags=["Districts"])

@router.get("", response_model=List[DistrictResponse])
def get_districts(db: Session = Depends(get_db)):
    return db.query(District).order_by(District.district_name.asc()).all()
