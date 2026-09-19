from app.db import get_db_connection


class PaymentData:
    """Database operations for payments."""

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

    def create_payment(
        self,
        order_id,
        payment_method,
        amount,
        transaction_reference=None,
        paid_at=None,
    ):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO payments (
                    order_id, payment_method, amount,
                    transaction_reference, paid_at
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    order_id,
                    payment_method,
                    amount,
                    transaction_reference,
                    paid_at,
                ),
            )
            connection.commit()
            return self.get_payment(cursor.lastrowid)
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    def get_payment(self, payment_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT payment_id, order_id, payment_method, payment_status,
                       amount, transaction_reference, paid_at
                FROM payments
                WHERE payment_id = %s
                """,
                (payment_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    def get_order_payments(self, order_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT payment_id, order_id, payment_method, payment_status,
                       amount, transaction_reference, paid_at
                FROM payments
                WHERE order_id = %s
                ORDER BY payment_id
                """,
                (order_id,),
            )
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    def update_payment(self, payment_id, payment_data):
        fields = list(payment_data)
        values = [payment_data[field] for field in fields]
        assignments = ", ".join(f"{field} = %s" for field in fields)

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                f"UPDATE payments SET {assignments} WHERE payment_id = %s",
                (*values, payment_id),
            )
            connection.commit()
            return self.get_payment(payment_id)
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()
