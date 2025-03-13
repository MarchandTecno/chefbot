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

# Obtener todos los platillos del menú
@menu_bp.route('/', methods=['GET'])
def route_get_all_menu_items():
    try:
        items = get_all_menu_items()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener un platillo específico por ID
@menu_bp.route('/<int:item_id>', methods=['GET'])
def route_get_menu_item(item_id):
    try:
        item = get_menu_item(item_id)
        if item:
            return jsonify(item), 200
        return jsonify({"message": "Item no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Agregar un nuevo platillo
@menu_bp.route('/', methods=['POST'])
def route_add_menu_item():
    data = request.get_json()
    try:
        add_menu_item(data)
        return jsonify({"message": "Platillo agregado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Actualizar un platillo existente
@menu_bp.route('/<int:item_id>', methods=['PUT'])
def route_update_menu_item(item_id):
    data = request.get_json()
    try:
        update_menu_item(item_id, data)
        return jsonify({"message": "Platillo actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Eliminar un platillo
@menu_bp.route('/<int:item_id>', methods=['DELETE'])
def route_delete_menu_item(item_id):
    try:
        delete_menu_item(item_id)
        return jsonify({"message": "Platillo eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
