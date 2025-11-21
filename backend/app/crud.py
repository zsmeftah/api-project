from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas, auth
from collections import defaultdict

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, role: str = "user"):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_indicators(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    zone_id: int = None, 
    type: str = None, 
    start_date: datetime = None, 
    end_date: datetime = None
):
    query = db.query(models.Indicator)
    
    if zone_id:
        query = query.filter(models.Indicator.zone_id == zone_id)
    
    if type:
        query = query.filter(models.Indicator.type == type)
        
    if start_date:
        query = query.filter(models.Indicator.timestamp >= start_date)
        
    if end_date:
        query = query.filter(models.Indicator.timestamp <= end_date)
        
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

def get_stats_average(db: Session, zone_id: int, type: str):

    query = db.query(models.Indicator).filter(
        models.Indicator.zone_id == zone_id,
        models.Indicator.type == type
    ).order_by(models.Indicator.timestamp)
    results = query.all()

    daily_values = defaultdict(list)
    for item in results:

        day = item.timestamp.strftime("%Y-%m-%d")
        daily_values[day].append(item.value)

    labels = []
    series = []
    
    for day in sorted(daily_values.keys()):
        values = daily_values[day]
        avg = sum(values) / len(values)
        labels.append(day)
        series.append(round(avg, 2))

    return {"labels": labels, "series": series}