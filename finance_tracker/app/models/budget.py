from app import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from app.models.transaction import Transaction

class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    alert_threshold = db.Column(db.Float, default=0.8)  # Alert at 80% of budget
    is_active = db.Column(db.Boolean, default=True)

    @hybrid_property
    def remaining_amount(self):
        spent = sum(t.amount for t in Transaction.query.filter_by(
            user_id=self.user_id,
            category=self.category
        ).filter(
            Transaction.date.between(self.start_date, self.end_date)
        ).all())
        return self.amount - spent
