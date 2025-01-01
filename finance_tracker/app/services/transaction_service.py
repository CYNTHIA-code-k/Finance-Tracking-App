from app.models.transaction import Transaction
from app import db
from datetime import datetime

class TransactionService:
    @staticmethod
    def create_transaction(user_id, amount, description, category, type):
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            description=description,
            category=category,
            type=type
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction
    
    @staticmethod
    def get_user_transactions(user_id):
        return Transaction.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_transaction_by_id(transaction_id, user_id):
        return Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    
    @staticmethod
    def get_transactions_by_date_range(user_id, start_date, end_date):
        return Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).all()