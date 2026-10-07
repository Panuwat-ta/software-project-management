"""Week 12 evolution tests: baseline (5) + CR-01/CR-02/BUG-101/CLI/integration.

CR-01: barcode support. CR-02: reorder points, low-stock alerts, CSV
reporting. BUG-101: legacy data files (short keys n/q/p/c, missing new
fields) must load without KeyError. All fixtures use pytest tmp_path.
"""

import csv
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import CsvReportExporter, InventoryCLI, InventoryManager, Product


@pytest.fixture
def manager(tmp_path):
    """Seeded manager backed by a tmp_path JSON database."""
    db_path = tmp_path / "data.json"
    db_path.write_text("{}", encoding="utf-8")
    mgr = InventoryManager(db_path=str(db_path))
    mgr.products = {
        "1": Product("1", "Item A", 20, 100.0, "Cat 1"),
        "2": Product("2", "Item B", 10, 50.0, "Cat 2"),
        "3": Product("3", "Item C", 4, 200.0, "Cat 3"),
    }
    mgr.save_data()
    return mgr


# ---------------------------------------------------------------- baseline (5)
def test_calculate_inventory_summary(manager):
    """Summary totals and low-stock detection stay correct."""
    summary = manager.get_inventory_summary()
    assert summary["total_types"] == 3
    assert summary["total_value"] == 3300.0
    assert "Item C" in summary["low_stock_list"]
    assert "Item A" not in summary["low_stock_list"]


def test_cut_stock_success(manager):
    """Cutting stock succeeds when inventory is sufficient."""
    success, msg, remaining = manager.cut_stock("1", 5)
    assert success is True
    assert remaining == 15
    assert manager.products["1"].quantity == 15


def test_cut_stock_not_enough(manager):
    """Cutting more than available fails without changing stock."""
    success, msg, remaining = manager.cut_stock("2", 15)
    assert success is False
    assert msg == "Error: Not enough stock!"
    assert remaining == 10


def test_cut_stock_not_found(manager):
    """Cutting stock for an unknown ID reports not found."""
    success, msg, remaining = manager.cut_stock("999", 5)
    assert success is False
    assert msg == "Product not found!"
    assert remaining is None


def test_add_or_update_product(manager):
    """New products are added and existing ones overwritten."""
    manager.add_or_update_product("4", "Item D", 100, 5.0, "Cat 4")
    assert "4" in manager.products
    assert manager.products["4"].name == "Item D"
    manager.add_or_update_product("1", "Item A+", 30, 120.0, "Cat 1")
    assert manager.products["1"].name == "Item A+"
    assert manager.products["1"].quantity == 30


# ------------------------------------------------------------------ CR-01 (4)
def test_cr01_barcode_defaults_to_empty():
    """CR-01: barcode defaults to '' when not supplied."""
    prod = Product("9", "No Barcode", 5, 10.0, "Misc")
    assert prod.barcode == ""


def test_cr01_barcode_round_trip(manager):
    """CR-01: barcode survives to_dict/from_dict and reload."""
    manager.add_or_update_product("7", "Scanned", 8, 25.0, "Food", barcode="8851234567890")
    reloaded = InventoryManager(db_path=manager.db_path)
    assert reloaded.products["7"].barcode == "8851234567890"


def test_cr01_csv_contains_barcode(manager, tmp_path):
    """CR-01: exported CSV carries the barcode column values."""
    manager.add_or_update_product("7", "Scanned", 8, 25.0, "Food", barcode="885000111")
    out = tmp_path / "barcode.csv"
    CsvReportExporter.export_manager(manager, str(out))
    with open(out, newline="", encoding="utf-8") as handle:
        rows = {r["ProductID"]: r for r in csv.DictReader(handle)}
    assert rows["7"]["Barcode"] == "885000111"
    assert rows["1"]["Barcode"] == ""


def test_cr01_add_or_update_keeps_backward_compat(manager):
    """CR-01: add_or_update without new args still works (baseline CLI)."""
    manager.add_or_update_product("8", "Plain", 3, 9.0, "Misc")
    assert manager.products["8"].barcode == ""
    assert manager.products["8"].reorder_point == 5


# ------------------------------------------------------------------ CR-02 (6)
def test_cr02_reorder_point_default():
    """CR-02: reorder_point defaults to 5."""
    assert Product("1", "X", 10, 1.0, "C").reorder_point == 5


def test_cr02_is_low_stock_boundary():
    """CR-02: qty == reorder_point counts as low stock (<=)."""
    assert Product("1", "Edge", 5, 1.0, "C", reorder_point=5).is_low_stock is True
    assert Product("2", "Ok", 6, 1.0, "C", reorder_point=5).is_low_stock is False


def test_cr02_get_low_stock_alerts(manager):
    """CR-02: alerts list only products at/below their reorder point."""
    alerts = manager.get_low_stock_alerts()
    assert {p.product_id for p in alerts} == {"3"}
    manager.products["2"].reorder_point = 10
    assert {p.product_id for p in manager.get_low_stock_alerts()} == {"2", "3"}


def test_cr02_custom_reorder_point_persists(manager):
    """CR-02: custom reorder points survive a save/reload cycle."""
    manager.add_or_update_product("9", "Custom ROP", 12, 7.5, "Misc", reorder_point=15)
    reloaded = InventoryManager(db_path=manager.db_path)
    assert reloaded.products["9"].reorder_point == 15
    assert reloaded.products["9"].is_low_stock is True


def test_cr02_csv_header_and_row_shape(manager, tmp_path):
    """CR-02: CSV header is exactly ProductID,ProductName,Barcode,..."""
    out = tmp_path / "report.csv"
    CsvReportExporter.export_manager(manager, str(out))
    with open(out, newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        rows = list(reader)
    assert header == [
        "ProductID",
        "ProductName",
        "Barcode",
        "Quantity",
        "ReorderPoint",
        "Price",
    ]
    assert len(rows) == 3
    row1 = rows[0]
    assert row1[0] == "1" and row1[1] == "Item A"
    assert row1[3] == "20" and row1[4] == "5" and row1[5] == "100.00"


def test_cr02_csv_empty_inventory(tmp_path):
    """CR-02: empty inventory exports a header-only CSV."""
    db_path = tmp_path / "empty.json"
    db_path.write_text("{}", encoding="utf-8")
    mgr = InventoryManager(db_path=str(db_path))
    mgr.products = {}
    out = tmp_path / "empty.csv"
    CsvReportExporter.export_manager(mgr, str(out))
    with open(out, newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    assert rows == [CsvReportExporter.HEADER]


# ---------------------------------------------------------------- BUG-101 (4)
def test_bug101_legacy_short_keys():
    """BUG-101: legacy n/q/p/c keys load without KeyError."""
    prod = Product.from_dict("5", {"n": "Old", "q": 7, "p": 3.5, "c": "Legacy"})
    assert (prod.name, prod.quantity, prod.price, prod.category) == (
        "Old",
        7,
        3.5,
        "Legacy",
    )


def test_bug101_missing_new_fields_default():
    """BUG-101: new-schema rows without barcode/reorder_point get defaults."""
    prod = Product.from_dict(
        "6", {"name": "Pre-Evo", "quantity": 9, "price": 2.0, "category": "Food"}
    )
    assert prod.barcode == ""
    assert prod.reorder_point == 5


def test_bug101_legacy_file_loads(tmp_path):
    """BUG-101: a legacy JSON file loads and re-saves with new fields."""
    db_path = tmp_path / "legacy.json"
    db_path.write_text(
        json.dumps({"1": {"n": "Old A", "q": 4, "p": 10.0, "c": "Cat"}}),
        encoding="utf-8",
    )
    mgr = InventoryManager(db_path=str(db_path))
    assert mgr.products["1"].name == "Old A"
    assert mgr.products["1"].barcode == ""
    assert mgr.products["1"].is_low_stock is True
    mgr.save_data()
    saved = json.loads(db_path.read_text(encoding="utf-8"))
    assert saved["1"]["barcode"] == ""
    assert saved["1"]["reorder_point"] == 5


def test_bug101_empty_name_falls_back(tmp_path):
    """BUG-101: missing name keys fall back to 'Unknown', not crash."""
    prod = Product.from_dict("0", {})
    assert prod.name == "Unknown"
    assert prod.quantity == 0
    assert prod.barcode == ""


# --------------------------------------------------------------------- CLI (3)
def test_cli_show_all_lists_products(manager, capsys):
    """CLI show_all prints every product including barcode column."""
    InventoryCLI(manager).show_all()
    out = capsys.readouterr().out
    assert "Item A" in out and "Item C" in out
    assert "Barcode" in out or "885" in out or "ID:" in out
    assert "[LOW]" in out  # Item C (4 <= 5) flagged


def test_cli_invalid_menu_choice(manager, monkeypatch, capsys):
    """CLI rejects out-of-range choices then exits cleanly."""
    inputs = iter(["9", "6"])
    monkeypatch.setattr("builtins.input", lambda *a: next(inputs))
    InventoryCLI(manager).run()
    out = capsys.readouterr().out
    assert "Invalid choice, please select 1-6." in out
    assert "Goodbye" in out


def test_cli_export_csv_writes_file(manager, tmp_path, capsys):
    """CLI export_csv path (menu 5) writes the report file."""
    out = tmp_path / "cli_report.csv"
    cli = InventoryCLI(manager)
    assert cli.export_csv(str(out)) == str(out)
    assert out.exists()
    assert "Success: CSV report written" in capsys.readouterr().out


# -------------------------------------------------------------- integration (3)
def test_integration_save_reload_preserves_evolution_fields(tmp_path):
    """Integration: full product state survives save -> reload."""
    db_path = tmp_path / "db.json"
    db_path.write_text("{}", encoding="utf-8")
    mgr = InventoryManager(db_path=str(db_path))
    mgr.add_or_update_product("1", "Evo", 6, 12.5, "Drink", "BAR1", 10)
    fresh = InventoryManager(db_path=str(db_path))
    prod = fresh.products["1"]
    assert (prod.barcode, prod.reorder_point, prod.is_low_stock) == ("BAR1", 10, True)


def test_integration_cut_stock_triggers_alert(manager):
    """Integration: cutting stock to the ROP raises a low-stock alert."""
    manager.cut_stock("2", 5)  # 10 -> 5, ROP 5
    assert manager.products["2"].is_low_stock is True
    assert "Item B" in manager.get_inventory_summary()["low_stock_list"]


def test_integration_atomic_save_no_tmp_left(manager, tmp_path):
    """Integration: atomic save leaves no .tmp residue behind."""
    manager.save_data()
    leftovers = list(tmp_path.glob("*.tmp"))
    assert leftovers == []
    reloaded = InventoryManager(db_path=manager.db_path)
    assert set(reloaded.products) == {"1", "2", "3"}
