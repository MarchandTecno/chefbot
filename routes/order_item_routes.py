# routes/order_item_routes.py
from flask import Blueprint, request, jsonify
from handlers.order_item_handler import (
    create_order_item,
    get_order_item,
    get_order_items_by_order,
    update_order_item,
    delete_order_item
)

order_item_bp = Blueprint('order_item', __name__)

# Crear un ítem de orden
@order_item_bp.route('/', methods=['POST'])
def route_create_order_item():
    data = request.get_json()
    try:
        # Se espera que 'data' contenga: order_id, menu_item_id, quantity y price.
        order_item_id = create_order_item(
            order_id=data['order_id'],
            menu_item_id=data['menu_item_id'],
            quantity=data['quantity'],
            price=data['price']
        )
        return jsonify({"message": "Ítem de la orden creado con éxito", "order_item_id": order_item_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener un ítem de orden por su ID
@order_item_bp.route('/<int:order_item_id>', methods=['GET'])
def route_get_order_item(order_item_id):
    try:
        order_item = get_order_item(order_item_id)
        if order_item is None:
            return jsonify({"error": "Ítem no encontrado"}), 404
        return jsonify(order_item), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener todos los ítems asociados a una orden
@order_item_bp.route('/order/<int:order_id>', methods=['GET'])
def route_get_order_items_by_order(order_id):
    try:
        items = get_order_items_by_order(order_id)
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar un ítem de orden
@order_item_bp.route('/<int:order_item_id>', methods=['PUT'])
def route_update_order_item(order_item_id):
    data = request.get_json()
    try:
        updated_id = update_order_item(order_item_id, data)
        return jsonify({"message": "Ítem actualizado con éxito", "order_item_id": updated_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar un ítem de orden
@order_item_bp.route('/<int:order_item_id>', methods=['DELETE'])
def route_delete_order_item(order_item_id):
    try:
        delete_order_item(order_item_id)
        return jsonify({"message": "Ítem eliminado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
