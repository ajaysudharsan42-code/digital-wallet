# models.py
# DB tables as Python classes.

import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0)


class Transaction(Base):
    __tablename__ = "transactions"

    txn_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    wallet_id = Column(String, ForeignKey("users.id"))
    type = Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
