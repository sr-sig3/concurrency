from pydantic import BaseModel

class PointUse(BaseModel):
    user_id: str
    amount: float

class PointCharge(BaseModel):
    user_id: str
    amount: float

class PointCheck(BaseModel):
    user_id: str

class UserResponse(BaseModel):
    user_id: str
    points: float

    class Config:
        from_attributes = True 