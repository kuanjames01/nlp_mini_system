from app.db import get_db_connection


class OrderItemData:
    """Database operations for order items."""

    def get_order(self, order_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT order_id FROM orders WHERE order_id = %s",
                (order_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    def get_menu_item(self, item_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT item_id, item_name, description, price, is_available
                FROM menu_items
                WHERE item_id = %s
                """,
                (item_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    def create_order_item(self, order_id, item_id, quantity, unit_price):
        subtotal = unit_price * quantity
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO order_items (order_id, item_id, quantity, unit_price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (order_id, item_id, quantity, unit_price, subtotal),
            )
            connection.commit()
            return self.get_order_item(cursor.lastrowid)
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    def get_order_item(self, order_item_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT oi.order_item_id, oi.order_id, oi.item_id,
                       oi.quantity, oi.unit_price, oi.subtotal,
                       mi.item_name, mi.description, mi.price AS current_price
                FROM order_items oi
                JOIN menu_items mi ON mi.item_id = oi.item_id
                WHERE oi.order_item_id = %s
                """,
                (order_item_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    def get_order_items(self, order_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT oi.order_item_id, oi.order_id, oi.item_id,
                       oi.quantity, oi.unit_price, oi.subtotal,
                       mi.item_name, mi.description, mi.price AS current_price
                FROM order_items oi
                JOIN menu_items mi ON mi.item_id = oi.item_id
                WHERE oi.order_id = %s
                ORDER BY oi.order_item_id
                """,
                (order_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    def delete_order_item(self, order_item_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "DELETE FROM order_items WHERE order_item_id = %s",
                (order_item_id,),
            )
            connection.commit()
            return cursor.rowcount > 0
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()