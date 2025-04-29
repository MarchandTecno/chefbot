# routes/payment_routes.py
from flask import Blueprint, request, jsonify
from handlers.payment_handler import (
    create_payment,
    get_payment,
    get_payments_by_order,
    update_payment,
    delete_payment
)

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/', methods=['POST'])
def route_create_payment():
    """
    Crear un nuevo pago.
    ---
    tags:
      - Payments
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - order_id
            - payment_method
            - amount
          properties:
            order_id:
              type: integer
              example: 1
            payment_method:
              type: string
              example: Tarjeta
            amount:
              type: number
              example: 250.00
    responses:
      201:
        description: Pago creado correctamente.
        schema:
          type: object
          properties:
            message:
              type: string
            payment_id:
              type: integer
      500:
        description: Error interno.
    """
    data = request.get_json()
    try:
        payment_id = create_payment(data)
        return jsonify({"message": "Pago creado correctamente", "payment_id": payment_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payment_bp.route('/<int:payment_id>', methods=['GET'])
def route_get_payment(payment_id):
    """
    Obtener un pago por su ID.
    ---
    tags:
      - Payments
    parameters:
      - name: payment_id
        in: path
        type: integer
        required: true
        description: ID del pago.
    responses:
      200:
        description: Detalles del pago.
        schema:
          type: object
          properties:
            id:
              type: integer
            order_id:
              type: integer
            payment_method:
              type: string
            amount:
              type: number
            paid_at:
              type: string
              format: date-time
      404:
        description: Pago no encontrado.
      500:
        description: Error interno.
    """
    try:
        payment = get_payment(payment_id)
        if payment is None:
            return jsonify({"error": "Pago no encontrado"}), 404
        return jsonify(payment), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payment_bp.route('/order/<int:order_id>', methods=['GET'])
def route_get_payments_by_order(order_id):
    """
    Obtener todos los pagos asociados a una orden.
    ---
    tags:
      - Payments
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID de la orden.
    responses:
      200:
        description: Lista de pagos asociados a la orden.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              order_id:
                type: integer
              payment_method:
                type: string
              amount:
                type: number
              paid_at:
                type: string
                format: date-time
      500:
        description: Error interno.
    """
    try:
        payments = get_payments_by_order(order_id)
        return jsonify(payments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payment_bp.route('/<int:payment_id>', methods=['PUT'])
def route_update_payment(payment_id):
    """
    Actualizar la información de un pago.
    ---
    tags:
      - Payments
    parameters:
      - in: path
        name: payment_id
        type: integer
        required: true
        description: ID del pago a actualizar.
      - in: body
        name: body
        schema:
          type: object
          properties:
            payment_method:
              type: string
              example: Efectivo
            amount:
              type: number
              example: 300.00
    responses:
      200:
        description: Pago actualizado correctamente.
        schema:
          type: object
          properties:
            message:
              type: string
            payment_id:
              type: integer
      500:
        description: Error interno.
    """
    data = request.get_json()
    try:
        updated_id = update_payment(payment_id, data)
        return jsonify({"message": "Pago actualizado correctamente", "payment_id": updated_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@payment_bp.route('/<int:payment_id>', methods=['DELETE'])
def route_delete_payment(payment_id):
    """
    Eliminar un pago.
    ---
    tags:
      - Payments
    parameters:
      - in: path
        name: payment_id
        type: integer
        required: true
        description: ID del pago a eliminar.
    responses:
      200:
        description: Pago eliminado correctamente.
        schema:
          type: object
          properties:
            message:
              type: string
      500:
        description: Error interno.
    """
    try:
        delete_payment(payment_id)
        return jsonify({"message": "Pago eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
