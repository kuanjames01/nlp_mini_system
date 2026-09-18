from fastapi import FastAPI
from app.db import get_db_connection
from app.endpoints.menu import router as menu_router

app = FastAPI(
    title="Chicken Ordering System API",
    description="API for a chicken food ordering system",
    version="1.0.0"
)

app.include_router(menu_router)


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