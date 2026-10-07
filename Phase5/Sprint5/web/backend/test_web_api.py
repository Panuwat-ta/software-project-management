"""API tests for the FastAPI layer (Phase A foundation)."""

import os
import sys

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ),
)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from web.backend import deps  # noqa: E402
from web.backend.main import app  # noqa: E402


@pytest.fixture
def client(tmp_path):
    """Isolated API client with a throwaway SQLite file."""
    deps.configure(str(tmp_path / "web.db"))
    with TestClient(app) as handle:
        yield handle
    deps.configure(os.devnull)


def test_health(client):
    """GET /api/health returns ok + version."""
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    assert "version" in res.json()


def test_startup_seeds_defaults(client):
    """Startup seeds the 3 demo products when DB is empty."""
    res = client.get("/api/products")
    assert res.status_code == 200
    ids = {p["product_id"] for p in res.json()}
    assert {"101", "102", "103"} <= ids


def test_product_crud_and_validation(client):
    """Create, read, cut, validation errors and delete."""
    payload = {
        "product_id": "W1",
        "name": "Web Item",
        "quantity": 10,
        "price": 99.0,
        "category": "Test",
        "barcode": "B1",
        "reorder_point": 3,
    }
    created = client.post("/api/products", json=payload)
    assert created.status_code == 201
    assert created.json()["low_stock"] is False

    fetched = client.get("/api/products/W1")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Web Item"

    missing = client.get("/api/products/NOPE")
    assert missing.status_code == 404

    bad = dict(payload, product_id="W2", quantity=-1)
    denied = client.post("/api/products", json=bad)
    assert denied.status_code == 422

    cut = client.post("/api/products/W1/cut", json={"qty": 8})
    assert cut.status_code == 200
    assert cut.json()["quantity"] == 2
    assert cut.json()["low_stock"] is True

    over = client.post("/api/products/W1/cut", json={"qty": 99})
    assert over.status_code == 409

    removed = client.delete("/api/products/W1")
    assert removed.status_code == 200
    assert client.get("/api/products/W1").status_code == 404


def test_summary_and_csv(client):
    """Summary numbers and CSV download match the CLI columns."""
    summary = client.get("/api/summary").json()
    assert summary["total_types"] >= 3
    assert summary["total_value"] > 0

    csv_res = client.get("/api/export.csv")
    assert csv_res.status_code == 200
    first = csv_res.text.splitlines()[0]
    assert first == (
        "ProductID,ProductName,Barcode,Quantity,ReorderPoint,Price"
    )


def test_member_tiers_and_checkout(client):
    """Member CRUD incl. fallback plus Gold checkout receipt."""
    gold = client.post(
        "/api/members",
        json={"member_id": "G1", "name": "Gold", "tier": "Gold"},
    )
    assert gold.status_code == 201
    assert gold.json()["discount_rate"] == 0.10

    tiers = {t["tier"]: t["discount_rate"]
             for t in client.get("/api/members/tiers").json()}
    assert tiers == {
        "Regular": 0.0, "Silver": 0.05, "Gold": 0.10, "Platinum": 0.15,
    }

    odd = client.post(
        "/api/members",
        json={"member_id": "OX", "name": "Odd", "tier": "Diamond"},
    )
    assert odd.json()["tier"] == "Regular"

    client.post(
        "/api/products",
        json={"product_id": "G9", "name": "Gold Item", "quantity": 10,
              "price": 500.0, "category": "T", "barcode": "",
              "reorder_point": 5},
    )
    receipt = client.post(
        "/api/checkout",
        json={"product_id": "G9", "member_id": "G1", "qty": 2},
    )
    assert receipt.status_code == 200
    body = receipt.json()
    assert body["subtotal"] == 1000.0
    assert body["grand_total"] == 900.0

    guest = client.post(
        "/api/checkout",
        json={"product_id": "G9", "member_id": None, "qty": 1},
    )
    assert guest.json()["grand_total"] == 500.0

    empty = client.post(
        "/api/checkout",
        json={"product_id": "G9", "member_id": None, "qty": 99},
    )
    assert empty.status_code == 409

    ghost = client.post(
        "/api/checkout",
        json={"product_id": "GHOST", "member_id": None, "qty": 1},
    )
    assert ghost.status_code == 404


def test_injection_id_is_literal(client):
    """Malicious ids are plain strings, never SQL (SPM-23)."""
    evil = "' OR '1'='1"
    res = client.get(f"/api/products/{evil}")
    assert res.status_code == 404
    assert client.get("/api/summary").json()["total_types"] >= 3
