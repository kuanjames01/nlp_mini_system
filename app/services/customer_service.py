from app.db import get_db_connection


class CustomerService:
    """Business logic for customer operations."""

    def create_customer(self, customer_name, contact_number=None, email=None):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO customers (customer_name, contact_number, email)
                VALUES (%s, %s, %s)
                """,
                (customer_name, contact_number, email),
            )
            connection.commit()
            return self.get_customer(cursor.lastrowid)
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    def get_customer(self, customer_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                SELECT customer_id, customer_name, contact_number, email, created_at
                FROM customers
                WHERE customer_id = %s
                """,
                (customer_id,),
            )
            row = cursor.fetchone()

            if row is None:
                return None

            return dict(zip(cursor.column_names, row))
        finally:
            cursor.close()
            connection.close()

    def update_customer(self, customer_id, customer_data):
        existing_customer = self.get_customer(customer_id)

        if existing_customer is None:
            return None

        allowed_fields = {"customer_name", "contact_number", "email"}
        fields = [field for field in customer_data if field in allowed_fields]
        values = [customer_data[field] for field in fields]
        assignments = ", ".join(f"{field} = %s" for field in fields)

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                f"UPDATE customers SET {assignments} WHERE customer_id = %s",
                (*values, customer_id),
            )
            connection.commit()
            return self.get_customer(customer_id)
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()
