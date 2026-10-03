"""Checkout API: discount checkout over CheckoutService."""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from . import deps

router = APIRouter(prefix="/api/checkout", tags=["checkout"])


class CheckoutIn(BaseModel):
    """Checkout payload (member_id null/blank = guest)."""

    product_id: str = Field(min_length=1)
    member_id: Optional[str] = None
    qty: int = Field(gt=0)


@router.post("")
def checkout(payload: CheckoutIn) -> dict:
    """Checkout with automatic member discount; returns receipt."""
    ok, result, _rest = deps.get_checkout().process_checkout(
        payload.product_id, payload.member_id, payload.qty
    )
    if not ok:
        message = str(result)
        if "not found" in message.lower():
            raise HTTPException(404, message)
        if "not enough stock" in message.lower():
            raise HTTPException(409, message)
        raise HTTPException(400, message)
    if not isinstance(result, dict):
        raise HTTPException(500, "Checkout returned no receipt!")
    return result
