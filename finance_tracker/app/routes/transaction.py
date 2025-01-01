from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transaction import Transaction
from app.schemas.transaction_schema import TransactionSchema
from app import db, cache

transaction_bp = Blueprint('transaction', __name__)
transaction_schema = TransactionSchema()

@transaction_bp.route('/', methods=['GET'])
@jwt_required()
@cache.memoize(timeout=300)
def get_transactions():
    current_user_id = get_jwt_identity()
    transactions = Transaction.query.filter_by(user_id=current_user_id).all()
    return jsonify(transaction_schema.dump(transactions, many=True))

@transaction_bp.route('/', methods=['POST'])
@jwt_required()
def create_transaction():
    current_user_id = get_jwt_identity()
    data = transaction_schema.load(request.json)
    
    new_transaction = Transaction(user_id=current_user_id, **data)
    db.session.add(new_transaction)
    db.session.commit()
    
    # Clear cache for this user's transactions
    cache.delete_memoized(get_transactions, current_user_id)
    
    return jsonify(transaction_schema.dump(new_transaction)), 201