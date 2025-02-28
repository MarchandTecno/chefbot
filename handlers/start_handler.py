from flask import jsonify

def start():
    return jsonify({"message": "¡Hola! Soy tu asistente de pedidos. ¿Te gustaría ver el menú?"}), 200
