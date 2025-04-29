# routes/sales_routes.py
from flask import Blueprint, request, jsonify
from handlers.sales_handler import (
    get_all_sales,
    get_sale_by_id,
    create_sale,
    update_sale,
    delete_sale,
    get_sales_by_date_range,
    get_daily_sales_totals
)

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/', methods=['GET'])
def route_get_all_sales():
    """
    Obtener todas las ventas.
    ---
    tags:
      - Sales
    responses:
      200:
        description: Lista de todas las ventas.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              total_sales:
                type: number
              cash_sales:
                type: number
              card_sales:
                type: number
              transfer_sales:
                type: number
              sales_date:
                type: string
                format: date
              created_at:
                type: string
                format: date-time
      500:
        description: Error interno.
    """
    try:
        sales = get_all_sales()
        return jsonify(sales), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sales_bp.route('/<int:sale_id>', methods=['GET'])
def route_get_sale_by_id(sale_id):
    """
    Obtener una venta por su ID.
    ---
    tags:
      - Sales
    parameters:
      - name: sale_id
        in: path
        type: integer
        required: true
        description: ID de la venta.
    responses:
      200:
        description: Detalles de la venta.
        schema:
          type: object
          properties:
            id:
              type: integer
            total_sales:
              type: number
            cash_sales:
              type: number
            card_sales:
              type: number
            transfer_sales:
              type: number
            sales_date:
              type: string
              format: date
            created_at:
              type: string
              format: date-time
      404:
        description: Venta no encontrada.
      500:
        description: Error interno.
    """
    try:
        sale = get_sale_by_id(sale_id)
        if sale is None:
            return jsonify({"error": "Venta no encontrada"}), 404
        return jsonify(sale), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sales_bp.route('/', methods=['POST'])
def route_create_sale():
    """
    Crear una nueva venta.
    ---
    tags:
      - Sales
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - total_sales
            - cash_sales
            - card_sales
            - transfer_sales
            - sales_date
          properties:
            total_sales:
              type: number
              example: 1000.00
            cash_sales:
              type: number
              example: 400.00
            card_sales:
              type: number
              example: 500.00
            transfer_sales:
              type: number
              example: 100.00
            sales_date:
              type: string
              format: date
              example: "2025-04-28"
    responses:
      201:
        description: Venta creada correctamente.
        schema:
          type: object
          properties:
            message:
              type: string
            success:
              type: boolean
      500:
        description: Error interno.
    """
    data = request.get_json()
    try:
        # validación mínima
        required = ["total_sales", "cash_sales", "card_sales", "transfer_sales", "sales_date"]
        if not all(k in data for k in required):
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        create_sale(data)
        return jsonify({"message": "Venta creada correctamente", "success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sales_bp.route('/<int:sale_id>', methods=['PUT'])
def route_update_sale(sale_id):
    """
    Actualizar una venta existente.
    ---
    tags:
      - Sales
    parameters:
      - in: path
        name: sale_id
        type: integer
        required: true
        description: ID de la venta a actualizar.
      - in: body
        name: body
        schema:
          type: object
          properties:
            total_sales:
              type: number
            cash_sales:
              type: number
            card_sales:
              type: number
            transfer_sales:
              type: number
            sales_date:
              type: string
              format: date
    responses:
      200:
        description: Venta actualizada correctamente.
        schema:
          type: object
          properties:
            message:
              type: string
            success:
              type: boolean
      400:
        description: Datos de entrada inválidos.
      500:
        description: Error interno.
    """
    data = request.get_json()
    try:
        # al menos uno
        if not any(k in data for k in ["total_sales", "cash_sales", "card_sales", "transfer_sales", "sales_date"]):
            return jsonify({"error": "Debe incluir al menos un campo para actualizar"}), 400

        update_sale(sale_id, data)
        return jsonify({"message": "Venta actualizada correctamente", "success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sales_bp.route('/<int:sale_id>', methods=['DELETE'])
def route_delete_sale(sale_id):
    """
    Eliminar una venta.
    ---
    tags:
      - Sales
    parameters:
      - in: path
        name: sale_id
        type: integer
        required: true
        description: ID de la venta a eliminar.
    responses:
      200:
        description: Venta eliminada correctamente.
        schema:
          type: object
          properties:
            message:
              type: string
            success:
              type: boolean
      500:
        description: Error interno.
    """
    try:
        delete_sale(sale_id)
        return jsonify({"message": "Venta eliminada correctamente", "success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sales_bp.route('/range', methods=['GET'])
def route_get_sales_by_date_range():
    """
    Obtener ventas en un rango de fechas.
    ---
    tags:
      - Sales
    parameters:
      - in: query
        name: start_date
        type: string
        format: date
        required: true
        description: Fecha de inicio (YYYY-MM-DD).
      - in: query
        name: end_date
        type: string
        format: date
        required: true
        description: Fecha de fin (YYYY-MM-DD).
    responses:
      200:
        description: Ventas en el rango proporcionado.
        schema:
          type: array
          items:
            type: object
      400:
        description: Parámetros inválidos.
      500:
        description: Error interno.
    """
    start = request.args.get("start_date")
    end = request.args.get("end_date")
    if not start or not end:
        return jsonify({"error": "Debe proporcionar start_date y end_date"}), 400
    try:
        sales = get_sales_by_date_range(start, end)
        return jsonify(sales), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@sales_bp.route('/daily/<string:sales_date>', methods=['GET'])
def route_get_daily_sales_totals(sales_date):
    """
    Obtener totales de ventas para una fecha específica.
    ---
    tags:
      - Sales
    parameters:
      - name: sales_date
        in: path
        type: string
        format: date
        required: true
        description: Fecha de ventas (YYYY-MM-DD).
    responses:
      200:
        description: Totales diarios de ventas.
        schema:
          type: object
          properties:
            sales_date:
              type: string
            total_sales:
              type: number
            cash_sales:
              type: number
            card_sales:
              type: number
            transfer_sales:
              type: number
      404:
        description: No hay ventas en la fecha.
      500:
        description: Error interno.
    """
    try:
        totals = get_daily_sales_totals(sales_date)
        if totals is None:
            return jsonify({"error": "No hay datos para esa fecha"}), 404
        return jsonify(totals), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

