from fastapi import APIRouter, HTTPException

from app.services.menu_service import MenuService


router = APIRouter(prefix="/menu", tags=["Menu"])
menu_service = MenuService()


@router.get("/categories")
def get_categories():
    return menu_service.get_categories()


@router.get("/items")
def get_items():
    return menu_service.get_items()


@router.get("/items/{item_id}")
def get_item(item_id: int):
    item = menu_service.get_item(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    return item