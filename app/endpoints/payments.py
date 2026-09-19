from datetime import datetime
from decimal import Decimal
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.payment_service import PaymentService


router = APIRouter(prefix="/payments", tags=["Payments"])
payment_service = PaymentService()


class PaymentCreate(BaseModel):
	order_id: int
	payment_method: Literal["Cash", "Online"]
	amount: Decimal = Field(gt=0)
	transaction_reference: str | None = None
	paid_at: datetime | None = None


class PaymentUpdate(BaseModel):
	payment_status: Literal["Pending", "Paid", "Failed", "Refunded"] | None = None
	transaction_reference: str | None = None
	paid_at: datetime | None = None


@router.post("")
def create_payment(payment: PaymentCreate):
	try:
		created_payment = payment_service.create_payment(
			order_id=payment.order_id,
			payment_method=payment.payment_method,
			amount=payment.amount,
			transaction_reference=payment.transaction_reference,
			paid_at=payment.paid_at,
		)
	except ValueError as error:
		raise HTTPException(status_code=400, detail=str(error)) from error

	if created_payment is None:
		raise HTTPException(status_code=404, detail="Order not found")

	return created_payment


@router.get("/{payment_id}")
def get_payment(payment_id: int):
	payment = payment_service.get_payment(payment_id)

	if payment is None:
		raise HTTPException(status_code=404, detail="Payment not found")

	return payment


@router.get("/order/{order_id}")
def get_order_payments(order_id: int):
	return payment_service.get_order_payments(order_id)


@router.put("/{payment_id}")
def update_payment(payment_id: int, payment: PaymentUpdate):
	payment_data = payment.model_dump(exclude_unset=True)

	if not payment_data:
		raise HTTPException(
			status_code=400,
			detail="At least one payment field is required",
		)

	updated_payment = payment_service.update_payment(payment_id, payment_data)

	if updated_payment is None:
		raise HTTPException(status_code=404, detail="Payment not found")

	return updated_payment
