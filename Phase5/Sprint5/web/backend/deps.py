"""Shared backend deps: thin layer over app.py v3.0 domain."""

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(ROOT, "app.py")):
    parent = os.path.dirname(ROOT)
    if parent == ROOT:  # pragma: no cover - safety net
        raise RuntimeError("repo root (app.py) not found!")
    ROOT = parent
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import app as domain  # noqa: E402  (path bootstrap above)


_db_path: str | None = None
_ready: dict = {}


def configure(db_path: str) -> None:
    """Pin the database file (used by tests)."""
    global _db_path
    _db_path = os.path.abspath(db_path)
    _ready.pop(_db_path, None)
    domain.SQLiteDatabaseContext.reset()


def db_path() -> str:
    """Resolve the active database file path."""
    if _db_path:
        return _db_path
    env_path = os.environ.get("INVENTORY_DB")
    if env_path:
        return os.path.abspath(env_path)
    return os.path.join(ROOT, "inventory.db")


def _raw_ctx() -> domain.SQLiteDatabaseContext:
    """Return the shared context without readiness checks."""
    return domain.SQLiteDatabaseContext.getInstance(db_path())


def get_ctx() -> domain.SQLiteDatabaseContext:
    """Return the shared context (lazy, no import side effects).

    The first use per database file also migrates legacy JSON
    once and seeds defaults, so readiness never depends on
    server lifespan events (which test clients may skip).
    """
    ctx = _raw_ctx()
    if not _ready.get(ctx.db_path):
        ensure_ready()
        _ready[ctx.db_path] = True
    return ctx


def get_repo() -> domain.InventoryRepository:
    """Return an inventory repository bound to the active DB."""
    return domain.InventoryRepository(get_ctx())


def get_members() -> domain.MemberManager:
    """Return a member manager bound to the active DB."""
    return domain.MemberManager(get_ctx())


def get_checkout() -> domain.CheckoutService:
    """Return a checkout service bound to the active DB."""
    return domain.CheckoutService(get_repo(), get_members())


def ensure_ready() -> dict:
    """Migrate legacy JSON once, then seed defaults if empty."""
    repo = domain.InventoryRepository(_raw_ctx())
    migrated: dict = {"migrated": 0, "match": True}
    json_file = os.path.join(ROOT, "data.json")
    if repo.count_products() == 0 and os.path.exists(json_file):
        try:
            migrated = domain.migrate_json_to_sqlite(
                json_file, repo
            )
        except (OSError, ValueError):
            pass
    seeded = domain.seed_default_products(repo)
    return {"migrated": migrated, "seeded": seeded}
