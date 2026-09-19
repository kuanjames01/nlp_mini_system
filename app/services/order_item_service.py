from app.data.order_item_data import OrderItemData


class OrderItemService:
    """Business logic for order item operations."""

    def __init__(self):
        self.order_item_data = OrderItemData()

    def add_order_item(self, order_id, item_id, quantity):
        if quantity <= 0:
            raise ValueError("quantity must be greater than 0")

        if self.order_item_data.get_order(order_id) is None:
            return None

        menu_item = self.order_item_data.get_menu_item(item_id)
        if menu_item is None or not menu_item["is_available"]:
            return None

        return self.order_item_data.create_order_item(
            order_id=order_id,
            item_id=item_id,
            quantity=quantity,
            unit_price=menu_item["price"],
        )

    def get_order_items(self, order_id):
        return self.order_item_data.get_order_items(order_id)

    def delete_order_item(self, order_item_id):
        return self.order_item_data.delete_order_item(order_item_id)