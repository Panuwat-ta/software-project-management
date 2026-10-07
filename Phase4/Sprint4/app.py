"""Evolved inventory system (Week 12 evolution, v2.0.0-evolution).

Extends the Phase-2 baseline with barcode support (CR-01),
per-product reorder points and low-stock alerts (CR-02), a CSV
report exporter, and a BUG-101 fix for legacy data files that lack
the new fields. All data in this coursework project is hypothetical.
"""

import csv
import json
import os
from typing import Callable, Dict, List, Optional, TypeVar

T = TypeVar("T")


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
        reorder_point: int = 5,
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
        """True when quantity is at or below the reorder point."""
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
        """Build a Product from a dict, tolerating legacy schemas.

        Backward compatibility (BUG-101 fix):
        - Legacy short keys ``n``/``q``/``p``/``c`` fall back when the
          long keys are absent.
        - Missing ``barcode``/``reorder_point`` (files written before
          the evolution) default to ``""`` and ``5``.
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
        reorder_point = data.get("reorder_point", 5)
        return cls(
            product_id,
            name,
            int(quantity),
            float(price),
            category,
            str(barcode),
            int(reorder_point),
        )


class InventoryManager:
    """Business logic and JSON persistence for the inventory."""

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
            with open(self.db_path, "r", encoding="utf-8") as handle:
                raw_data = json.load(handle)
                self.products = {
                    pid: Product.from_dict(pid, pdata)
                    for pid, pdata in raw_data.items()
                }
        except (json.JSONDecodeError, OSError) as exc:
            print(f"Error loading database: {exc}. Starting with empty inventory.")
            self.products = {}

    def save_data(self) -> None:
        """Persist products atomically (temp file + os.replace)."""
        temp_path = self.db_path + ".tmp"
        try:
            with open(temp_path, "w", encoding="utf-8") as handle:
                output = {pid: prod.to_dict() for pid, prod in self.products.items()}
                json.dump(output, handle, indent=4, ensure_ascii=False)
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
        reorder_point: int = 5,
    ) -> bool:
        """Insert a new product or overwrite an existing one."""
        self.products[product_id] = Product(
            product_id, name, quantity, price, category, barcode, reorder_point
        )
        self.save_data()
        return True

    def cut_stock(
        self, product_id: str, amount: int
    ) -> tuple:
        """Remove stock; returns (success, message, remaining)."""
        if product_id not in self.products:
            return False, "Product not found!", None
        product = self.products[product_id]
        if product.quantity < amount:
            return False, "Error: Not enough stock!", product.quantity
        product.quantity -= amount
        self.save_data()
        return True, "Stock updated.", product.quantity

    def get_low_stock_alerts(self) -> List[Product]:
        """Return products at or below their reorder point (CR-02)."""
        return [prod for prod in self.products.values() if prod.is_low_stock]

    def get_inventory_summary(self) -> dict:
        """Summarise types, total value, and low-stock product names."""
        total_types = len(self.products)
        total_value = sum(p.quantity * p.price for p in self.products.values())
        low_stock_list = [p.name for p in self.get_low_stock_alerts()]
        return {
            "total_types": total_types,
            "total_value": total_value,
            "low_stock_list": low_stock_list,
        }


class CsvReportExporter:
    """Exports the inventory to a CSV report (CR-02 / SC03)."""

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
        """Write products to ``csv_path`` and return the path."""
        try:
            with open(csv_path, "w", newline="", encoding="utf-8") as handle:
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
    def export_manager(cls, manager: InventoryManager, csv_path: str) -> str:
        """Convenience wrapper exporting a manager's products."""
        return cls.export(manager.products, csv_path)


class InventoryCLI:
    """Command-line interface with input validation."""

    def __init__(self, manager: InventoryManager) -> None:
        self.manager = manager

    def _get_input(self, prompt: str, validator_func: Callable[[str], T]) -> T:
        """Prompt until the validator accepts the input."""
        while True:
            try:
                user_input = input(prompt).strip()
                result = validator_func(user_input)
                if isinstance(result, Exception):
                    raise result
                return result
            except ValueError as exc:
                print(f"Invalid input: {exc}. Please try again.")

    def run(self) -> None:
        """Main menu loop."""
        while True:
            print("\n=== INVENTORY SYSTEM v2.0 ===")
            print("1. Show all products")
            print("2. Add or Update product")
            print("3. Cut stock (Out)")
            print("4. Check inventory summary")
            print("5. Export CSV report")
            print("6. Exit")
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
                print("Thank you for using the system. Goodbye!")
                break
            else:
                print("Invalid choice, please select 1-6.")

    def show_all(self) -> None:
        """List every product with barcode and stock status."""
        print("-" * 85)
        if not self.manager.products:
            print("Inventory is empty.")
        for pid, prod in self.manager.products.items():
            flag = " [LOW]" if prod.is_low_stock else ""
            print(
                f"ID: {pid:<5} | Name: {prod.name:<20} | "
                f"Barcode: {prod.barcode:<12} | Stock: {prod.quantity:<6} | "
                f"ROP: {prod.reorder_point:<4} | Price: {prod.price:<7.2f} "
                f"THB | Type: {prod.category}{flag}"
            )
        print("-" * 85)

    def add_or_update(self) -> None:
        """Prompt for product fields, including barcode (CR-01)."""

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
                raise ValueError("Quantity cannot be negative")
            return qty

        def validate_price(val: str) -> float:
            price = float(val)
            if price < 0:
                raise ValueError("Price cannot be negative")
            return price

        def validate_reorder(val: str) -> int:
            if val == "":
                return 5
            rop = int(val)
            if rop < 0:
                raise ValueError("Reorder point cannot be negative")
            return rop

        def validate_category(val: str) -> str:
            return val if val else "General"

        def validate_barcode(val: str) -> str:
            return val

        qty = self._get_input("Enter Qty: ", validate_qty)
        price = self._get_input("Enter Price: ", validate_price)
        category = self._get_input("Enter Category: ", validate_category)
        barcode = self._get_input("Enter Barcode (optional): ", validate_barcode)
        reorder_point = self._get_input(
            "Enter Reorder Point [5]: ", validate_reorder
        )
        self.manager.add_or_update_product(
            pid, name, qty, price, category, barcode, reorder_point
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
                raise ValueError("Amount must be greater than zero")
            return amount

        amount = self._get_input("How many items out?: ", validate_amount)
        success, message, remaining = self.manager.cut_stock(pid, amount)
        if success:
            print(message)
            product = self.manager.products[pid]
            if product.is_low_stock:
                print(
                    "!!! WARNING: ITEM IS AT OR BELOW REORDER POINT "
                    f"(<={product.reorder_point}) !!!"
                )
        else:
            print(f"Failed: {message}")

    def show_summary(self) -> None:
        """Print the inventory summary and low-stock alerts."""
        summary = self.manager.get_inventory_summary()
        print("\n--- INVENTORY SUMMARY ---")
        print(f"Total product types: {summary['total_types']}")
        print(f"Total inventory value: {summary['total_value']:,.2f} THB")
        low = ", ".join(summary["low_stock_list"]) or "None"
        print(f"Alert low stock (<= reorder point): {low}")

    def export_csv(self, csv_path: Optional[str] = None) -> Optional[str]:
        """Export the inventory to CSV (SC03 reporting)."""
        if csv_path is None:
            raw = input("Enter CSV path [report.csv]: ").strip()
            csv_path = raw or "report.csv"
        try:
            CsvReportExporter.export_manager(self.manager, csv_path)
        except OSError:
            print("Failed: could not write CSV report.")
            return None
        print(f"Success: CSV report written to {csv_path}.")
        return csv_path


if __name__ == "__main__":
    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
    inv_manager = InventoryManager(db_path=db_file)
    cli = InventoryCLI(inv_manager)
    cli.run()
