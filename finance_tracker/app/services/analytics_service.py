from collections import defaultdict
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models.transaction import Transaction

class AnalyticsService:
    @staticmethod
    def calculate_spending_trends(user_id, months=12):
        """
        Calculate spending trends by category for the specified number of months
        
        Args:
            user_id (int): The user ID to analyze
            months (int): Number of months to analyze (default: 12)
            
        Returns:
            dict: Monthly spending trends by category
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30 * months)
        
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date.between(start_date, end_date)
        ).all()
        
        monthly_trends = defaultdict(lambda: defaultdict(float))
        for transaction in transactions:
            if transaction.type == 'expense':
                month_year = transaction.month_year
                monthly_trends[month_year][transaction.category] += transaction.amount
        
        return dict(monthly_trends)
    
    @staticmethod
    def predict_monthly_expenses(user_id):
        """
        Predict monthly expenses based on the last 3 months of transaction data
        
        Args:
            user_id (int): The user ID to analyze
            
        Returns:
            float: Predicted monthly expenses
        """
        last_3_months = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.date >= datetime.utcnow() - timedelta(days=90)
        ).all()
        
        if not last_3_months:
            return 0
        
        total = sum(t.amount for t in last_3_months)
        return total / max(3, len(last_3_months))
    
    @staticmethod
    def get_category_breakdown(user_id, start_date=None, end_date=None):
        """
        Get spending breakdown by category for a specified date range
        
        Args:
            user_id (int): The user ID to analyze
            start_date (datetime): Start date for analysis (optional)
            end_date (datetime): End date for analysis (optional)
            
        Returns:
            dict: Category spending breakdown
        """
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
            
        query = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.date.between(start_date, end_date)
        )
        
        category_totals = {}
        for transaction in query.all():
            category = transaction.category or 'Uncategorized'
            category_totals[category] = category_totals.get(category, 0) + transaction.amount
            
        return category_totals

    @staticmethod
    def get_monthly_budget_status(user_id, budget_amount):
        """
        Calculate current month's spending against budget
        
        Args:
            user_id (int): The user ID to analyze
            budget_amount (float): Monthly budget amount
            
        Returns:
            dict: Budget status including total spent and remaining budget
        """
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        month_expenses = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.type == 'expense',
            Transaction.date >= start_of_month
        ).with_entities(func.sum(Transaction.amount)).scalar() or 0
        
        return {
            'budget': budget_amount,
            'spent': month_expenses,
            'remaining': budget_amount - month_expenses,
            'percentage_used': (month_expenses / budget_amount * 100) if budget_amount > 0 else 0
        }