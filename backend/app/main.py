from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List


from . import auth, crud, database, models

from . import schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="EcoTrack API")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.get("/indicators/", response_model=List[schemas.Indicator])
#def read_indicators(skip: int = 0, limit: int = 100, zone_id: int = None, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
#    indicators = crud.get_indicators(db, skip=skip, limit=limit, zone_id=zone_id)
#    return indicators
def read_indicators(
    skip: int = 0, 
    limit: int = 100, 
    zone_id: int = None,
    type: str = None,
    from_date: datetime = None,
    to_date: datetime = None,
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    indicators = crud.get_indicators(
        db, 
        skip=skip, 
        limit=limit, 
        zone_id=zone_id,
        type=type,
        start_date=from_date,
        end_date=to_date
    )
    return indicators

@app.post("/indicators/", response_model=schemas.Indicator)
def create_indicator(indicator: schemas.IndicatorCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_admin)):
    return crud.create_indicator(db=db, indicator=indicator)

@app.post("/zones/", response_model=schemas.Zone)
def create_zone(zone: schemas.ZoneCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_admin)):
    return crud.create_zone(db=db, zone=zone)

@app.get("/stats/average", response_model=schemas.StatsResponse)
def get_stats(
    zone_id: int, 
    type: str, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    stats = crud.get_stats_average(db, zone_id=zone_id, type=type)
    return stats