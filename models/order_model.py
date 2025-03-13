from db_init import db

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.Integer, nullable=True)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    items = db.relationship('OrderItem', backref='order', lazy=True)

