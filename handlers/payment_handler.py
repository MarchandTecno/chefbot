# handlers/payment_handler.py
from datetime import datetime
from db_init import db
from models.payment_model import Payment
from sqlalchemy import text

def create_payment(data):
    """
    Crea un nuevo pago.
    Se espera que 'data' sea un diccionario con las claves:
      - order_id: ID de la orden.
      - payment_method: Método de pago (por ejemplo, 'Efectivo', 'Tarjeta').
      - amount: Monto a pagar.
    Retorna el ID del pago creado.
    """
    try:
        # Opción utilizando el ORM de SQLAlchemy
        payment = Payment(
            order_id=data["order_id"],
            payment_method=data["payment_method"],
            amount=data["amount"],
            paid_at=datetime.utcnow()
        )
        db.session.add(payment)
        db.session.commit()
        return payment.id
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al crear el pago: {str(e)}")

def get_payment(payment_id):
    """
    Obtiene un pago por su ID.
    Retorna un diccionario con los datos del pago o None si no existe.
    """
    try:
        payment = Payment.query.get(payment_id)
        if payment is None:
            return None
        return payment.to_dict()
    except Exception as e:
        raise Exception(f"Error al obtener el pago: {str(e)}")

def get_payments_by_order(order_id):
    """
    Obtiene todos los pagos asociados a una orden.
    Retorna una lista de diccionarios.
    """
    try:
        payments = Payment.query.filter_by(order_id=order_id).all()
        return [payment.to_dict() for payment in payments]
    except Exception as e:
        raise Exception(f"Error al obtener los pagos: {str(e)}")

def update_payment(payment_id, data):
    """
    Actualiza la información de un pago.
    Se espera que 'data' sea un diccionario opcional con las claves:
      - payment_method
      - amount
    Retorna el ID del pago actualizado.
    """
    try:
        payment = Payment.query.get(payment_id)
        if not payment:
            raise Exception("Pago no encontrado")
        if "payment_method" in data:
            payment.payment_method = data["payment_method"]
        if "amount" in data:
            payment.amount = data["amount"]
        # Opcional: actualizar paid_at si se incluye en data
        if "paid_at" in data:
            payment.paid_at = data["paid_at"]
        db.session.commit()
        return payment.id
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al actualizar el pago: {str(e)}")

def delete_payment(payment_id):
    """
    Elimina un pago por su ID.
    Retorna True si se elimina correctamente.
    """
    try:
        payment = Payment.query.get(payment_id)
        if not payment:
            raise Exception("Pago no encontrado")
        db.session.delete(payment)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al eliminar el pago: {str(e)}")
