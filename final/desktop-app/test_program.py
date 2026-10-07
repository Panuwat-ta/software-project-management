"""Integration tests for the GTK4 desktop program domain bridge."""


from app import Member, Product, SQLiteDatabaseContext
from program import (
    build_backend,
    format_receipt,
    product_status,
    responsive_layout_mode,
    sidebar_width_for_window,
    summary_metrics,
)


def teardown_function():
    SQLiteDatabaseContext.reset()


def test_responsive_layout_breakpoints():
    assert responsive_layout_mode(1200) == "desktop"
    assert responsive_layout_mode(980) == "desktop"
    assert responsive_layout_mode(979) == "compact"
    assert responsive_layout_mode(760) == "compact"
    assert responsive_layout_mode(759) == "narrow"
    assert responsive_layout_mode(640) == "narrow"
    assert sidebar_width_for_window(1184) == 394
    assert sidebar_width_for_window(900) == 300
    assert sidebar_width_for_window(640) == 213


def test_program_backend_creates_seed_data(tmp_path):
    db, repo, members, checkout = build_backend(
        tmp_path / "ui.db", legacy_json=None, seed=True
    )
    assert db is not None
    assert members is not None
    assert checkout is not None
    assert repo.count_products() == 3


def test_program_dashboard_metrics(tmp_path):
    _db, repo, _members, _checkout = build_backend(
        tmp_path / "ui.db", legacy_json=None, seed=False
    )
    repo.save(Product("A1", "Milk", 2, 25.0, "Drink", reorder_point=3))
    repo.save(Product("A2", "Water", 10, 10.0, "Drink", reorder_point=2))
    metrics = summary_metrics(repo)
    assert metrics == {
        "total_types": 2,
        "total_value": 150.0,
        "low_stock_count": 1,
    }


def test_program_product_status(tmp_path):
    _db, repo, _members, _checkout = build_backend(
        tmp_path / "ui.db", legacy_json=None, seed=False
    )
    low = Product("P1", "Low", 2, 10.0, "General", reorder_point=2)
    ok = Product("P2", "OK", 3, 10.0, "General", reorder_point=2)
    assert product_status(low) == "LOW"
    assert product_status(ok) == "OK"


def test_program_member_checkout_uses_discount(tmp_path):
    _db, repo, members, checkout = build_backend(
        tmp_path / "ui.db", legacy_json=None, seed=False
    )
    repo.save(Product("P1", "Keyboard", 10, 500.0, "IT", reorder_point=2))
    members.save_member(Member("M1", "Gold User", "Gold"))
    ok, receipt, remaining = checkout.process_checkout("P1", "M1", 2)
    assert ok is True
    assert receipt["subtotal"] == 1000.0
    assert receipt["discount_value"] == 100.0
    assert receipt["grand_total"] == 900.0
    assert remaining == 8


def test_program_receipt_format():
    text = format_receipt(
        {
            "product_name": "Keyboard",
            "product_id": "P1",
            "quantity": 2,
            "unit_price": 500.0,
            "subtotal": 1000.0,
            "tier": "Gold",
            "discount_rate": 0.10,
            "discount_value": 100.0,
            "grand_total": 900.0,
            "remaining": 8,
        }
    )
    assert "Keyboard" in text
    assert "Gold (10%)" in text
    assert "900.00" in text


def test_program_csv_export_through_repo(tmp_path):
    from app import CsvReportExporter

    _db, repo, _members, _checkout = build_backend(
        tmp_path / "ui.db", legacy_json=None, seed=False
    )
    repo.save(Product("P1", "Milk", 3, 20.0, "Drink"))
    out = tmp_path / "report.csv"
    CsvReportExporter.export_repo(repo, str(out))
    content = out.read_text(encoding="utf-8")
    assert "ProductID" in content
    assert "P1" in content
    assert "Milk" in content
