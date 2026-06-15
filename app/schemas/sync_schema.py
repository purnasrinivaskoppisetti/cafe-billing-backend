from pydantic import BaseModel
from typing import List
from datetime import datetime


class TransactionItemRequest(BaseModel):
    product_id: str
    name: str
    rate: float
    qty: int


class TransactionRequest(BaseModel):
    id: str
    bill_number: str
    total_items: int
    sub_total: float
    discount: float
    grand_total: float
    payment_method: str
    created_at: datetime


class SyncRequest(BaseModel):
    device_id: str
    transaction: TransactionRequest
    items: List[TransactionItemRequest]