from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class Industry(Base):
    __tablename__ = "industries"

    id = Column(Integer, primary_key=True, index=True)
    industry_name = Column(String(100), unique=True, nullable=False, index=True)

    companies = relationship("Company", back_populates="industry")

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(150), nullable=False, index=True)
    industry_id = Column(Integer, ForeignKey("industries.id"), nullable=True)

    industry = relationship("Industry", back_populates="companies")
