# main.py
# API routes only. Delegates DB work to crud.py.

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Digital Wallet API")


@app.post("/users", response_model=schemas.UserOut, status_code=201)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, payload.name, payload.email)


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/wallets/{id}/credit", response_model=schemas.TransactionOut)
def credit(id: str, payload: schemas.AmountRequest, db: Session = Depends(get_db)):
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.credit_wallet(db, user, payload.amount)


@app.post("/wallets/{id}/debit", response_model=schemas.TransactionOut)
def debit(id: str, payload: schemas.AmountRequest, db: Session = Depends(get_db)):
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    txn = crud.debit_wallet(db, user, payload.amount)
    if txn.status == "FAILED":
        raise HTTPException(status_code=400, detail="Insufficient balance")
    return txn


@app.post("/wallets/transfer")
def transfer(payload: schemas.TransferRequest, db: Session = Depends(get_db)):
    sender = crud.get_user(db, payload.from_id)
    receiver = crud.get_user(db, payload.to_id)
    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="User not found")
    if payload.from_id == payload.to_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to same wallet")

    debit_txn, credit_txn = crud.transfer_funds(db, sender, receiver, payload.amount)
    if debit_txn.status == "FAILED":
        raise HTTPException(status_code=400, detail="Insufficient balance")
    return {"debit_txn": debit_txn, "credit_txn": credit_txn}


@app.get("/wallets/{id}/transactions", response_model=list[schemas.TransactionOut])
def transactions(id: str, db: Session = Depends(get_db)):
    if not crud.get_user(db, id):
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_transactions(db, id)
