"""Inventory system v3.0 (SQLite + Member + Checkout).

Evolves the v2.0 JSON baseline with a Singleton SQLite
layer, Repository pattern, Strategy member tiers and a
discount checkout flow. All data here is fictional and
used for coursework only.
"""

import csv
import json
import os
import sqlite3
from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Optional, TypeVar

T = TypeVar("T")

DEFAULT_REORDER_POINT = 5
CSV_HEADER = [
    "ProductID",
    "ProductName",
    "Barcode",
    "Quantity",
    "ReorderPoint",
    "Price",
]


class Product:
    """Represents a single inventory product."""

    def __init__(
        self,
        product_id: str,
        name: str,
        quantity: int,
        price: float,
        category: str,
        barcode: str = "",
        reorder_point: int = DEFAULT_REORDER_POINT,
    ) -> None:
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.category = category
        self.barcode = barcode
        self.reorder_point = reorder_point

    @property
    def is_low_stock(self) -> bool:
        """True when quantity is at/below reorder point."""
        return self.quantity <= self.reorder_point

    def to_dict(self) -> dict:
        """Serialise the product for JSON storage."""
        return {
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "category": self.category,
            "barcode": self.barcode,
            "reorder_point": self.reorder_point,
        }

    @classmethod
    def from_dict(cls, product_id: str, data: dict) -> "Product":
        """Build a Product, tolerating legacy schemas.

        Backward compatibility (BUG-101 fix): legacy short
        keys ``n``/``q``/``p``/``c`` fall back when the long
        keys are absent; missing ``barcode``/``reorder``
        default to ``""`` and ``5``.
        """
        name = data.get("name") or data.get("n", "Unknown")
        if "quantity" in data:
            quantity = data["quantity"]
        else:
            quantity = data.get("q", 0)
        if "price" in data:
            price = data["price"]
        else:
            price = data.get("p", 0.0)
        category = data.get("category") or data.get("c", "General")
        barcode = data.get("barcode", "")
        reorder = data.get("reorder_point", DEFAULT_REORDER_POINT)
        return cls(
            product_id,
            name,
            int(quantity),
            float(price),
            category,
            str(barcode),
            int(reorder),
        )


class MemberTier(ABC):
    """Strategy interface for member discount rates."""

    label = "Regular"

    @abstractmethod
    def get_discount_rate(self) -> float:
        """Return the discount rate (0.0 - 1.0)."""
        raise NotImplementedError


class RegularMember(MemberTier):
    """Regular tier: no discount."""

    label = "Regular"

    def get_discount_rate(self) -> float:
        """Return 0.0 (no discount)."""
        return 0.0


class SilverMember(MemberTier):
    """Silver tier: 5 percent discount."""

    label = "Silver"

    def get_discount_rate(self) -> float:
        """Return 0.05."""
        return 0.05


class GoldMember(MemberTier):
    """Gold tier: 10 percent discount."""

    label = "Gold"

    def get_discount_rate(self) -> float:
        """Return 0.10."""
        return 0.10


class PlatinumMember(MemberTier):
    """Platinum tier: 15 percent discount."""

    label = "Platinum"

    def get_discount_rate(self) -> float:
        """Return 0.15."""
        return 0.15


TIER_CLASSES = {
    "Regular": RegularMember,
    "Silver": SilverMember,
    "Gold": GoldMember,
    "Platinum": PlatinumMember,
}


def normalize_tier(raw: object) -> str:
    """Normalise a tier name, fallback to Regular."""
    if not isinstance(raw, str):
        return "Regular"
    cleaned = raw.strip().capitalize()
    if cleaned in TIER_CLASSES:
        return cleaned
    return "Regular"


def discount_rate_for(tier_name: object) -> float:
    """Return the discount rate for a tier name."""
    tier = normalize_tier(tier_name)
    return TIER_CLASSES[tier]().get_discount_rate()


class Member:
    """Represents a shop member with a discount tier."""

    def __init__(
        self,
        member_id: str,
        name: str,
        tier: str = "Regular",
    ) -> None:
        self.member_id = member_id
        self.name = name
        self.tier = normalize_tier(tier)

    @property
    def discount_rate(self) -> float:
        """Return the discount rate for this member."""
        return discount_rate_for(self.tier)

    def to_dict(self) -> dict:
        """Serialise the member to a plain dict."""
        return {
            "name": self.name,
            "tier": self.tier,
            "discount_rate": self.discount_rate,
        }

    @classmethod
    def from_dict(cls, member_id: str, data: dict) -> "Member":
        """Build a Member, fallback to Regular tier."""
        name = data.get("name", "Unknown")
        tier = normalize_tier(data.get("tier", "Regular"))
        return cls(member_id, str(name), tier)


class SQLiteDatabaseContext:
    """Singleton SQLite connection (one instance per path).

    All SQL issued here uses parameterized queries only
    (``?`` placeholders); callers must never concatenate
    user input into SQL text.
    """

    _instance: Optional["SQLiteDatabaseContext"] = None
    _db_path: Optional[str] = None

    def __init__(self, db_path: str) -> None:
        self.db_path = os.path.abspath(db_path)
        # Thread-shared: the web server serves requests from a
        # thread pool while the singleton holds one connection.
        self.conn = sqlite3.connect(
            self.db_path, check_same_thread=False
        )
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    @classmethod
    def getInstance(cls, db_path: str) -> "SQLiteDatabaseContext":
        """Return the shared instance for ``db_path``."""
        target = os.path.abspath(db_path)
        if cls._instance is None or cls._db_path != target:
            cls.reset()
            cls._instance = cls(target)
            cls._db_path = target
        return cls._instance

    # Alias using snake_case for new callers/tests.
    @classmethod
    def get_instance(cls, db_path: str) -> "SQLiteDatabaseContext":
        """Snake_case alias of ``getInstance``."""
        return cls.getInstance(db_path)

    @classmethod
    def reset(cls) -> None:
        """Close and drop the shared instance (for tests)."""
        if cls._instance is not None:
            try:
                cls._instance.conn.close()
            except sqlite3.Error:
                pass
        cls._instance = None
        cls._db_path = None

    def _init_schema(self) -> None:
        """Create products/members tables if missing."""
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS products ("
            "product_id TEXT PRIMARY KEY, "
            "name TEXT NOT NULL, "
            "quantity INTEGER NOT NULL CHECK (quantity >= 0), "
            "price REAL NOT NULL CHECK (price >= 0), "
            "category TEXT NOT NULL DEFAULT 'General', "
            "barcode TEXT NOT NULL DEFAULT '', "
            "reorder_point INTEGER NOT NULL DEFAULT 5 "
            "CHECK (reorder_point >= 0))"
        )
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS members ("
            "member_id TEXT PRIMARY KEY, "
            "name TEXT NOT NULL, "
            "tier TEXT NOT NULL DEFAULT 'Regular', "
            "discount_rate REAL NOT NULL DEFAULT 0.0)"
        )
        self.conn.commit()

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Run a parameterized query, return the cursor."""
        return self.conn.execute(query, params)

    def commit(self) -> None:
        """Commit the current transaction."""
        self.conn.commit()

    def rollback(self) -> None:
        """Roll back the current transaction."""
        self.conn.rollback()

    def close(self) -> None:
        """Close the connection (keeps singleton ref)."""
        self.conn.close()


class InventoryRepository:
    """Repository hiding SQLite behind product methods."""

    def __init__(self, db: SQLiteDatabaseContext) -> None:
        self.db = db

    def save(self, product: Product) -> None:
        """Insert or replace a product (parameterized)."""
        try:
            self.db.execute(
                "INSERT OR REPLACE INTO products "
                "(product_id, name, quantity, price, "
                "category, barcode, reorder_point) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    product.product_id,
                    product.name,
                    int(product.quantity),
                    float(product.price),
                    product.category,
                    product.barcode,
                    int(product.reorder_point),
                ),
            )
            self.db.commit()
        except sqlite3.Error:
            self.db.rollback()
            raise

    def find_by_id(self, product_id: str) -> Optional[Product]:
        """Find a product by id; None when missing."""
        cursor = self.db.execute(
            "SELECT product_id, name, quantity, price, "
            "category, barcode, reorder_point "
            "FROM products WHERE product_id = ?",
            (product_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Product(
            str(row["product_id"]),
            str(row["name"]),
            int(row["quantity"]),
            float(row["price"]),
            str(row["category"]),
            str(row["barcode"]),
            int(row["reorder_point"]),
        )

    def find_all(self) -> List[Product]:
        """Return every product ordered by id."""
        cursor = self.db.execute(
            "SELECT product_id, name, quantity, price, "
            "category, barcode, reorder_point "
            "FROM products ORDER BY product_id"
        )
        products = []
        for row in cursor.fetchall():
            products.append(
                Product(
                    str(row["product_id"]),
                    str(row["name"]),
                    int(row["quantity"]),
                    float(row["price"]),
                    str(row["category"]),
                    str(row["barcode"]),
                    int(row["reorder_point"]),
                )
            )
        return products

    def update_stock(self, product_id: str, new_qty: int) -> bool:
        """Set a new quantity; False when id missing."""
        if new_qty < 0:
            raise ValueError("Quantity cannot be negative")
        try:
            cursor = self.db.execute(
                "UPDATE products SET quantity = ? "
                "WHERE product_id = ?",
                (int(new_qty), product_id),
            )
            self.db.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            self.db.rollback()
            raise

    def delete(self, product_id: str) -> bool:
        """Delete a product; False when id missing."""
        try:
            cursor = self.db.execute(
                "DELETE FROM products WHERE product_id = ?",
                (product_id,),
            )
            self.db.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            self.db.rollback()
            raise

    def count_products(self) -> int:
        """Return the number of stored products."""
        cursor = self.db.execute(
            "SELECT COUNT(*) AS total FROM products"
        )
        row = cursor.fetchone()
        return int(row["total"])

    def total_value(self) -> float:
        """Return sum(quantity * price) over products."""
        cursor = self.db.execute(
            "SELECT COALESCE(SUM(quantity * price), 0.0)"
            " AS total FROM products"
        )
        row = cursor.fetchone()
        return float(row["total"])

    def get_low_stock_alerts(self) -> List[Product]:
        """Return products at/below their reorder point."""
        return [p for p in self.find_all() if p.is_low_stock]

    def get_inventory_summary(self) -> dict:
        """Summarise types, value and low-stock names."""
        products = self.find_all()
        low = [p.name for p in products if p.is_low_stock]
        value = sum(p.quantity * p.price for p in products)
        return {
            "total_types": len(products),
            "total_value": value,
            "low_stock_list": low,
        }


class MemberManager:
    """CRUD for shop members backed by SQLite."""

    def __init__(self, db: SQLiteDatabaseContext) -> None:
        self.db = db

    def save_member(self, member: Member) -> None:
        """Insert or replace a member (parameterized)."""
        member.tier = normalize_tier(member.tier)
        try:
            self.db.execute(
                "INSERT OR REPLACE INTO members "
                "(member_id, name, tier, discount_rate) "
                "VALUES (?, ?, ?, ?)",
                (
                    member.member_id,
                    member.name,
                    member.tier,
                    float(discount_rate_for(member.tier)),
                ),
            )
            self.db.commit()
        except sqlite3.Error:
            self.db.rollback()
            raise

    def find_by_id(self, member_id: str) -> Optional[Member]:
        """Find a member by id; None when missing."""
        cursor = self.db.execute(
            "SELECT member_id, name, tier, discount_rate "
            "FROM members WHERE member_id = ?",
            (member_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Member(
            str(row["member_id"]),
            str(row["name"]),
            normalize_tier(row["tier"]),
        )

    def find_all(self) -> List[Member]:
        """Return every member ordered by id."""
        cursor = self.db.execute(
            "SELECT member_id, name, tier, discount_rate "
            "FROM members ORDER BY member_id"
        )
        members = []
        for row in cursor.fetchall():
            members.append(
                Member(
                    str(row["member_id"]),
                    str(row["name"]),
                    normalize_tier(row["tier"]),
                )
            )
        return members

    def delete_member(self, member_id: str) -> bool:
        """Delete a member; False when id missing."""
        try:
            cursor = self.db.execute(
                "DELETE FROM members WHERE member_id = ?",
                (member_id,),
            )
            self.db.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            self.db.rollback()
            raise


class CheckoutService:
    """Checkout flow with automatic member discount."""

    def __init__(
        self,
        repo: InventoryRepository,
        members: MemberManager,
    ) -> None:
        self.repo = repo
        self.members = members

    def calculate_total_with_discount(
        self,
        product: Product,
        tier_name: object,
        qty: int,
    ) -> tuple:
        """Return (subtotal, discount, grand_total)."""
        amount = int(qty)
        if amount <= 0:
            raise ValueError("Quantity must be positive")
        rate = discount_rate_for(tier_name)
        subtotal = float(product.price) * amount
        discount = subtotal * rate
        total = subtotal - discount
        return (subtotal, discount, total)

    def _resolve_tier(self, member_id: object) -> str:
        """Resolve a member id to a tier (guest Regular)."""
        if not member_id or not str(member_id).strip():
            return "Regular"
        found = self.members.find_by_id(str(member_id).strip())
        if found is None:
            return "Regular"
        return found.tier

    def process_checkout(
        self,
        product_id: str,
        member_id: Optional[str],
        qty: int,
    ) -> tuple:
        """Checkout, cut stock and return a receipt dict.

        Returns (True, receipt, remaining) on success or
        (False, message, current_qty_or_None) on failure.
        """
        amount = int(qty)
        if amount <= 0:
            return (False, "Amount must be greater than 0", None)
        product = self.repo.find_by_id(product_id)
        if product is None:
            return (False, "Product not found!", None)
        if product.quantity < amount:
            return (
                False,
                "Error: Not enough stock!",
                product.quantity,
            )
        tier = self._resolve_tier(member_id)
        sub, disc, total = self.calculate_total_with_discount(
            product, tier, amount
        )
        remaining = product.quantity - amount
        try:
            self.repo.update_stock(product_id, remaining)
        except (sqlite3.Error, ValueError) as exc:
            return (False, f"Checkout failed: {exc}", None)
        receipt = {
            "product_id": product.product_id,
            "product_name": product.name,
            "quantity": amount,
            "unit_price": float(product.price),
            "subtotal": round(sub, 2),
            "tier": tier,
            "discount_rate": discount_rate_for(tier),
            "discount_value": round(disc, 2),
            "grand_total": round(total, 2),
            "remaining": remaining,
            "low_stock": remaining <= product.reorder_point,
        }
        return (True, receipt, remaining)


class InventoryManager:
    """JSON business logic (legacy backend, kept compatible)."""

    def __init__(self, db_path: str = "data.json") -> None:
        self.db_path = db_path
        self.products: Dict[str, Product] = {}
        self.load_data()

    def load_data(self) -> None:
        """Load products from the JSON database file."""
        if not os.path.exists(self.db_path):
            self._set_default_data()
            self.save_data()
            return
        try:
            with open(self.db_path, "r", encoding="utf-8") as fh:
                raw_data = json.load(fh)
                self.products = {
                    pid: Product.from_dict(pid, pdata)
                    for pid, pdata in raw_data.items()
                }
        except (json.JSONDecodeError, OSError) as exc:
            print(f"Error loading database: {exc}. Starting empty.")
            self.products = {}

    def save_data(self) -> None:
        """Persist products atomically (temp file + replace)."""
        temp_path = self.db_path + ".tmp"
        try:
            with open(temp_path, "w", encoding="utf-8") as fh:
                output = {
                    pid: prod.to_dict()
                    for pid, prod in self.products.items()
                }
                json.dump(output, fh, indent=4, ensure_ascii=False)
            os.replace(temp_path, self.db_path)
        except OSError as exc:
            print(f"Error saving database: {exc}")

    def _set_default_data(self) -> None:
        """Seed the inventory when no database file exists."""
        self.products = {
            "101": Product("101", "Mama Noodles", 50, 6.0, "Food"),
            "102": Product("102", "Lactasoy Milk", 20, 12.0, "Drink"),
            "103": Product("103", "Singha Water", 100, 10.0, "Drink"),
        }

    def add_or_update_product(
        self,
        product_id: str,
        name: str,
        quantity: int,
        price: float,
        category: str,
        barcode: str = "",
        reorder_point: int = DEFAULT_REORDER_POINT,
    ) -> bool:
        """Insert a new product or overwrite an existing one."""
        self.products[product_id] = Product(
            product_id, name, quantity, price,
            category, barcode, reorder_point,
        )
        self.save_data()
        return True

    def cut_stock(self, product_id: str, amount: int) -> tuple:
        """Remove stock; returns (success, message, rest)."""
        if product_id not in self.products:
            return (False, "Product not found!", None)
        product = self.products[product_id]
        if product.quantity < amount:
            return (
                False,
                "Error: Not enough stock!",
                product.quantity,
            )
        product.quantity -= amount
        self.save_data()
        return (True, "Stock updated.", product.quantity)

    def get_low_stock_alerts(self) -> List[Product]:
        """Return products at/below their reorder point."""
        return [p for p in self.products.values() if p.is_low_stock]

    def get_inventory_summary(self) -> dict:
        """Summarise types, total value and low-stock names."""
        total_types = len(self.products)
        total_value = sum(
            p.quantity * p.price for p in self.products.values()
        )
        low = [p.name for p in self.get_low_stock_alerts()]
        return {
            "total_types": total_types,
            "total_value": total_value,
            "low_stock_list": low,
        }


class CsvReportExporter:
    """Exports the inventory to a CSV report."""

    HEADER = [
        "ProductID",
        "ProductName",
        "Barcode",
        "Quantity",
        "ReorderPoint",
        "Price",
    ]

    @staticmethod
    def export(products: Dict[str, Product], csv_path: str) -> str:
        """Write products to ``csv_path``, return the path."""
        try:
            with open(csv_path, "w", newline="",
                      encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(CsvReportExporter.HEADER)
                for pid, prod in products.items():
                    writer.writerow(
                        [
                            pid,
                            prod.name,
                            prod.barcode,
                            prod.quantity,
                            prod.reorder_point,
                            f"{prod.price:.2f}",
                        ]
                    )
        except OSError as exc:
            print(f"Error exporting CSV report: {exc}")
            raise
        return csv_path

    @classmethod
    def export_manager(
        cls, manager: InventoryManager, csv_path: str
    ) -> str:
        """Export a JSON manager's products to CSV."""
        return cls.export(manager.products, csv_path)

    @classmethod
    def export_repo(
        cls, repo: InventoryRepository, csv_path: str
    ) -> str:
        """Export a SQLite repo's products to CSV."""
        products = {p.product_id: p for p in repo.find_all()}
        return cls.export(products, csv_path)


def migrate_json_to_sqlite(
    json_path: str, repo: InventoryRepository
) -> dict:
    """Migrate a JSON file into SQLite, verify 100 percent.

    Reads every record with ``Product.from_dict`` (so legacy
    short keys and missing barcode/reorder are handled),
    upserts into ``repo`` and checks that record counts and
    total inventory value match exactly.
    """
    with open(json_path, "r", encoding="utf-8") as handle:
        raw_data = json.load(handle)
    migrated = 0
    for pid, pdata in raw_data.items():
        product = Product.from_dict(pid, pdata)
        repo.save(product)
        migrated += 1
    json_total = sum(
        Product.from_dict(pid, pdata).quantity
        * Product.from_dict(pid, pdata).price
        for pid, pdata in raw_data.items()
    )
    sqlite_total = repo.total_value()
    sqlite_count = repo.count_products()
    match = (
        sqlite_count == len(raw_data)
        and abs(sqlite_total - json_total) < 0.01
    )
    return {
        "migrated": migrated,
        "json_count": len(raw_data),
        "sqlite_count": sqlite_count,
        "json_total": round(float(json_total), 2),
        "sqlite_total": round(float(sqlite_total), 2),
        "match": match,
    }


def seed_default_products(repo: InventoryRepository) -> int:
    """Seed 3 demo products when the database is empty."""
    if repo.count_products() > 0:
        return 0
    defaults = [
        Product("101", "Mama Noodles", 50, 6.0, "Food"),
        Product("102", "Lactasoy Milk", 20, 12.0, "Drink"),
        Product("103", "Singha Water", 100, 10.0, "Drink"),
    ]
    for product in defaults:
        repo.save(product)
    return len(defaults)


class InventoryCLI:
    """Command-line interface with input validation."""

    def __init__(
        self,
        repo: InventoryRepository,
        members: MemberManager,
        checkout: CheckoutService,
    ) -> None:
        self.repo = repo
        self.members = members
        self.checkout = checkout

    def _get_input(
        self, prompt: str, validator_func: Callable[[str], T]
    ) -> T:
        """Prompt until the validator accepts the input."""
        while True:
            try:
                user_input = input(prompt).strip()
                result = validator_func(user_input)
                if isinstance(result, Exception):
                    raise result
                return result
            except ValueError as exc:
                print(f"Invalid input: {exc}. Try again.")

    def run(self) -> None:
        """Main menu loop."""
        while True:
            print("\n=== INVENTORY SYSTEM v3.0 ===")
            print("1. Show all products")
            print("2. Add or Update product")
            print("3. Cut stock (Out)")
            print("4. Check inventory summary")
            print("5. Export CSV report")
            print("6. Manage members")
            print("7. Checkout with discount")
            print("8. Exit")
            choice = input("Select menu: ").strip()
            if choice == "1":
                self.show_all()
            elif choice == "2":
                self.add_or_update()
            elif choice == "3":
                self.cut_stock()
            elif choice == "4":
                self.show_summary()
            elif choice == "5":
                self.export_csv()
            elif choice == "6":
                self.manage_members()
            elif choice == "7":
                self.checkout_flow()
            elif choice == "8":
                print("Thank you. Goodbye!")
                break
            else:
                print("Invalid choice, select 1-8.")

    def show_all(self) -> None:
        """List every product with barcode and stock flag."""
        print("-" * 85)
        products = self.repo.find_all()
        if not products:
            print("Inventory is empty.")
        for prod in products:
            flag = " [LOW]" if prod.is_low_stock else ""
            print(
                f"ID: {prod.product_id:<5} | "
                f"Name: {prod.name:<20} | "
                f"Barcode: {prod.barcode:<12} | "
                f"Stock: {prod.quantity:<6} | "
                f"ROP: {prod.reorder_point:<4} | "
                f"Price: {prod.price:<7.2f} "
                f"THB | Type: {prod.category}{flag}"
            )
        print("-" * 85)

    def add_or_update(self) -> None:
        """Prompt for product fields incl. barcode/ROP."""

        def validate_id(val: str) -> str:
            if not val:
                raise ValueError("ID cannot be empty")
            return val

        def validate_name(val: str) -> str:
            if not val:
                raise ValueError("Name cannot be empty")
            return val

        pid = self._get_input("Enter ID: ", validate_id)
        name = self._get_input("Enter Name: ", validate_name)

        def validate_qty(val: str) -> int:
            qty = int(val)
            if qty < 0:
                raise ValueError("Quantity is negative")
            return qty

        def validate_price(val: str) -> float:
            price = float(val)
            if price < 0:
                raise ValueError("Price is negative")
            return price

        def validate_reorder(val: str) -> int:
            if val == "":
                return DEFAULT_REORDER_POINT
            rop = int(val)
            if rop < 0:
                raise ValueError("Reorder is negative")
            return rop

        def validate_category(val: str) -> str:
            return val if val else "General"

        def validate_barcode(val: str) -> str:
            return val

        qty = self._get_input("Enter Qty: ", validate_qty)
        price = self._get_input("Enter Price: ", validate_price)
        category = self._get_input(
            "Enter Category: ", validate_category
        )
        barcode = self._get_input(
            "Enter Barcode (optional): ", validate_barcode
        )
        reorder = self._get_input(
            "Enter Reorder Point [5]: ", validate_reorder
        )
        self.repo.save(
            Product(pid, name, qty, price,
                    category, barcode, reorder)
        )
        print("Success: Product recorded.")

    def cut_stock(self) -> None:
        """Cut stock for a product and warn on low levels."""
        pid = input("Enter product ID to cut stock: ").strip()
        if not pid:
            print("Failed: ID cannot be empty.")
            return

        def validate_amount(val: str) -> int:
            amount = int(val)
            if amount <= 0:
                raise ValueError("Amount must be > 0")
            return amount

        amount = self._get_input(
            "How many items out?: ", validate_amount
        )
        product = self.repo.find_by_id(pid)
        if product is None:
            print("Failed: Product not found!")
            return
        if product.quantity < amount:
            print("Failed: Error: Not enough stock!")
            return
        remaining = product.quantity - amount
        self.repo.update_stock(pid, remaining)
        print("Stock updated.")
        updated = self.repo.find_by_id(pid)
        if updated is not None and updated.is_low_stock:
            print(
                "!!! WARNING: AT/BELOW REORDER POINT "
                f"(<= {updated.reorder_point}) !!!"
            )

    def show_summary(self) -> None:
        """Print the inventory summary and low-stock list."""
        summary = self.repo.get_inventory_summary()
        print("\n--- INVENTORY SUMMARY ---")
        print(f"Total product types: {summary['total_types']}")
        value = summary["total_value"]
        print(f"Total inventory value: {value:,.2f} THB")
        low = ", ".join(summary["low_stock_list"]) or "None"
        print(f"Alert low stock (<= reorder point): {low}")

    def export_csv(self, csv_path: Optional[str] = None) -> str:
        """Export the inventory to CSV (SC03 reporting)."""
        if csv_path is None:
            raw = input("Enter CSV path [report.csv]: ").strip()
            csv_path = raw or "report.csv"
        try:
            CsvReportExporter.export_repo(self.repo, csv_path)
        except OSError:
            print("Failed: could not write CSV report.")
            return ""
        print(f"Success: CSV report written to {csv_path}.")
        return csv_path

    def manage_members(self) -> None:
        """Member submenu: list, add/update, find, back."""
        while True:
            print("\n--- MEMBER MANAGEMENT ---")
            print("1. List members")
            print("2. Add or Update member")
            print("3. Find member")
            print("4. Back")
            choice = input("Select: ").strip()
            if choice == "1":
                self._list_members()
            elif choice == "2":
                self._add_member()
            elif choice == "3":
                self._find_member()
            elif choice == "4":
                break
            else:
                print("Invalid choice, select 1-4.")

    def _list_members(self) -> None:
        """Print every member with tier and rate."""
        members = self.members.find_all()
        print("-" * 60)
        if not members:
            print("No members yet.")
        for mem in members:
            print(
                f"ID: {mem.member_id:<8} | "
                f"Name: {mem.name:<20} | "
                f"Tier: {mem.tier:<9} | "
                f"Rate: {mem.discount_rate:.0%}"
            )
        print("-" * 60)

    def _add_member(self) -> None:
        """Prompt for member fields and save."""

        def validate_mid(val: str) -> str:
            if not val:
                raise ValueError("ID cannot be empty")
            return val

        def validate_mname(val: str) -> str:
            if not val:
                raise ValueError("Name cannot be empty")
            return val

        def validate_tier(val: str) -> str:
            if val == "":
                return "Regular"
            tier = normalize_tier(val)
            if val.strip().capitalize() not in TIER_CLASSES:
                print("Unknown tier, fallback to Regular.")
            return tier

        mid = self._get_input("Enter Member ID: ", validate_mid)
        name = self._get_input("Enter Name: ", validate_mname)
        tier = self._get_input(
            "Tier [Regular/Silver/Gold/Platinum]: ",
            validate_tier,
        )
        self.members.save_member(Member(mid, name, tier))
        print(f"Success: member {mid} saved ({tier}).")

    def _find_member(self) -> None:
        """Look up one member by id."""
        mid = input("Enter Member ID: ").strip()
        found = self.members.find_by_id(mid)
        if found is None:
            print("Member not found (guest = Regular 0%).")
            return
        print(
            f"Found: {found.name} | Tier: {found.tier} | "
            f"Discount: {found.discount_rate:.0%}"
        )

    def checkout_flow(self) -> None:
        """Checkout with automatic member discount."""
        pid = input("Enter product ID: ").strip()
        if not pid:
            print("Failed: ID cannot be empty.")
            return

        def validate_qty(val: str) -> int:
            qty = int(val)
            if qty <= 0:
                raise ValueError("Quantity must be > 0")
            return qty

        qty = self._get_input("Enter quantity: ", validate_qty)
        mid = input("Member ID (Enter = guest): ").strip() or None
        ok, payload, _ = self.checkout.process_checkout(
            pid, mid, qty
        )
        if not ok:
            print(f"Failed: {payload}")
            return
        print("\n--- RECEIPT ---")
        print(f"Product : {payload['product_name']}")
        print(f"Qty x Price: {payload['quantity']} x "
              f"{payload['unit_price']:.2f}")
        print(f"Subtotal : {payload['subtotal']:.2f} THB")
        print(f"Tier {payload['tier']} "
              f"({payload['discount_rate']:.0%}): "
              f"-{payload['discount_value']:.2f} THB")
        print(f"TOTAL    : {payload['grand_total']:.2f} THB")
        print(f"Remaining stock: {payload['remaining']}")
        if payload["low_stock"]:
            print("!!! WARNING: AT/BELOW REORDER POINT !!!")


if __name__ == "__main__":
    _base = os.path.dirname(os.path.abspath(__file__))
    _db_file = os.path.join(_base, "inventory.db")
    _json_file = os.path.join(_base, "data.json")
    _ctx = SQLiteDatabaseContext.getInstance(_db_file)
    _repo = InventoryRepository(_ctx)
    _mem = MemberManager(_ctx)
    _co = CheckoutService(_repo, _mem)
    if _repo.count_products() == 0 and os.path.exists(_json_file):
        try:
            _stats = migrate_json_to_sqlite(_json_file, _repo)
            print(f"Migrated legacy JSON: {_stats}")
        except (OSError, ValueError) as _err:
            print(f"Migration skipped: {_err}")
    seed_default_products(_repo)
    _cli = InventoryCLI(_repo, _mem, _co)
    _cli.run()
