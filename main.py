from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/points/use", response_model=schemas.UserResponse)
def use_points(point_use: schemas.PointUse, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == point_use.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.points < point_use.amount:
        raise HTTPException(status_code=400, detail="Insufficient points")
    
    user.points -= point_use.amount
    db.commit()
    db.refresh(user)
    return user

@app.post("/points/charge", response_model=schemas.UserResponse)
def charge_points(point_charge: schemas.PointCharge, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == point_charge.user_id).first()
    if not user:
        user = models.User(user_id=point_charge.user_id, points=0)
        db.add(user)
    
    user.points += point_charge.amount
    db.commit()
    db.refresh(user)
    return user

@app.get("/points/check/{user_id}", response_model=schemas.UserResponse)
def check_points(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        user = models.User(user_id=user_id, points=0)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user 