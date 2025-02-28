# models/order_model.py

# Esta es una clase simple para manejar los pedidos
class Order:
    def __init__(self, item, status='pendiente'):
        self.item = item
        self.status = status
    
    def confirm(self):
        self.status = 'confirmado'
    
    def __repr__(self):
        return f"Pedido: {self.item} - Estado: {self.status}"
