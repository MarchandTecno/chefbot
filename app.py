from flask import Flask
from flasgger import Swagger
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from db_init import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

# Swagger
swagger = Swagger(app)

# Rutas
with app.app_context():
    from routes.menu_routes import menu_bp
    from routes.employees_routes import employees_bp
    from routes.order_routes import order_bp
    from routes.user_routes import user_bp
    from routes.db_routes import db_bp
    from routes.order_item_routes import order_item_bp
    from routes.payment_routes import payment_bp
    from routes.sales_routes import sales_bp

    # Blueprints
    app.register_blueprint(menu_bp, url_prefix="/menu")
    app.register_blueprint(order_bp, url_prefix="/order")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(employees_bp, url_prefix="/employee")
    app.register_blueprint(db_bp, url_prefix="/db")
    app.register_blueprint(order_item_bp, url_prefix="/order_item")
    app.register_blueprint(payment_bp, url_prefix="/payment")
    app.register_blueprint(sales_bp, url_prefix="/sales")

if __name__ == "__main__":
    app.run(debug=True)
