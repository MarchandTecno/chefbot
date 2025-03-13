# handlers/user_handler.py

from models.user_model import User
from db_init import db

def get_or_create_user(data):
    """
    Busca un usuario por su id y, si no existe, lo crea.
    Se espera que 'data' contenga:
      - user_id: Identificador único del usuario (int o str)
      - name: Nombre del usuario
      - phone: Teléfono del usuario (opcional)
    Retorna un diccionario con la información del usuario.
    """
    user_id = data.get("user_id")
    name = data.get("name")
    phone = data.get("phone", "")

    # Buscar el usuario en la base de datos
    user = User.query.filter_by(id=user_id).first()
    if not user:
        user = User(id=user_id, name=name, phone=phone)
        db.session.add(user)
        db.session.commit()
    # Retornar una representación del usuario
    return {"id": user.id, "name": user.name, "phone": user.phone}

def get_user(user_id):
    """
    Retorna los datos de un usuario a partir de su ID.
    """
    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise Exception("Usuario no encontrado")
    return {"id": user.id, "name": user.name, "phone": user.phone}

def update_user(user_id, data):
    """
    Actualiza la información de un usuario.
    Se espera que 'data' contenga los campos a actualizar, por ejemplo:
      - name
      - phone
    """
    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise Exception("Usuario no encontrado")
    if "name" in data:
        user.name = data["name"]
    if "phone" in data:
        user.phone = data["phone"]
    db.session.commit()
    return {"id": user.id, "name": user.name, "phone": user.phone}

def delete_user(user_id):
    """
    Elimina un usuario de la base de datos.
    """
    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise Exception("Usuario no encontrado")
    db.session.delete(user)
    db.session.commit()
    return True
