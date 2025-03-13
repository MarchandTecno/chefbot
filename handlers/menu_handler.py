# handlers/menu_handler.py
from db_init import db
from sqlalchemy import text

def get_all_menu_items():
    """
    Ejecuta el procedimiento almacenado GetAllMenuItems y devuelve una lista de diccionarios con los platillos.
    """
    try:
        result = db.session.execute(text("CALL GetAllMenuItems()"))
        items = [dict(row._mapping) for row in result]
        return items
    except Exception as e:
        raise Exception(f"Error al obtener el menú: {str(e)}")

def get_menu_item(item_id):
    """
    Ejecuta el procedimiento almacenado GetMenuItem para obtener los detalles de un platillo por su ID.
    """
    try:
        result = db.session.execute(text("CALL GetMenuItem(:item_id)"), {"item_id": item_id})
        row = result.fetchone()
        if row:
            return dict(row._mapping)
        return None
    except Exception as e:
        raise Exception(f"Error al obtener el platillo: {str(e)}")

def add_menu_item(data):
    """
    Ejecuta el procedimiento almacenado AddMenuItem para agregar un nuevo platillo.
    Se espera que 'data' sea un diccionario con las claves:
    - name
    - description
    - price
    - available
    """
    try:
        db.session.execute(
            text("CALL AddMenuItem(:name, :description, :price, :available)"),
            data
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al agregar el platillo: {str(e)}")

def update_menu_item(item_id, data):
    """
    Ejecuta el procedimiento almacenado UpdateMenuItem para actualizar un platillo existente.
    Se espera que 'data' sea un diccionario con las claves:
    - name
    - description
    - price
    - available
    """
    try:
        # Agregamos el item_id a los datos para pasarlo al SP
        data['item_id'] = item_id
        db.session.execute(
            text("CALL UpdateMenuItem(:item_id, :name, :description, :price, :available)"),
            data
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al actualizar el platillo: {str(e)}")

def delete_menu_item(item_id):
    """
    Ejecuta el procedimiento almacenado DeleteMenuItem para eliminar un platillo por su ID.
    """
    try:
        db.session.execute(
            text("CALL DeleteMenuItem(:item_id)"),
            {"item_id": item_id}
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al eliminar el platillo: {str(e)}")
