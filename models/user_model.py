# models/user_model.py
class User:
    def __init__(self, user_id, name, phone_number):
        self.user_id = user_id
        self.name = name
        self.phone_number = phone_number
        self.current_order = None

    def start_order(self):
        self.current_order = []

    def add_to_order(self, item):
        if self.current_order is not None:
            self.current_order.append(item)

    def clear_order(self):
        self.current_order = None