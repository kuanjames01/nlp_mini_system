from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.services.customer_service import CustomerService


router = APIRouter(prefix="/customers", tags=["Customers"])
customer_service = CustomerService()


class CustomerCreate(BaseModel):
    customer_name: str = Field(min_length=1)
    contact_number: str | None = None
    email: str | None = None

    @field_validator("customer_name")
    @classmethod
    def validate_customer_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("customer_name must not be blank")
        return value


class CustomerUpdate(BaseModel):
    customer_name: str | None = Field(default=None, min_length=1)
    contact_number: str | None = None
    email: str | None = None

    @field_validator("customer_name")
    @classmethod
    def validate_customer_name(cls, value):
        if value is None:
            return value

        value = value.strip()
        if not value:
            raise ValueError("customer_name must not be blank")
        return value


@router.post("")
def create_customer(customer: CustomerCreate):
    return customer_service.create_customer(
        customer_name=customer.customer_name,
        contact_number=customer.contact_number,
        email=customer.email,
    )


@router.get("/{customer_id}")
def get_customer(customer_id: int):
    customer = customer_service.get_customer(customer_id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


@router.put("/{customer_id}")
def update_customer(customer_id: int, customer: CustomerUpdate):
    customer_data = customer.model_dump(exclude_unset=True)

    if not customer_data:
        raise HTTPException(
            status_code=400,
            detail="At least one customer field is required",
        )

    updated_customer = customer_service.update_customer(customer_id, customer_data)

    if updated_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return updated_customer
