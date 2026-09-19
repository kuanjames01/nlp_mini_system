from app.data.admin_data import AdminData


class AdminService:
    """Business logic for administration."""

    def __init__(self):
        self.admin_data = AdminData()

    def get_dashboard(self):
        return self.admin_data.get_dashboard()

    def get_orders(self):
        return self.admin_data.get_orders()
