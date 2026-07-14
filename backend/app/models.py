from sqlalchemy import Column, Integer, String, Text
from .database import Base


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False, index=True)
    category = Column(String(80), nullable=False, index=True)
    description = Column(Text, nullable=True)
    address = Column(String(255), nullable=True)
