from flask import Flask, request, jsonify
from handlers.start_handler import start
from handlers.menu_handler import show_menu
from handlers.order_handler import order

app = Flask(__name__)

@app.route('/start', methods=['GET'])
def home():
    return start()

@app.route('/menu', methods=['GET'])
def menu():
    return show_menu()

@app.route('/order', methods=['POST'])
def order_request():
    data = request.get_json()
    item = data.get("item")
    return order(item)

if __name__ == '__main__':
    app.run(port=5000)
