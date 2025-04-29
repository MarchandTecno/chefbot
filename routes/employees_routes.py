from flask import Blueprint, request, jsonify
from handlers.employees_handler import (
    get_all_employees,
    get_employee,
    add_employee,
    update_employee,
    delete_employee
)

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/', methods=['GET'])
def route_get_all_employees():
    """
    Obtener todos los empleados.
    ---
    tags:
      - Employees
    responses:
      200:
        description: Lista de empleados.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              role:
                type: string
              phone:
                type: string
              status:
                type: boolean
              created_at:
                type: string
                format: date-time
      500:
        description: Error interno.
    """
    try:
        employees = get_all_employees()
        return jsonify(employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employees_bp.route('/<int:employee_id>', methods=['GET'])
def route_get_employee(employee_id):
    """
    Obtener un empleado por su ID.
    ---
    tags:
      - Employees
    parameters:
      - name: employee_id
        in: path
        type: integer
        required: true
        description: ID del empleado.
    responses:
      200:
        description: Detalles del empleado.
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            role:
              type: string
            phone:
              type: string
            status:
              type: boolean
            created_at:
              type: string
              format: date-time
      404:
        description: Empleado no encontrado.
      500:
        description: Error interno.
    """
    try:
        employee = get_employee(employee_id)
        if not employee:
            return jsonify({"error": "Empleado no encontrado"}), 404
        return jsonify(employee), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employees_bp.route('/', methods=['POST'])
def route_add_employee():
    """
    Agregar un nuevo empleado.
    ---
    tags:
      - Employees
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - role
            - phone
            - status
          properties:
            name:
              type: string
              example: Pedro Ramírez
            role:
              type: string
              example: Mesero
            phone:
              type: string
              example: '555-1234'
            status:
              type: boolean
              example: 1
    responses:
      201:
        description: Empleado agregado correctamente.
      400:
        description: Datos de entrada inválidos.
      500:
        description: Error interno.
    """
    try:
        data = request.get_json()

        # Validar que los datos requeridos estén presentes
        required_fields = ["name", "role", "phone"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos obligatorios"}), 400
        
        #Si no se envia un "status" se asigna 1 como activo
        data.setdefault("status", 1)

        add_employee(data)
        return jsonify({"message": "Empleado agregado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employees_bp.route('/<int:employee_id>', methods=['PUT'])
def route_update_employee(employee_id):
    """
    Actualizar la información de un empleado.
    ---
    tags:
      - Employees
    parameters:
      - in: path
        name: employee_id
        type: integer
        required: true
        description: ID del empleado a actualizar.
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - role
            - phone
            - status
          properties:
            name:
              type: string
              example: Laura Torres
            role:
              type: string
              example: Cocinera
            phone:
              type: string
              example: '555-5678'
            status:
              type: boolean
              example: false
    responses:
      200:
        description: Empleado actualizado correctamente.
      400:
        description: Datos de entrada inválidos.
      500:
        description: Error interno.
    """
    try:
        data = request.get_json()

        # Validar que al menos un campo esté presente
        if not any(key in data for key in ["name", "role", "phone", "status"]):
            return jsonify({"error": "Debe incluir al menos un campo para actualizar"}), 400

        update_employee(employee_id, data)
        return jsonify({"message": "Empleado actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employees_bp.route('/<int:employee_id>', methods=['DELETE'])
def route_delete_employee(employee_id):
    """
    Eliminar un empleado.
    ---
    tags:
      - Employees
    parameters:
      - in: path
        name: employee_id
        type: integer
        required: true
        description: ID del empleado a eliminar.
    responses:
      200:
        description: Empleado eliminado correctamente.
      404:
        description: Empleado no encontrado o con órdenes asociadas.
      500:
        description: Error interno.
    """
    try:
        result = delete_employee(employee_id)
        if not result:
            return jsonify({"error": "Empleado no encontrado"}), 404

        return jsonify({"message": "Empleado eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
