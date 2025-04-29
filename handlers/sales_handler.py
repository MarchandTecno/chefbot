# handlers/sales_handler.py
from db_init import db
from sqlalchemy import text
from datetime import datetime

def get_all_sales():
    """
    Llama al procedimiento GetAllSales para obtener todas las ventas.
    Retorna una lista de diccionarios.
    """
    try:
        result = db.session.execute(text("CALL GetAllSales()"))
        sales = [dict(row._mapping) for row in result]
        return sales
    except Exception as e:
        raise Exception(f"Error al obtener todas las ventas: {str(e)}")

def get_sale_by_id(sale_id):
    """
    Llama al procedimiento GetSaleById para obtener una venta por su ID.
    Retorna un diccionario o None si no existe.
    """
    try:
        result = db.session.execute(
            text("CALL GetSaleById(:sale_id)"),
            {"sale_id": sale_id}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None
    except Exception as e:
        raise Exception(f"Error al obtener la venta: {str(e)}")

def create_sale(data):
    """
    Llama al procedimiento CreateSale para insertar una nueva venta.
    Se espera que 'data' contenga:
      - total_sales
      - cash_sales
      - card_sales
      - transfer_sales
      - sales_date (YYYY-MM-DD o datetime.date)
    Retorna True si la operación fue exitosa.
    """
    try:
        # Asegurarse de que sales_date sea string YYYY-MM-DD
        if isinstance(data.get("sales_date"), datetime):
            data["sales_date"] = data["sales_date"].date().isoformat()
        db.session.execute(
            text(
                "CALL CreateSale("
                ":total_sales, :cash_sales, :card_sales, :transfer_sales, :sales_date)"
            ),
            data
        )
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al crear la venta: {str(e)}")

def update_sale(sale_id, data):
    """
    Llama al procedimiento UpdateSale para modificar una venta existente.
    Se espera que 'data' contenga:
      - total_sales
      - cash_sales
      - card_sales
      - transfer_sales
      - sales_date
    Retorna True si la operación fue exitosa.
    """
    try:
        if isinstance(data.get("sales_date"), datetime):
            data["sales_date"] = data["sales_date"].date().isoformat()
        data["sale_id"] = sale_id
        db.session.execute(
            text(
                "CALL UpdateSale("
                ":sale_id, :total_sales, :cash_sales, :card_sales, :transfer_sales, :sales_date)"
            ),
            data
        )
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al actualizar la venta: {str(e)}")

def delete_sale(sale_id):
    """
    Llama al procedimiento DeleteSale para eliminar una venta.
    Retorna True si la operación fue exitosa.
    """
    try:
        db.session.execute(
            text("CALL DeleteSale(:sale_id)"),
            {"sale_id": sale_id}
        )
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error al eliminar la venta: {str(e)}")

def get_sales_by_date_range(start_date, end_date):
    """
    Llama al procedimiento GetSalesByDateRange para obtener ventas
    entre dos fechas (inclusive).
    'start_date' y 'end_date' pueden ser strings 'YYYY-MM-DD' o date.
    Retorna una lista de diccionarios.
    """
    try:
        # Normalizar fechas a string
        if isinstance(start_date, datetime):
            start_date = start_date.date().isoformat()
        if isinstance(end_date, datetime):
            end_date = end_date.date().isoformat()
        result = db.session.execute(
            text("CALL GetSalesByDateRange(:start_date, :end_date)"),
            {"start_date": start_date, "end_date": end_date}
        )
        return [dict(row._mapping) for row in result]
    except Exception as e:
        raise Exception(f"Error al obtener ventas por rango de fechas: {str(e)}")

def get_daily_sales_totals(sales_date):
    """
    Llama al procedimiento GetDailySalesTotals para obtener los totales de ventas
    de una fecha específica.
    'sales_date' puede ser string 'YYYY-MM-DD' o date.
    Retorna un diccionario con los totales o None si no hay datos.
    """
    try:
        if isinstance(sales_date, datetime):
            sales_date = sales_date.date().isoformat()
        result = db.session.execute(
            text("CALL GetDailySalesTotals(:sales_date)"),
            {"sales_date": sales_date}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None
    except Exception as e:
        raise Exception(f"Error al obtener totales diarios de ventas: {str(e)}")
