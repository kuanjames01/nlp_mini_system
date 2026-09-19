"""Allowed values for order fields."""


ORDER_STATUSES = (
    "Pending",
    "Preparing",
    "Ready",
    "Completed",
    "Cancelled",
)

PAYMENT_METHODS = (
    "Cash",
    "Online",
)

PAYMENT_STATUSES = (
    "Pending",
    "Paid",
    "Failed",
)
