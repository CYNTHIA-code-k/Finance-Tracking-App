from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.budget import Budget
from app.schemas.budget_schema import BudgetSchema
from app import db

budget_bp = Blueprint('budget', __name__)
budget_schema = BudgetSchema()

@budget_bp.route('/', methods=['GET'])
@jwt_required()
def get_budgets():
    current_user_id = get_jwt_identity()
    budgets = Budget.query.filter_by(user_id=current_user_id).all()
    return jsonify(budget_schema.dump(budgets, many=True))

@budget_bp.route('/', methods=['POST'])
@jwt_required()
def create_budget():
    current_user_id = get_jwt_identity()
    data = budget_schema.load(request.json)
    
    new_budget = Budget(user_id=current_user_id, **data)
    db.session.add(new_budget)
    db.session.commit()
    
    return jsonify(budget_schema.dump(new_budget)), 201
