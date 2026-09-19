from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.order_item_service import OrderItemService


router = APIRouter(prefix="/orders", tags=["Order Items"])
order_item_service = OrderItemService()


class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int


@router.post("/{order_id}/items")
def add_order_item(order_id: int, order_item: OrderItemCreate):
    try:
        created_order_item = order_item_service.add_order_item(
            order_id=order_id,
            item_id=order_item.item_id,
            quantity=order_item.quantity,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    if created_order_item is None:
        raise HTTPException(
            status_code=404,
            detail="Order or available menu item not found",
        )

    return created_order_item


@router.get("/{order_id}/items")
def get_order_items(order_id: int):
    return order_item_service.get_order_items(order_id)


@router.delete("/items/{order_item_id}")
def delete_order_item(order_item_id: int):
    deleted = order_item_service.delete_order_item(order_item_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Order item not found")

    return {"message": "Order item deleted successfully"}