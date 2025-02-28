from flask import jsonify
from models.order_model import Order

# Usamos un diccionario para simular un almacenamiento de pedidos
orders = {}

def order(item):
    if item:
        # Creamos un nuevo pedido y lo guardamos en el diccionario
        new_order = Order(item)
        order_id = len(orders) + 1  # Generamos un ID de pedido simple
        orders[order_id] = new_order
        return jsonify({"message": f"Has pedido {item}. ¿Te gustaría confirmar? (sí/no)"}), 200
    else:
        return jsonify({"error": "No se recibió ningún pedido. ¿Qué te gustaría ordenar?"}), 400
