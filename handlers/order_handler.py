# handlers/order_handler.py
from db_init import db
from models.order_model import Order
from models.order_item_model import OrderItem

def create_order(data):
    """
    Crea una nueva orden y sus ítems.
    Se espera que 'data' sea un diccionario con:
      - user_id: ID del usuario
      - employee_id: ID del empleado (opcional)
      - items: lista de ítems, cada uno con:
          - menu_item_id: ID del ítem del menú
          - quantity: cantidad (opcional, por defecto 1)
          - price: precio unitario (para calcular el subtotal)
    """
    user_id = data.get('user_id')
    employee_id = data.get('employee_id')
    items = data.get('items')  # lista de ítems

    if not user_id or not items:
        raise Exception("Datos insuficientes para crear la orden.")

    try:
        # Calcular total de la orden
        total = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
        new_order = Order(user_id=user_id, employee_id=employee_id, total=total, status='pendiente')
        db.session.add(new_order)
        db.session.commit()  # Para obtener new_order.id

        # Crear los ítems de la orden
        for item in items:
            quantity = item.get('quantity', 1)
            price = item.get('price', 0)
            subtotal = price * quantity
            order_item = OrderItem(
                order_id=new_order.id,
                menu_item_id=item.get('menu_item_id'),
                quantity=quantity,
                subtotal=subtotal
            )
            db.session.add(order_item)
        db.session.commit()

        return new_order.id
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error creando la orden: {str(e)}")

def get_orders():
    """
    Retorna una lista de todas las órdenes.
    """
    try:
        orders = Order.query.all()
        orders_list = []
        for order in orders:
            orders_list.append({
                "id": order.id,
                "user_id": order.user_id,
                "employee_id": order.employee_id,
                "total": order.total,
                "status": order.status,
                "created_at": order.created_at.isoformat() if order.created_at else None
            })
        return orders_list
    except Exception as e:
        raise Exception(f"Error obteniendo órdenes: {str(e)}")

def update_order_status(order_id, status):
    """
    Actualiza el estado de la orden identificada por order_id.
    """
    try:
        order = Order.query.get(order_id)
        if not order:
            raise Exception("Orden no encontrada.")
        order.status = status
        db.session.commit()
        return order
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error actualizando el estado de la orden: {str(e)}")

def get_order_details(order_id):
    """
    Retorna los detalles de una orden, incluyendo sus ítems.
    """
    try:
        order = Order.query.get(order_id)
        if not order:
            return None
        items = OrderItem.query.filter_by(order_id=order.id).all()
        item_list = []
        for item in items:
            item_list.append({
                "menu_item_id": item.menu_item_id,
                "quantity": item.quantity,
                "subtotal": item.subtotal,
                "created_at": item.created_at.isoformat() if item.created_at else None
            })
        details = {
            "id": order.id,
            "user_id": order.user_id,
            "employee_id": order.employee_id,
            "total": order.total,
            "status": order.status,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "items": item_list
        }
        return details
    except Exception as e:
        raise Exception(f"Error obteniendo los detalles de la orden: {str(e)}")

def delete_order(order_id):
    """
    Elimina una orden y sus ítems asociados.
    """
    try:
        order = Order.query.get(order_id)
        if not order:
            raise Exception("Orden no encontrada.")
        # Eliminar ítems asociados
        OrderItem.query.filter_by(order_id=order.id).delete()
        db.session.delete(order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error eliminando la orden: {str(e)}")
