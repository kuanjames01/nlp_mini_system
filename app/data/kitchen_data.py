from app.db import get_db_connection


class KitchenData:
    """Database operations for kitchen orders."""

    def _build_orders(self, query, parameters=()):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute(query, parameters)
            rows = cursor.fetchall()
            orders = {}

            for row in rows:
                order_id = row["order_id"]
                order = orders.setdefault(
                    order_id,
                    {
                        "order_id": order_id,
                        "customer_id": row["customer_id"],
                        "order_status": row["order_status"],
                        "payment_method": row["payment_method"],
                        "payment_status": row["payment_status"],
                        "total_amount": row["total_amount"],
                        "created_at": row["created_at"],
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

    def get_orders(self):
        return self._build_orders(
            """
            SELECT o.order_id, o.customer_id, o.order_status,
                   o.payment_method, o.payment_status, o.total_amount,
                   o.created_at, oi.order_item_id, oi.item_id,
                   mi.item_name, oi.quantity, oi.unit_price, oi.subtotal
            FROM orders o
            LEFT JOIN order_items oi ON oi.order_id = o.order_id
            LEFT JOIN menu_items mi ON mi.item_id = oi.item_id
            WHERE o.order_status IN ('Pending', 'Preparing', 'Ready')
            ORDER BY o.created_at DESC, oi.order_item_id
            """
        )

    def get_order(self, order_id):
        orders = self._build_orders(
            """
            SELECT o.order_id, o.customer_id, o.order_status,
                   o.payment_method, o.payment_status, o.total_amount,
                   o.created_at, oi.order_item_id, oi.item_id,
                   mi.item_name, oi.quantity, oi.unit_price, oi.subtotal
            FROM orders o
            LEFT JOIN order_items oi ON oi.order_id = o.order_id
            LEFT JOIN menu_items mi ON mi.item_id = oi.item_id
            WHERE o.order_id = %s
            ORDER BY oi.order_item_id
            """,
            (order_id,),
        )
        return orders[0] if orders else None

    def update_order_status(self, order_id, order_status):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE orders
                SET order_status = %s
                WHERE order_id = %s
                """,
                (order_status, order_id),
            )
            connection.commit()
            return cursor.rowcount > 0
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()