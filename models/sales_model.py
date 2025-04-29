# models/sales_model.py
from sqlalchemy import Column, Integer, Numeric, Date, DateTime
from db_init import db

class Sale(db.Model):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_sales = Column(Numeric(10, 2), nullable=False)
    cash_sales = Column(Numeric(10, 2), nullable=False)
    card_sales = Column(Numeric(10, 2), nullable=False)
    transfer_sales = Column(Numeric(10, 2), nullable=False)
    sales_date = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=db.func.current_timestamp(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "total_sales": float(self.total_sales),
            "cash_sales": float(self.cash_sales),
            "card_sales": float(self.card_sales),
            "transfer_sales": float(self.transfer_sales),
            "sales_date": self.sales_date.isoformat() if self.sales_date else None,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }
