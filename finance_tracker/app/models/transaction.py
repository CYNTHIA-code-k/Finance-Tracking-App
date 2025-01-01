from datetime import datetime
from app import db
from sqlalchemy.ext.hybrid import hybrid_property

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50))
    type = db.Column(db.String(20))  # 'income' or 'expense'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    @hybrid_property
    def month_year(self):
        """Return the month and year of the transaction as a string"""
        return self.date.strftime('%Y-%m')
    
    def __repr__(self):
        return f'<Transaction {self.id}: {self.amount} - {self.description}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description,
            'date': self.date.isoformat() if self.date else None,
            'category': self.category,
            'type': self.type,
            'user_id': self.user_id,
            'month_year': self.month_year
        }