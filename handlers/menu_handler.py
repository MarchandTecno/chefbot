from flask import jsonify

def show_menu():
    menu = {
        "Tacos": "$30",
        "Hamburguesa": "$50",
        "Pizza": "$80",
        "Refresco": "$20"
    }
    return jsonify({"menu": menu}), 200
