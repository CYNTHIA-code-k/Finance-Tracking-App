from app.models.savings_goal import SavingsGoal
from app import db

class SavingsGoalService:
    @staticmethod
    def create_savings_goal(user_id, name, target_amount, deadline):
        goal = SavingsGoal(
            user_id=user_id,
            name=name,
            target_amount=target_amount,
            deadline=deadline
        )
        db.session.add(goal)
        db.session.commit()
        return goal
    
    @staticmethod
    def get_user_savings_goals(user_id):
        return SavingsGoal.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def update_goal_progress(goal_id, user_id, amount):
        goal = SavingsGoal.query.filter_by(id=goal_id, user_id=user_id).first()
        if goal:
            goal.current_amount = amount
            db.session.commit()
        return goal
    
    @staticmethod
    def delete_savings_goal(goal_id, user_id):
        goal = SavingsGoal.query.filter_by(id=goal_id, user_id=user_id).first()
        if goal:
            db.session.delete(goal)
            db.session.commit()
            return True
        return False