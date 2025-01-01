import pytest
from app import create_app, db
from app.models.transaction import Transaction
from app.services.transaction_service import create_transaction, get_transactions  # Import functions to be tested

@pytest.fixture
def setup_app():
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_create_transaction_service(setup_app):
    # Example test for service that creates a transaction
    transaction_data = {"user_id": 1, "amount": 150.0, "description": "Service Test"}
    transaction = create_transaction(transaction_data)

    assert transaction is not None
    assert transaction.amount == 150.0

def test_get_transactions_service(setup_app):
    # Example test for service that retrieves transactions
    transaction = Transaction(user_id=1, amount=100.0, description='Test Transaction')
    db.session.add(transaction)
    db.session.commit()

    transactions = get_transactions(user_id=1)
    assert len(transactions) == 1
    assert transactions[0].amount == 100.0
