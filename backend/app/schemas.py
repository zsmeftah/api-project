from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None

class IndicatorBase(BaseModel):
    type: str
    source: str
    value: float
    unit: str
    zone_id: int
    timestamp: datetime

class IndicatorCreate(IndicatorBase):
    pass

class Indicator(IndicatorBase):
    id: int
    class Config:
        from_attributes = True

class ZoneBase(BaseModel):
    name: str
    postal_code: str

class ZoneCreate(ZoneBase):
    pass

class Zone(ZoneBase):
    id: int
    indicators: List[Indicator] = []
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    is_active: bool
    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    labels: List[str]
    series: List[float]