class MenuData:
    """Temporary in-memory menu data.

    This class can later be replaced with a database-backed data source
    without changing the menu endpoints.
    """

    _categories = [
        {"id": 1, "name": "Chicken Meals"},
        {"id": 2, "name": "Chicken Wings"},
        {"id": 3, "name": "Chicken Buckets"},
        {"id": 4, "name": "Chicken Burgers"},
        {"id": 5, "name": "Sides"},
        {"id": 6, "name": "Drinks"},
    ]

    _items = [
        {"id": 1, "name": "1pc Chicken Meal", "price": 99.00, "category_id": 1},
        {"id": 2, "name": "2pc Chicken Meal", "price": 149.00, "category_id": 1},
        {"id": 3, "name": "Chicken Fillet Meal", "price": 129.00, "category_id": 1},
        {"id": 4, "name": "Original Chicken Wings", "price": 129.00, "category_id": 2},
        {"id": 5, "name": "BBQ Chicken Wings", "price": 139.00, "category_id": 2},
        {"id": 6, "name": "Spicy Chicken Wings", "price": 139.00, "category_id": 2},
        {"id": 7, "name": "6pc Chicken Bucket", "price": 399.00, "category_id": 3},
        {"id": 8, "name": "10pc Chicken Bucket", "price": 599.00, "category_id": 3},
        {"id": 9, "name": "Classic Chicken Burger", "price": 119.00, "category_id": 4},
        {"id": 10, "name": "Spicy Chicken Burger", "price": 129.00, "category_id": 4},
        {"id": 11, "name": "French Fries", "price": 69.00, "category_id": 5},
        {"id": 12, "name": "Extra Rice", "price": 35.00, "category_id": 5},
        {"id": 13, "name": "Iced Tea", "price": 49.00, "category_id": 6},
        {"id": 14, "name": "Soft Drink", "price": 45.00, "category_id": 6},
        {"id": 15, "name": "Bottled Water", "price": 30.00, "category_id": 6},
    ]

    def get_categories(self):
        return self._categories

    def get_items(self):
        return self._items

    def get_item_by_id(self, item_id):
        return next((item for item in self._items if item["id"] == item_id), None)