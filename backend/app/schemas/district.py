from pydantic import BaseModel

class DistrictBase(BaseModel):
    district_name: str
    state: str = "Maharashtra"

class DistrictResponse(DistrictBase):
    id: int

    class Config:
        from_attributes = True
