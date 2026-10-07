# Digital Wallet REST API

A backend REST API for managing digital wallets, built with Python, FastAPI, SQLAlchemy, and SQLite.

## Features

- Create and manage wallets
- Credit and debit wallet balances
- Transfer funds between wallets
- Track wallet transactions
- Validate transaction amounts
- Prevent negative wallet balances
- Handle missing wallets and insufficient balances

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

## Project Structure

| File | Description |
|------|-------------|
| `main.py` | FastAPI routes and application |
| `database.py` | Database connection and session management |
| `models.py` | Database models |
| `schemas.py` | API request and response schemas |
| `crud.py` | Database operations and wallet business logic |
| `requirements.txt` | Project dependencies |

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
