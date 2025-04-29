# models/payment_model.py
from db_init import db
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from datetime import datetime

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, nullable=False)  # Se recomienda una ForeignKey si se necesita, e.g., db.ForeignKey('orders.id')
    payment_method = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    paid_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "payment_method": self.payment_method,
            "amount": float(self.amount),
            "paid_at": self.paid_at.strftime("%Y-%m-%d %H:%M:%S") if self.paid_at else None
        }
