from sqlalchemy.orm import Session

from . import auth
from . import models
from . import schemas

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, role: str = "user"):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_indicators(db: Session, skip: int = 0, limit: int = 100, zone_id: int = None):
    query = db.query(models.Indicator)
    if zone_id:
        query = query.filter(models.Indicator.zone_id == zone_id)
    return query.offset(skip).limit(limit).all()

def create_indicator(db: Session, indicator: schemas.IndicatorCreate):
    db_indicator = models.Indicator(**indicator.dict())
    db.add(db_indicator)
    db.commit()
    db.refresh(db_indicator)
    return db_indicator

def create_zone(db: Session, zone: schemas.ZoneCreate):
    db_zone = models.Zone(**zone.dict())
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

def get_zone_by_name(db: Session, name: str):
    return db.query(models.Zone).filter(models.Zone.name == name).first()