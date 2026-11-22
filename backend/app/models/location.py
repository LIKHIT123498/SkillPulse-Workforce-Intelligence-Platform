from sqlalchemy import Column, Integer, String
from app.database.session import Base

class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    district_name = Column(String(100), unique=True, nullable=False, index=True)
    state = Column(String(100), default="Maharashtra")