"""FastAPI entrypoint: serves /api/* and the static frontend."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles

from . import api_checkout, api_members, api_products, deps

VERSION = "4.0.0-web"
FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "frontend",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Migrate + seed on startup (same behaviour as the CLI)."""
    deps.ensure_ready()
    yield


app = FastAPI(title="Inventory Web API", version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_products.router)
app.include_router(api_members.router)
app.include_router(api_checkout.router)


@app.get("/api/health")
def health() -> dict:
    """Liveness probe with the app version."""
    return {"status": "ok", "version": VERSION}


@app.get("/api/summary")
def summary() -> dict:
    """Inventory summary: types, value and low-stock names."""
    return deps.get_repo().get_inventory_summary()


@app.get("/api/export.csv")
def export_csv() -> PlainTextResponse:
    """Download the inventory CSV report (same columns as CLI)."""
    return PlainTextResponse(
        api_products.build_csv(),
        media_type="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=inventory-report.csv"
        },
    )


if os.path.isdir(FRONTEND_DIR):  # pragma: no cover - static env only
    app.mount(
        "/", StaticFiles(directory=FRONTEND_DIR, html=True), name="web"
    )


@app.get("/frontend-check", include_in_schema=False)
def frontend_check() -> dict:
    """Confirm the frontend directory resolves (for smoke tests)."""
    exists = os.path.isfile(os.path.join(FRONTEND_DIR, "index.html"))
    return {"frontend_index": exists}
