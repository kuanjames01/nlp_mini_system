from app.db import get_db_connection


class OrderService:
    """Business logic for order operations."""

    def _customer_exists(self, customer_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT customer_id FROM customers WHERE customer_id = %s",
                (customer_id,),
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            connection.close()

    def create_order(self, customer_id, payment_method):
        if not self._customer_exists(customer_id):
            return None

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO orders (customer_id, payment_method)
                VALUES (%s, %s)
                """,
                (customer_id, payment_method),
            )
            connection.commit()
            return self.get_order(cursor.lastrowid)
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    def get_order(self, order_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT order_id, customer_id, order_status, payment_method,
                       payment_status, total_amount, created_at, updated_at
                FROM orders
                WHERE order_id = %s
                """,
                (order_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    def get_customer_orders(self, customer_id):
        if not self._customer_exists(customer_id):
            return None

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT order_id, customer_id, order_status, payment_method,
                       payment_status, total_amount, created_at, updated_at
                FROM orders
                WHERE customer_id = %s
                ORDER BY created_at DESC
                """,
                (customer_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    def update_order(self, order_id, order_data):
        if self.get_order(order_id) is None:
            return None

        allowed_fields = {"order_status", "payment_method", "payment_status"}
        fields = [field for field in order_data if field in allowed_fields]
        values = [order_data[field] for field in fields]
        assignments = ", ".join(f"{field} = %s" for field in fields)

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                f"UPDATE orders SET {assignments} WHERE order_id = %s",
                (*values, order_id),
            )
            connection.commit()
            return self.get_order(order_id)
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()
