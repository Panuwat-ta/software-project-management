"""Products API: thin REST wrapper over InventoryRepository."""

import csv
import io

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from . import deps

router = APIRouter(prefix="/api/products", tags=["products"])


class ProductIn(BaseModel):
    """Product payload (mirrors domain Product fields)."""

    product_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    quantity: int = Field(ge=0)
    price: float = Field(ge=0)
    category: str = "General"
    barcode: str = ""
    reorder_point: int = Field(default=5, ge=0)


class CutIn(BaseModel):
    """Stock-cut payload."""

    qty: int = Field(gt=0)


def to_dict(product) -> dict:
    """Serialise a domain Product for JSON responses."""
    return {
        "product_id": product.product_id,
        "name": product.name,
        "quantity": product.quantity,
        "price": product.price,
        "category": product.category,
        "barcode": product.barcode,
        "reorder_point": product.reorder_point,
        "low_stock": product.is_low_stock,
    }


@router.get("", response_model=list)
def list_products() -> list:
    """List every product ordered by id."""
    return [to_dict(p) for p in deps.get_repo().find_all()]


@router.post("", status_code=201)
def upsert_product(payload: ProductIn) -> dict:
    """Insert or overwrite a product (same semantics as CLI)."""
    repo = deps.get_repo()
    repo.save(
        deps.domain.Product(
            payload.product_id.strip(),
            payload.name.strip(),
            payload.quantity,
            payload.price,
            payload.category.strip() or "General",
            payload.barcode,
            payload.reorder_point,
        )
    )
    saved = repo.find_by_id(payload.product_id.strip())
    if saved is None:
        raise HTTPException(500, "Failed to persist product!")
    return to_dict(saved)


@router.get("/{product_id}")
def get_product(product_id: str) -> dict:
    """Fetch one product; 404 when missing (never SQL)."""
    found = deps.get_repo().find_by_id(product_id)
    if found is None:
        raise HTTPException(404, "Product not found!")
    return to_dict(found)


@router.put("/{product_id}")
def update_product(product_id: str, payload: ProductIn) -> dict:
    """Full update addressed by path id (upsert semantics)."""
    data = payload.model_dump()
    data["product_id"] = product_id
    return upsert_product(ProductIn(**data))


@router.delete("/{product_id}")
def delete_product(product_id: str) -> dict:
    """Delete a product; 404 when the id is unknown."""
    removed = deps.get_repo().delete(product_id)
    if not removed:
        raise HTTPException(404, "Product not found!")
    return {"deleted": product_id}


@router.post("/{product_id}/cut")
def cut_stock(product_id: str, payload: CutIn) -> dict:
    """Cut stock; 404 unknown id, 409 insufficient stock."""
    repo = deps.get_repo()
    product = repo.find_by_id(product_id)
    if product is None:
        raise HTTPException(404, "Product not found!")
    if product.quantity < payload.qty:
        raise HTTPException(
            409,
            f"Error: Not enough stock! "
            f"(have {product.quantity})",
        )
    repo.update_stock(product_id, product.quantity - payload.qty)
    updated = repo.find_by_id(product_id)
    if updated is None:
        raise HTTPException(500, "Failed to reload product!")
    return to_dict(updated)


def build_csv() -> str:
    """Render the inventory CSV report in memory."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(deps.domain.CSV_HEADER)
    for prod in deps.get_repo().find_all():
        writer.writerow(
            [
                prod.product_id,
                prod.name,
                prod.barcode,
                prod.quantity,
                prod.reorder_point,
                f"{prod.price:.2f}",
            ]
        )
    return buffer.getvalue()
