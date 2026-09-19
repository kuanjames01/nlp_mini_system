from app.data.payment_data import PaymentData


class PaymentService:
    """Business logic for payments."""

    def __init__(self):
        self.payment_data = PaymentData()

    def create_payment(
        self,
        order_id,
        payment_method,
        amount,
        transaction_reference=None,
        paid_at=None,
    ):
        if amount <= 0:
            raise ValueError("amount must be greater than 0")

        if self.payment_data.get_order(order_id) is None:
            return None

        return self.payment_data.create_payment(
            order_id=order_id,
            payment_method=payment_method,
            amount=amount,
            transaction_reference=transaction_reference,
            paid_at=paid_at,
        )

    def get_payment(self, payment_id):
        return self.payment_data.get_payment(payment_id)

    def get_order_payments(self, order_id):
        return self.payment_data.get_order_payments(order_id)

    def update_payment(self, payment_id, payment_data):
        if self.payment_data.get_payment(payment_id) is None:
            return None

        return self.payment_data.update_payment(payment_id, payment_data)
