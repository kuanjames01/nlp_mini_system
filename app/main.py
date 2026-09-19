from fastapi import FastAPI
from app.db import get_db_connection
from app.endpoints.customers import router as customers_router
from app.endpoints.menu import router as menu_router
from app.endpoints.orders import router as orders_router
from app.endpoints.order_items import router as order_items_router
from app.endpoints.payments import router as payments_router
from app.endpoints.kitchen import router as kitchen_router
from app.endpoints.admin import router as admin_router

app = FastAPI(
    title="Chicken Ordering System API",
    description="API for a chicken food ordering system",
    version="1.0.0"
)

app.include_router(menu_router)
app.include_router(customers_router)
app.include_router(orders_router)
app.include_router(order_items_router)
app.include_router(payments_router)
app.include_router(kitchen_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "message": "Chicken Ordering System API is running!"
    }


@app.get("/test-db")
def test_database():
    connection = get_db_connection()

    if connection.is_connected():
        connection.close()

        return {
            "message": "Database connection successful!"
        }

    return {
        "message": "Database connection failed!"
    }