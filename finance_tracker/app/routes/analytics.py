from flask import jsonify
from flask_login import login_required, current_user
from app.routes import analytics_bp  # Import the blueprint from routes/__init__.py
from app.services.analytics_service import AnalyticsService

@analytics_bp.route('/api/analytics/spending-trends')
@login_required
def get_spending_trends():
    trends = AnalyticsService.calculate_spending_trends(current_user.id)
    return jsonify(trends)

@analytics_bp.route('/api/analytics/predicted-expenses')
@login_required
def get_predicted_expenses():
    prediction = AnalyticsService.predict_monthly_expenses(current_user.id)
    return jsonify({'predicted_monthly_expenses': prediction})

@analytics_bp.route('/api/analytics/category-breakdown')
@login_required
def get_category_breakdown():
    breakdown = AnalyticsService.get_category_breakdown(current_user.id)
    return jsonify(breakdown)

@analytics_bp.route('/api/analytics/budget-status/<float:budget_amount>')
@login_required
def get_budget_status(budget_amount):
    status = AnalyticsService.get_monthly_budget_status(current_user.id, budget_amount)
    return jsonify(status)