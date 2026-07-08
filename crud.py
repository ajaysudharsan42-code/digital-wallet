# crud.py
# All DB operations. main.py calls these, never touches DB directly.

from sqlalchemy.orm import Session
from models import User, Transaction


def create_user(db: Session, name: str, email: str) -> User:
    user = User(name=name, email=email, balance=0.0)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def _log_transaction(db: Session, wallet_id: str, txn_type: str, amount: float, status: str) -> Transaction:
    txn = Transaction(wallet_id=wallet_id, type=txn_type, amount=amount, status=status)
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


def credit_wallet(db: Session, user: User, amount: float) -> Transaction:
    user.balance += amount
    db.commit()
    return _log_transaction(db, user.id, "CREDIT", amount, "SUCCESS")


def debit_wallet(db: Session, user: User, amount: float) -> Transaction:
    if user.balance < amount:
        return _log_transaction(db, user.id, "DEBIT", amount, "FAILED")
    user.balance -= amount
    db.commit()
    return _log_transaction(db, user.id, "DEBIT", amount, "SUCCESS")


def transfer_funds(db: Session, sender: User, receiver: User, amount: float):
    if sender.balance < amount:
        failed = _log_transaction(db, sender.id, "TRANSFER", amount, "FAILED")
        return failed, None

    sender.balance -= amount
    receiver.balance += amount
    db.commit()

    debit_txn = _log_transaction(db, sender.id, "TRANSFER", amount, "SUCCESS")
    credit_txn = _log_transaction(db, receiver.id, "TRANSFER", amount, "SUCCESS")
    return debit_txn, credit_txn


def get_transactions(db: Session, wallet_id: str):
    return db.query(Transaction).filter(Transaction.wallet_id == wallet_id).all()
