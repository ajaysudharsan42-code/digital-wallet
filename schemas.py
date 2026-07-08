# schemas.py
# Defines API input/output shapes (separate from DB tables).

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    balance: float

    class Config:
        from_attributes = True


class AmountRequest(BaseModel):
    amount: float = Field(gt=0)


class TransferRequest(BaseModel):
    from_id: str
    to_id: str
    amount: float = Field(gt=0)


class TransactionOut(BaseModel):
    txn_id: str
    wallet_id: str
    type: str
    amount: float
    timestamp: datetime
    status: str

    class Config:
        from_attributes = True
