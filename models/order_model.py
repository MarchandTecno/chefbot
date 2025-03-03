# models/order_model.py
class Order:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = []
        self.status = "pending"

    def add_item(self, item, quantity=1):
        self.items.append({
            "item": item,
            "quantity": quantity
        })

    def get_total(self):
        return sum(item['item'].price * item['quantity'] for item in self.items)

    def complete_order(self):
        self.status = "completed"