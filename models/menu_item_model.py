# models/menu_item_model.py
class MenuItem:
    def __init__(self, name, description, price, available=True):
        self.name = name
        self.description = description
        self.price = price
        self.available = available

    def __repr__(self):
        return f"{self.name} - ${self.price:.2f}"
