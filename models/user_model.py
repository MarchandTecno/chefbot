from flask_sqlalchemy import SQLAlchemy
from db_init import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  
    current_order = db.Column(db.JSON, nullable=True)

    def start_order(self):
        self.current_order = []

    def add_to_order(self, item):
        if self.current_order is not None:
            self.current_order.append(item)

    def clear_order(self):
        self.current_order = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "current_order": self.current_order,
        }
