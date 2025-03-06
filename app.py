# app.py (flujo simple)
from flask import Flask, request, jsonify
from flask import jsonify
from models.user_model import User
from models.order_model import Order
from models.menu_item_model import MenuItem
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

# Datos simulados para pruebas
menu = [
    MenuItem("Pizza", "Pizza de queso con orilla rellena", 120),
    MenuItem("Hamburguesa", "Carne de res, lechuga, tomate y aderezos", 80),
    MenuItem("Tacos", "3 tacos de pastor con piña", 60)
]

users = {}

@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()
    user_id = data.get("user_id")
    name = data.get("name")
    phone = data.get("phone")

    if user_id not in users:
        users[user_id] = User(user_id, name, phone)
        users[user_id].start_order()
        return jsonify({"message": f"¡Hola, {name}! ¿Te gustaría ver el menú? (sí/no)"})
    else:
        return jsonify({"message": "Ya tienes una sesión activa."})

@app.route("/menu", methods=["GET"])
def show_menu():
    menu_items = [f"{item.name} - ${item.price}" for item in menu]
    return jsonify({"menu": menu_items})

@app.route("/order", methods=["POST"])
def place_order():
    data = request.get_json()
    user_id = data.get("user_id")
    item_name = data.get("item")
    quantity = data.get("quantity", 1)

    user = users.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    item = next((item for item in menu if item.name == item_name), None)
    if item and item.available:
        user.add_to_order({"item": item, "quantity": quantity})
        return jsonify({"message": f"{quantity}x {item_name} añadido al pedido. ¿Quieres pedir algo más o confirmar? (confirmar/cancelar)"})
    else:
        return jsonify({"error": "Platillo no disponible"}), 404

@app.route("/confirm", methods=["POST"])
def confirm_order():
    data = request.get_json()
    user_id = data.get("user_id")
    
    user = users.get(user_id)
    if not user or not user.current_order:
        return jsonify({"error": "No tienes un pedido activo"}), 404

    order = Order(user_id)
    for item in user.current_order:
        order.add_item(item['item'], item['quantity'])
    order.complete_order()

    total = order.get_total()
    user.clear_order()
    return jsonify({"message": f"Pedido confirmado. Total: ${total}. ¡Gracias por tu compra!"})

@app.route("/ping_db", methods=["GET"])
def ping_db():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"message": "Conexión a la base de datos exitosa"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
