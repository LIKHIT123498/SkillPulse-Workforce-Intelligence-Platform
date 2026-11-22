from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.analytics import MarketOverviewResponse, SectorDemandItem, DistrictDemandItem
from app.services.analytics import (
    get_market_overview,
    get_skill_demand_by_sector,
    get_district_demand_distribution
)

router = APIRouter(prefix="/analytics", tags=["Labor Market Analytics"])

@router.get("/overview", response_model=MarketOverviewResponse)
def get_overview(db: Session = Depends(get_db)):
    """Returns high-level platform intelligence metrics."""
    return get_market_overview(db)

@router.get("/skills", response_model=List[SectorDemandItem])
def get_sector_skills(
    sector: Optional[str] = Query(None, description="Filter by sector name"),
    db: Session = Depends(get_db)
):
    """Returns skill-demand counts categorized by sector."""
    return get_skill_demand_by_sector(db, sector)

@router.get("/districts", response_model=List[DistrictDemandItem])
def get_district_demand(db: Session = Depends(get_db)):
    """Returns geographical demand distribution across Maharashtra districts."""
    return get_district_demand_distribution(db)
