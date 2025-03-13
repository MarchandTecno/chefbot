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

@order_item_bp.route('/', methods=['POST'])
def route_create_order_item():
    """
    Crear un ítem de orden.
    ---
    tags:
    - Order_Items
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - order_id
            - menu_item_id
            - quantity
            - price
          properties:
            order_id:
              type: integer
              example: 1
            menu_item_id:
              type: integer
              example: 2
            quantity:
              type: integer
              example: 3
            price:
              type: number
              example: 150.00
    responses:
      201:
        description: Ítem de la orden creado con éxito.
        schema:
          type: object
          properties:
            message:
              type: string
            order_item_id:
              type: integer
      500:
        description: Error interno.
    """
    data = request.get_json()
    try:
        order_item_id = create_order_item(
            order_id=data['order_id'],
            menu_item_id=data['menu_item_id'],
            quantity=data['quantity'],
            price=data['price']
        )
        return jsonify({"message": "Ítem de la orden creado con éxito", "order_item_id": order_item_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@order_item_bp.route('/<int:order_item_id>', methods=['GET'])
def route_get_order_item(order_item_id):
    """
    Obtener un ítem de orden por su ID.
    ---
    tags:
    - Order_Items
    parameters:
      - name: order_item_id
        in: path
        type: integer
        required: true
        description: ID del ítem de orden.
    responses:
      200:
        description: Detalles del ítem de orden.
        schema:
          type: object
          properties:
            id:
              type: integer
            order_id:
              type: integer
            menu_item_id:
              type: integer
            quantity:
              type: integer
            subtotal:
              type: number
            created_at:
              type: string
              format: date-time
      404:
        description: Ítem no encontrado.
      500:
        description: Error interno.
    """
    try:
        order_item = get_order_item(order_item_id)
        if order_item is None:
            return jsonify({"error": "Ítem no encontrado"}), 404
        return jsonify(order_item), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@order_item_bp.route('/order/<int:order_id>', methods=['GET'])
def route_get_order_items_by_order(order_id):
    """
    Obtener todos los ítems asociados a una orden.
    ---
    tags:
    - Order_Items
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID de la orden.
    responses:
      200:
        description: Lista de ítems asociados a la orden.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              order_id:
                type: integer
              menu_item_id:
                type: integer
              quantity:
                type: integer
              subtotal:
                type: number
              created_at:
                type: string
                format: date-time
      500:
        description: Error interno.
    """
    try:
        items = get_order_items_by_order(order_id)
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@order_item_bp.route('/<int:order_item_id>', methods=['PUT'])
def route_update_order_item(order_item_id):
    """
    Actualizar un ítem de orden.
    ---
    tags:
    - Order_Items
    parameters:
      - name: order_item_id
        in: path
        type: integer
        required: true
        description: ID del ítem de orden a actualizar.
      - in: body
        name: body
        schema:
          type: object
          properties:
            quantity:
              type: integer
              example: 2
            price:
              type: number
              example: 120.00
            menu_item_id:
              type: integer
              example: 3
    responses:
      200:
        description: Ítem actualizado con éxito.
        schema:
          type: object
          properties:
            message:
              type: string
            order_item_id:
              type: integer
      500:
        description: Error interno.
    """
    data = request.get_json()
    try:
        updated_id = update_order_item(order_item_id, data)
        return jsonify({"message": "Ítem actualizado con éxito", "order_item_id": updated_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@order_item_bp.route('/<int:order_item_id>', methods=['DELETE'])
def route_delete_order_item(order_item_id):
    """
    Eliminar un ítem de orden.
    ---
    tags:
    - Order_Items
    parameters:
      - name: order_item_id
        in: path
        type: integer
        required: true
        description: ID del ítem de orden a eliminar.
    responses:
      200:
        description: Ítem eliminado con éxito.
        schema:
          type: object
          properties:
            message:
              type: string
      500:
        description: Error interno.
    """
    try:
        delete_order_item(order_item_id)
        return jsonify({"message": "Ítem eliminado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
