from app.data.kitchen_data import KitchenData
from app.data.order_data import ORDER_STATUSES


class KitchenService:
    """Business logic for kitchen operations."""

    def __init__(self):
        self.kitchen_data = KitchenData()

    def get_orders(self):
        return self.kitchen_data.get_orders()

    def get_order(self, order_id):
        return self.kitchen_data.get_order(order_id)

    def update_order_status(self, order_id, order_status):
        if order_status not in ORDER_STATUSES:
            raise ValueError("Invalid order status")

        if self.kitchen_data.get_order(order_id) is None:
            return None

        self.kitchen_data.update_order_status(order_id, order_status)
        return self.kitchen_data.get_order(order_id)
