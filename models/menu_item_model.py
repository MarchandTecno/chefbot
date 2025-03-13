# models/menu_item_model.py
from db_init import db

class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available = db.Column(db.Boolean, default=True)

