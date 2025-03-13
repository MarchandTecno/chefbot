# routes/order_routes.py
from flask import Blueprint, request, jsonify
from handlers.order_handler import (
    create_order,
    get_orders,
    update_order_status,
    get_order_details,
    delete_order
)

order_bp = Blueprint('order_routes', __name__)

# Crear una orden
@order_bp.route('/create', methods=['POST'])
def route_create_order():
    data = request.get_json()
    try:
        order_id = create_order(data)
        return jsonify({"message": "Orden creada con éxito", "order_id": order_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener todas las órdenes
@order_bp.route('/', methods=['GET'])
def route_get_orders():
    try:
        orders = get_orders()
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar el estado de una orden
@order_bp.route('/<int:order_id>', methods=['PUT'])
def route_update_order_status(order_id):
    data = request.get_json()
    try:
        updated_order = update_order_status(order_id, data.get("status"))
        return jsonify({
            "message": "Estado de la orden actualizado",
            "order_id": updated_order.id,
            "new_status": updated_order.status
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener detalles de una orden específica
@order_bp.route('/<int:order_id>', methods=['GET'])
def route_get_order_details(order_id):
    try:
        details = get_order_details(order_id)
        if details is None:
            return jsonify({"error": "Orden no encontrada"}), 404
        return jsonify(details), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar una orden
@order_bp.route('/<int:order_id>', methods=['DELETE'])
def route_delete_order(order_id):
    try:
        delete_order(order_id)
        return jsonify({"message": "Orden eliminada con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
