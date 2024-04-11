class Order:
    def __init__(self, order_id, current_system_time, order_value, delivery_time):
        self.order_id = order_id
        self.current_system_time = current_system_time
        self.order_value = order_value
        self.delivery_time = delivery_time
        self.priority = self.calculate_priority()
        self.eta = 9999

    def calculate_priority(self):
        value_weight = 0.3
        time_weight = 0.7
        normalized_order_value = self.order_value / 50
        priority = value_weight * normalized_order_value - time_weight * self.current_system_time
        return priority

    def set_eta(self, eta):
        self.eta = eta
