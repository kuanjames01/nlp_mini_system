from app.data.menu_data import MenuData


class MenuService:
    """Business logic for menu operations."""

    def __init__(self):
        self.menu_data = MenuData()

    def get_categories(self):
        return self.menu_data.get_categories()

    def get_items(self):
        return self.menu_data.get_items()

    def get_item(self, item_id):
        return self.menu_data.get_item_by_id(item_id)