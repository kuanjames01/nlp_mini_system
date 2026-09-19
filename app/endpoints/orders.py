from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.data.order_data import ORDER_STATUSES, PAYMENT_METHODS, PAYMENT_STATUSES
from app.services.order_service import OrderService


router = APIRouter(prefix="/orders", tags=["Orders"])
order_service = OrderService()


class OrderCreate(BaseModel):
    customer_id: int
    payment_method: Literal[PAYMENT_METHODS[0], PAYMENT_METHODS[1]]


class OrderUpdate(BaseModel):
    order_status: Literal[
        ORDER_STATUSES[0],
        ORDER_STATUSES[1],
        ORDER_STATUSES[2],
        ORDER_STATUSES[3],
        ORDER_STATUSES[4],
    ] | None = None
    payment_method: Literal[PAYMENT_METHODS[0], PAYMENT_METHODS[1]] | None = None
    payment_status: Literal[
        PAYMENT_STATUSES[0],
        PAYMENT_STATUSES[1],
        PAYMENT_STATUSES[2],
    ] | None = None


@router.post("")
def create_order(order: OrderCreate):
    created_order = order_service.create_order(
        customer_id=order.customer_id,
        payment_method=order.payment_method,
    )

    if created_order is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return created_order


@router.get("/{order_id}")
def get_order(order_id: int):
    order = order_service.get_order(order_id)

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.get("/customer/{customer_id}")
def get_customer_orders(customer_id: int):
    orders = order_service.get_customer_orders(customer_id)

    if orders is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return orders


@router.put("/{order_id}")
def update_order(order_id: int, order: OrderUpdate):
    order_data = order.model_dump(exclude_unset=True)

    if not order_data:
        raise HTTPException(
            status_code=400,
            detail="At least one order field is required",
        )

    updated_order = order_service.update_order(order_id, order_data)

    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return updated_order
