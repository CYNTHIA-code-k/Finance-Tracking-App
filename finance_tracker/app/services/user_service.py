from app.models.user import User
from app import db

class UserService:
    @staticmethod
    def create_user(username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if user:
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            db.session.commit()
        return user