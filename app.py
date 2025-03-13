from flask import Flask
from flasgger import Swagger
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from db_init import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

# Inicializar Swagger
swagger = Swagger(app)

# Importar rutas
with app.app_context():
    from routes.menu_routes import menu_bp
    from routes.order_routes import order_bp
    from routes.user_routes import user_bp
    from routes.db_routes import db_bp
    from routes.order_item_routes import order_item_bp

    # Registrar los blueprints
    app.register_blueprint(menu_bp, url_prefix="/menu")
    app.register_blueprint(order_bp, url_prefix="/order")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(db_bp, url_prefix="/db")
    app.register_blueprint(order_item_bp, url_prefix="/order_item")

if __name__ == "__main__":
    app.run(debug=True)
