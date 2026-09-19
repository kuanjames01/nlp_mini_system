from fastapi import APIRouter

from app.services.admin_service import AdminService


router = APIRouter(prefix="/admin", tags=["Admin"])
admin_service = AdminService()


@router.get("/dashboard")
def get_dashboard():
	return admin_service.get_dashboard()


@router.get("/orders")
def get_orders():
	return admin_service.get_orders()
