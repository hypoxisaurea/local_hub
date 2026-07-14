from pydantic import BaseModel
from typing import Optional


class PlaceBase(BaseModel):
    title: str
    category: str
    description: Optional[str] = None
    address: Optional[str] = None


class PlaceCreate(PlaceBase):
    pass


class Place(PlaceBase):
    id: int

    class Config:
        orm_mode = True
