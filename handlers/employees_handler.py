# handlers/employees_handler.py
from db_init import db
from sqlalchemy import text

def get_all_employees():
    """
    Obtiene todos los empleados usando el procedimiento almacenado GetAllEmployees.
    Retorna una lista de diccionarios.
    """
    try:
        result = db.session.execute(text("CALL GetAllEmployees()"))
        employees = [dict(row._mapping) for row in result]
        return employees
    except Exception as e:
        raise Exception(f"Error obteniendo empleados: {str(e)}")

def get_employee(employee_id):
    """
    Obtiene un empleado por su ID usando el procedimiento almacenado GetEmployee.
    Retorna un diccionario o None si no se encuentra.
    """
    try:
        result = db.session.execute(text("CALL GetEmployee(:employee_id)"), {"employee_id": employee_id})
        row = result.fetchone()
        if row:
            return dict(row._mapping)
        return None
    except Exception as e:
        raise Exception(f"Error obteniendo el empleado: {str(e)}")

def add_employee(data):
    """
    Agrega un nuevo empleado usando el procedimiento almacenado CreateEmployee.
    Se espera que 'data' sea un diccionario con las claves:
      - name: Nombre del empleado.
      - role: Rol (por ejemplo, 'Mesero', 'Cocinero', etc.).
      - phone: Teléfono del empleado.
      - status: Estado del empleado (1 = activo, 0 = inactivo), opcional.
    """

    #Se asigna 1 por defecto si status no esta en los datos recibidos
    data.setdefault("status", 1)

    query = text("CALL CreateEmployee(:name, :role, :phone, :status)")  # Se agrega NOW()
    
    try:
        db.session.execute(query, data)  # Ejecuta la consulta
        db.session.commit()  # Confirma la transacción
    except Exception as e:
        db.session.rollback()  # Revierte si hay error
        raise Exception(f"Error al agregar el empleado: {str(e)}")

def update_employee(employee_id, data):
    """
    Actualiza la información de un empleado usando el procedimiento almacenado UpdateEmployee.
    Se espera que 'data' sea un diccionario con las claves:
      - name (opcional)
      - role (opcional)
      - phone (opcional)
    """
    #Nos aseguramos que status es 0 o es 1
    if "status" in data:
        data["status"] = int(bool(data["status"]))
    try:
        data["employee_id"] = employee_id
        db.session.execute(
            text("CALL UpdateEmployee(:id, :name, :role, :phone, :status)"),
            data
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al actualizar el empleado: {str(e)}")

def delete_employee(employee_id):
    """
    Elimina un empleado usando el procedimiento almacenado DeleteEmployee.
    """

    check_query = text("SELECT COUNT(*) as count FROM orders WHERE employee_id = :employee_id")
    result = db.session.execute(check_query, {"employee_id": employee_id})
    count = result.fetchone()._mapping["count"]

    if count > 0:
        raise Exception("No se puede eliminar el empleado: Existen ordenes asociadas.")
    try:
        db.session.execute(
            text("CALL DeleteEmployee(:employee_id)"),
            {"employee_id": employee_id}
        )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al eliminar el empleado: {str(e)}")
