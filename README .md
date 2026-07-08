# Digital Wallet API

## Run
```
pip install -r requirements.txt
uvicorn main:app --reload
```
Test at http://127.0.0.1:8000/docs

## Files
- `database.py` — DB connection + session management
- `models.py` — DB tables (User, Transaction)
- `schemas.py` — API request/response shapes
- `crud.py` — DB logic (create, credit, debit, transfer)
- `main.py` — routes

## Business rules
- Balance never negative
- Amount must be > 0
- Every action logged as transaction
- 404 if wallet missing, 400 if insufficient balance
