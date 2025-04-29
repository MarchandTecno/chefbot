from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from db_init import db

class Employee(db.Model):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convierte el objeto Employee a un diccionario JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "phone": self.phone,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }
