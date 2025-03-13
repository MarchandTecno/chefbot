# routes/menu_routes.py
from flask import Blueprint, request, jsonify
from handlers.menu_handler import (
    get_all_menu_items,
    get_menu_item,
    add_menu_item,
    update_menu_item,
    delete_menu_item
)

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/', methods=['GET'])
def route_get_all_menu_items():
    """
    Obtener todos los platillos del menú.
    ---
    tags:
    - Menu
    responses:
      200:
        description: Lista de platillos del menú.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              description:
                type: string
              price:
                type: number
              available:
                type: boolean
              created_at:
                type: string
                format: date-time
      500:
        description: Error interno.
    """
    try:
        items = get_all_menu_items()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/<int:item_id>', methods=['GET'])
def route_get_menu_item(item_id):
    """
    Obtener un platillo específico por ID.
    ---
    tags:
    - Menu
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID del platillo.
    responses:
      200:
        description: Detalles del platillo.
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            description:
              type: string
            price:
              type: number
            available:
              type: boolean
            created_at:
              type: string
              format: date-time
      404:
        description: Platillo no encontrado.
      500:
        description: Error interno.
    """
    try:
        item = get_menu_item(item_id)
        if item:
            return jsonify(item), 200
        return jsonify({"message": "Item no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/', methods=['POST'])
def route_add_menu_item():
    """
    Agregar un nuevo platillo al menú.
    ---
    tags:
    - Menu
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - description
            - price
            - available
          properties:
            name:
              type: string
            description:
              type: string
            price:
              type: number
            available:
              type: boolean
    responses:
      201:
        description: Platillo agregado correctamente.
      500:
        description: Error al agregar el platillo.
    """
    data = request.get_json()
    try:
        add_menu_item(data)
        return jsonify({"message": "Platillo agregado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/<int:item_id>', methods=['PUT'])
def route_update_menu_item(item_id):
    """
    Actualizar un platillo existente.
    ---
    tags:
    - Menu
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID del platillo a actualizar.
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            price:
              type: number
            available:
              type: boolean
    responses:
      200:
        description: Platillo actualizado correctamente.
      500:
        description: Error al actualizar el platillo.
    """
    data = request.get_json()
    try:
        update_menu_item(item_id, data)
        return jsonify({"message": "Platillo actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@menu_bp.route('/<int:item_id>', methods=['DELETE'])
def route_delete_menu_item(item_id):
    """
    Eliminar un platillo del menú.
    ---
    tags:
    - Menu
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID del platillo a eliminar.
    responses:
      200:
        description: Platillo eliminado correctamente.
      500:
        description: Error al eliminar el platillo.
    """
    try:
        delete_menu_item(item_id)
        return jsonify({"message": "Platillo eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
