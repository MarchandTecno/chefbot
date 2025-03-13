# routes/db_routes.py
from flask import Blueprint, jsonify
from db_init import db  # Cambiamos la importación para evitar el ciclo
from models.menu_item_model import MenuItem

db_bp = Blueprint('db', __name__)

@db_bp.route("/create_tables", methods=["GET"])
def create_tables():
    try:
        db.create_all()
        return jsonify({"message": "Tablas creadas con éxito."})
    except Exception as e:
        return jsonify({"error": str(e)})
