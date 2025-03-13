# handlers/order_item_handler.py
from db_init import db
from models.order_item_model import OrderItem

def create_order_item(order_id, menu_item_id, quantity, price):
    """
    Crea un nuevo ítem para una orden.
    Se espera:
      - order_id: ID de la orden a la que se añade el ítem.
      - menu_item_id: ID del platillo en el menú.
      - quantity: Cantidad pedida.
      - price: Precio unitario del platillo (usado para calcular el subtotal).
    Retorna el ID del ítem creado.
    """
    try:
        subtotal = price * quantity
        order_item = OrderItem(
            order_id=order_id,
            menu_item_id=menu_item_id,
            quantity=quantity,
            subtotal=subtotal
        )
        db.session.add(order_item)
        db.session.commit()
        return order_item.id
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error creando el ítem de la orden: {str(e)}")

def get_order_item(order_item_id):
    """
    Obtiene los detalles de un ítem de la orden por su ID.
    Retorna un diccionario con los datos o None si no se encuentra.
    """
    try:
        order_item = OrderItem.query.get(order_item_id)
        if not order_item:
            return None
        return {
            "id": order_item.id,
            "order_id": order_item.order_id,
            "menu_item_id": order_item.menu_item_id,
            "quantity": order_item.quantity,
            "subtotal": order_item.subtotal,
            "created_at": order_item.created_at.isoformat() if order_item.created_at else None
        }
    except Exception as e:
        raise Exception(f"Error obteniendo el ítem de la orden: {str(e)}")

def get_order_items_by_order(order_id):
    """
    Obtiene todos los ítems asociados a una orden dada.
    Retorna una lista de diccionarios.
    """
    try:
        order_items = OrderItem.query.filter_by(order_id=order_id).all()
        return [{
            "id": item.id,
            "order_id": item.order_id,
            "menu_item_id": item.menu_item_id,
            "quantity": item.quantity,
            "subtotal": item.subtotal,
            "created_at": item.created_at.isoformat() if item.created_at else None
        } for item in order_items]
    except Exception as e:
        raise Exception(f"Error obteniendo los ítems de la orden: {str(e)}")

def update_order_item(order_item_id, data):
    """
    Actualiza un ítem de la orden.
    Se puede actualizar la cantidad y, opcionalmente, recalcular el subtotal si se proporciona el precio.
    Se espera que 'data' contenga:
      - quantity (opcional)
      - price (opcional, para recalcular el subtotal)
      - menu_item_id (opcional)
    Retorna el ID del ítem actualizado.
    """
    try:
        order_item = OrderItem.query.get(order_item_id)
        if not order_item:
            raise Exception("Ítem de la orden no encontrado")
        if "quantity" in data:
            order_item.quantity = data["quantity"]
            if "price" in data:
                order_item.subtotal = data["quantity"] * data["price"]
        if "menu_item_id" in data:
            order_item.menu_item_id = data["menu_item_id"]
        db.session.commit()
        return order_item.id
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error actualizando el ítem de la orden: {str(e)}")

def delete_order_item(order_item_id):
    """
    Elimina un ítem de la orden dado su ID.
    """
    try:
        order_item = OrderItem.query.get(order_item_id)
        if not order_item:
            raise Exception("Ítem de la orden no encontrado")
        db.session.delete(order_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error eliminando el ítem de la orden: {str(e)}")
