from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.savings_goal_service import SavingsGoalService

savings_goals_bp = Blueprint('savings_goals', __name__)

@savings_goals_bp.route('/savings-goals', methods=['POST'])
@jwt_required()
def create_savings_goal():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        goal = SavingsGoalService.create_savings_goal(
            user_id=user_id,
            name=data['name'],
            target_amount=data['target_amount'],
            deadline=data['deadline'],
            current_amount=data.get('current_amount', 0.0)
        )
        return jsonify(goal.to_dict()), 201
    except KeyError as e:
        return jsonify({'message': f'Missing required field: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@savings_goals_bp.route('/savings-goals/<int:goal_id>', methods=['GET'])
@jwt_required()
def get_savings_goal(goal_id):
    user_id = get_jwt_identity()
    goal = SavingsGoalService.get_savings_goal(goal_id, user_id)
    
    if not goal:
        return jsonify({'message': 'Savings goal not found'}), 404
        
    return jsonify(goal.to_dict())

@savings_goals_bp.route('/savings-goals', methods=['GET'])
@jwt_required()
def list_savings_goals():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = SavingsGoalService.get_user_savings_goals(
        user_id=user_id,
        page=page,
        per_page=per_page
    )
    
    return jsonify({
        'goals': [goal.to_dict() for goal in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    })

@savings_goals_bp.route('/savings-goals/<int:goal_id>', methods=['PUT'])
@jwt_required()
def update_savings_goal(goal_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    goal = SavingsGoalService.update_savings_goal(
        goal_id=goal_id,
        user_id=user_id,
        **data
    )
    
    if not goal:
        return jsonify({'message': 'Savings goal not found'}), 404
        
    return jsonify(goal.to_dict())

@savings_goals_bp.route('/savings-goals/<int:goal_id>', methods=['DELETE'])
@jwt_required()
def delete_savings_goal(goal_id):
    user_id = get_jwt_identity()
    
    if SavingsGoalService.delete_savings_goal(goal_id, user_id):
        return jsonify({'message': 'Savings goal deleted successfully'})
    
    return jsonify({'message': 'Savings goal not found'}), 404

@savings_goals_bp.route('/savings-goals/<int:goal_id>/contribute', methods=['POST'])
@jwt_required()
def contribute_to_goal(goal_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'amount' not in data:
        return jsonify({'message': 'No amount provided'}), 400
        
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({'message': 'Contribution amount must be positive'}), 400
            
        goal = SavingsGoalService.contribute_to_goal(
            goal_id=goal_id,
            user_id=user_id,
            amount=amount
        )
        
        if not goal:
            return jsonify({'message': 'Savings goal not found'}), 404
            
        response = goal.to_dict()
        if goal.is_goal_met():
            response['message'] = "Congratulations! You've reached your savings goal!"
            
        return jsonify(response)
        
    except ValueError:
        return jsonify({'message': 'Invalid amount format'}), 400