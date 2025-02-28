# utils/helpers.py

def validate_order_input(input_data):
    """Valida si el dato de entrada es válido (en este caso, que haya un 'item')"""
    if input_data and 'item' in input_data:
        return True
    return False
