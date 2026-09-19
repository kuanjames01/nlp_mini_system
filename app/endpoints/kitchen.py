from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.data.order_data import ORDER_STATUSES
from app.services.kitchen_service import KitchenService


router = APIRouter(prefix="/kitchen", tags=["Kitchen"])
kitchen_service = KitchenService()


class KitchenOrderStatusUpdate(BaseModel):
	order_status: Literal[
		ORDER_STATUSES[0],
		ORDER_STATUSES[1],
		ORDER_STATUSES[2],
		ORDER_STATUSES[3],
		ORDER_STATUSES[4],
	]


@router.get("/orders")
def get_kitchen_orders():
	return kitchen_service.get_orders()


@router.get("/orders/{order_id}")
def get_kitchen_order(order_id: int):
	order = kitchen_service.get_order(order_id)

	if order is None:
		raise HTTPException(status_code=404, detail="Order not found")

	return order


@router.put("/orders/{order_id}/status")
def update_kitchen_order_status(
	order_id: int,
	status_update: KitchenOrderStatusUpdate,
):
	try:
		order = kitchen_service.update_order_status(
			order_id=order_id,
			order_status=status_update.order_status,
		)
	except ValueError as error:
		raise HTTPException(status_code=400, detail=str(error)) from error

	if order is None:
		raise HTTPException(status_code=404, detail="Order not found")

	return order
