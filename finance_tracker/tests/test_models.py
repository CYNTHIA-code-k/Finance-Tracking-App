import pytest
from app import create_app, db
from app.models.user import User  # Import your User model (adjust based on your models)
from app.models.transaction import Transaction  # Import Transaction model as an example

@pytest.fixture
def test_client():
    app = create_app('testing')  # Assume there's a 'testing' configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()  # Create database tables
        yield app.test_client()  # Provide a test client
        db.session.remove()
        db.drop_all()  # Clean up database tables after tests

def test_create_user(test_client):
    # Example test for user creation
    new_user = User(username='testuser', email='testuser@example.com', password='password123')
    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.email == 'testuser@example.com'

def test_create_transaction(test_client):
    # Example test for creating a transaction
    new_user = User(username='testuser2', email='testuser2@example.com', password='password123')
    db.session.add(new_user)
    db.session.commit()

    transaction = Transaction(user_id=new_user.id, amount=100.0, description='Test Transaction')
    db.session.add(transaction)
    db.session.commit()

    saved_transaction = Transaction.query.filter_by(user_id=new_user.id).first()
    assert saved_transaction is not None
    assert saved_transaction.amount == 100.0
