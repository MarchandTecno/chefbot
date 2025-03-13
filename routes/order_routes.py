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

@order_bp.route('/create', methods=['POST'])
def route_create_order():
    """
    Crear una orden.
    ---
    tags:
      - Orders
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - user_id
            - items
          properties:
            user_id:
              type: integer
              example: 1
            employee_id:
              type: integer
              example: 2
            items:
              type: array
              items:
                type: object
                required:
                  - menu_item_id
                  - quantity
                  - price
                properties:
                  menu_item_id:
                    type: integer
                    example: 3
                  quantity:
                    type: integer
                    example: 2
                  price:
                    type: number
                    example: 150.00
    responses:
      201:
        description: Orden creada con éxito.
      500:
        description: Error interno.
    """
    data = request.get_json()
    try:
        order_id = create_order(data)
        return jsonify({"message": "Orden creada con éxito", "order_id": order_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@order_bp.route('/', methods=['GET'])
def route_get_orders():
    """
    Obtener todas las órdenes.
    ---
    tags:
      - Orders
    responses:
      200:
        description: Lista de órdenes.
      500:
        description: Error interno.
    """
    try:
        orders = get_orders()
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@order_bp.route('/<int:order_id>', methods=['PUT'])
def route_update_order_status(order_id):
    """
    Actualizar el estado de una orden.
    ---
    tags:
      - Orders
    parameters:
      - in: path
        name: order_id
        type: integer
        required: true
        description: ID de la orden a actualizar.
      - in: body
        name: body
        schema:
          type: object
          properties:
            status:
              type: string
              example: completada
    responses:
      200:
        description: Estado de la orden actualizado correctamente.
      500:
        description: Error interno.
    """
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

@order_bp.route('/<int:order_id>', methods=['GET'])
def route_get_order_details(order_id):
    """
    Obtener detalles de una orden específica.
    ---
    tags:
      - Orders
    parameters:
      - in: path
        name: order_id
        type: integer
        required: true
        description: ID de la orden.
    responses:
      200:
        description: Detalles de la orden.
      404:
        description: Orden no encontrada.
      500:
        description: Error interno.
    """
    try:
        details = get_order_details(order_id)
        if details is None:
            return jsonify({"error": "Orden no encontrada"}), 404
        return jsonify(details), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@order_bp.route('/<int:order_id>', methods=['DELETE'])
def route_delete_order(order_id):
    """
    Eliminar una orden.
    ---
    tags:
      - Orders
    parameters:
      - in: path
        name: order_id
        type: integer
        required: true
        description: ID de la orden a eliminar.
    responses:
      200:
        description: Orden eliminada con éxito.
      500:
        description: Error interno.
    """
    try:
        delete_order(order_id)
        return jsonify({"message": "Orden eliminada con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
