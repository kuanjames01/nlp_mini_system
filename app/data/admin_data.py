from app.db import get_db_connection


class AdminData:
    """Database operations for administrative views."""

    def get_dashboard(self):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT
                    (SELECT COUNT(*) FROM customers) AS total_customers,
                    (SELECT COUNT(*) FROM orders) AS total_orders,
                    (SELECT COUNT(*) FROM orders WHERE order_status = 'Pending')
                        AS pending_orders,
                    (SELECT COUNT(*) FROM orders WHERE order_status = 'Preparing')
                        AS preparing_orders,
                    (SELECT COUNT(*) FROM orders WHERE order_status = 'Ready')
                        AS ready_orders,
                    (SELECT COUNT(*) FROM orders WHERE order_status = 'Completed')
                        AS completed_orders,
                    (SELECT COUNT(*) FROM orders WHERE order_status = 'Cancelled')
                        AS cancelled_orders,
                    (SELECT COALESCE(SUM(amount), 0)
                     FROM payments
                     WHERE payment_status = 'Paid') AS total_revenue
                """
            )
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    def get_orders(self):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(
                """
                SELECT o.order_id, o.customer_id, c.customer_name,
                       o.order_status, o.payment_method, o.payment_status,
                       o.total_amount, o.created_at, o.updated_at,
                       oi.order_item_id, oi.item_id, mi.item_name,
                       oi.quantity, oi.unit_price, oi.subtotal
                FROM orders o
                JOIN customers c ON c.customer_id = o.customer_id
                LEFT JOIN order_items oi ON oi.order_id = o.order_id
                LEFT JOIN menu_items mi ON mi.item_id = oi.item_id
                ORDER BY o.created_at DESC, oi.order_item_id
                """
            )
            rows = cursor.fetchall()
            orders = {}

            for row in rows:
                order_id = row["order_id"]
                order = orders.setdefault(
                    order_id,
                    {
                        "order_id": order_id,
                        "customer_id": row["customer_id"],
                        "customer_name": row["customer_name"],
                        "order_status": row["order_status"],
                        "payment_method": row["payment_method"],
                        "payment_status": row["payment_status"],
                        "total_amount": row["total_amount"],
                        "created_at": row["created_at"],
                        "updated_at": row["updated_at"],
                        "order_items": [],
                    },
                )

                if row["order_item_id"] is not None:
                    order["order_items"].append(
                        {
                            "order_item_id": row["order_item_id"],
                            "item_id": row["item_id"],
                            "item_name": row["item_name"],
                            "quantity": row["quantity"],
                            "unit_price": row["unit_price"],
                            "subtotal": row["subtotal"],
                        }
                    )

            return list(orders.values())
        finally:
            cursor.close()
            connection.close()