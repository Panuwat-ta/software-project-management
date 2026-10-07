import os
import json
import tempfile
import pytest
from app import (
    InventoryManager,
    Product,
    SQLiteDatabaseContext,
    InventoryRepository,
    MemberManager,
    Member,
    CheckoutService,
    normalize_tier,
    discount_rate_for,
    migrate_json_to_sqlite,
)

@pytest.fixture
def manager():
    """Fixture สำหรับเตรียมฐานข้อมูลจำลองก่อนการรันทดสอบแต่ละครั้ง"""
    # สร้าง temporary file สำหรับฐานข้อมูลจำลอง
    temp_db = tempfile.NamedTemporaryFile(
        delete=False, suffix=".json", mode="w", encoding="utf-8"
    )
    temp_db.write("{}")
    temp_db.close()
    
    # เริ่มต้น InventoryManager ด้วยไฟล์จำลอง
    mgr = InventoryManager(db_path=temp_db.name)
    
    # กำหนดข้อมูลจำลองเพื่อการทดสอบ
    mgr.products = {
        "1": Product("1", "Item A", 20, 100.0, "Cat 1"), # มูลค่า = 2000
        "2": Product("2", "Item B", 10, 50.0, "Cat 2"),  # มูลค่า = 500
        "3": Product("3", "Item C", 4, 200.0, "Cat 3"),  # 800, low
    }
    mgr.save_data()
    
    yield mgr
    
    # ลบไฟล์ชั่วคราวหลังทดสอบเสร็จสิ้น (Teardown)
    if os.path.exists(temp_db.name):
        os.remove(temp_db.name)

def test_calculate_inventory_summary(manager):
    """ทดสอบความถูกต้องของการคำนวณมูลค่ารวมและตรวจประเภทสินค้า"""
    summary = manager.get_inventory_summary()
    assert summary['total_types'] == 3
    assert summary['total_value'] == 3300.0
    assert "Item C" in summary['low_stock_list']
    assert "Item A" not in summary['low_stock_list']

def test_cut_stock_success(manager):
    """ทดสอบการหักสต็อกสำเร็จเมื่อมีสินค้าพอเพียง"""
    success, msg, remaining = manager.cut_stock("1", 5)
    assert success is True
    assert remaining == 15
    assert manager.products["1"].quantity == 15

def test_cut_stock_not_enough(manager):
    """ทดสอบการหักสต็อกล้มเหลวเมื่อจำนวนที่ขอตัดยอดเกินกว่าที่มีในสต็อก"""
    success, msg, remaining = manager.cut_stock("2", 15)
    assert success is False
    assert msg == "Error: Not enough stock!"
    assert remaining == 10

def test_cut_stock_not_found(manager):
    """ทดสอบการตัดสต็อกด้วย ID ที่ไม่มีในระบบ"""
    success, msg, remaining = manager.cut_stock("999", 5)
    assert success is False
    assert msg == "Product not found!"
    assert remaining is None

def test_add_or_update_product(manager):
    """ทดสอบการเพิ่มสินค้าใหม่และอัปเดตข้อมูลสินค้าเดิม"""
    # เพิ่มสินค้าใหม่
    manager.add_or_update_product("4", "Item D", 100, 5.0, "Cat 4")
    assert "4" in manager.products
    assert manager.products["4"].name == "Item D"
    
    # อัปเดตสินค้าเดิม
    manager.add_or_update_product("1", "Item A+", 30, 120.0, "Cat 1")
    assert manager.products["1"].name == "Item A+"
    assert manager.products["1"].quantity == 30


# ---------------- Sprint 2 (v3.0) tests ----------------

@pytest.fixture
def sqlite_ctx(tmp_path):
    """Fixture: isolated Singleton SQLite context per test."""
    SQLiteDatabaseContext.reset()
    ctx = SQLiteDatabaseContext.getInstance(str(tmp_path / "t.db"))
    yield ctx
    SQLiteDatabaseContext.reset()


@pytest.fixture
def repo(sqlite_ctx):
    """Fixture: empty inventory repository."""
    return InventoryRepository(sqlite_ctx)


@pytest.fixture
def members(sqlite_ctx):
    """Fixture: empty member manager sharing the same DB."""
    return MemberManager(sqlite_ctx)


@pytest.fixture
def checkout(repo, members):
    """Fixture: checkout service over empty repo/members."""
    return CheckoutService(repo, members)


def test_singleton_same_instance(tmp_path):
    """ขอ connection ซ้ำต้องได้ instance เดียว (SPM-23)."""
    SQLiteDatabaseContext.reset()
    try:
        db_path = str(tmp_path / "s.db")
        first = SQLiteDatabaseContext.getInstance(db_path)
        second = SQLiteDatabaseContext.getInstance(db_path)
        assert first is second
    finally:
        SQLiteDatabaseContext.reset()


def test_parameterized_blocks_sql_injection(repo):
    """input อันตรายต้องเป็น string ธรรมดา ไม่หลุดเป็น SQL."""
    repo.save(Product("P1", "Sugar", 10, 20.0, "Food"))
    evil = "' OR '1'='1"
    assert repo.find_by_id(evil) is None
    assert repo.count_products() == 1
    assert repo.find_by_id("P1") is not None
    # พยายาม DROP TABLE ผ่าน id ต้องไม่พังตาราง
    repo.find_by_id('"; DROP TABLE products; --')
    assert repo.count_products() == 1
    assert repo.total_value() == 200.0


def test_migrate_json_to_sqlite_verifies(repo, tmp_path):
    """ย้าย JSON legacy แล้วจำนวน+มูลค่าต้องตรง 100% (SPM-24)."""
    payload = {
        "A1": {"n": "Legacy X", "q": 5, "p": 100.0, "c": "Food"},
        "A2": {
            "name": "New Y", "quantity": 2, "price": 50.0,
            "category": "Drink", "barcode": "B1",
            "reorder_point": 3,
        },
    }
    json_path = str(tmp_path / "data.json")
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle)
    stats = migrate_json_to_sqlite(json_path, repo)
    assert stats["json_count"] == 2
    assert stats["sqlite_count"] == 2
    assert stats["json_total"] == 600.0
    assert stats["sqlite_total"] == 600.0
    assert stats["match"] is True
    legacy = repo.find_by_id("A1")
    assert legacy.name == "Legacy X"
    assert legacy.barcode == ""
    assert legacy.reorder_point == 5


def test_member_crud_four_tiers(members):
    """CRUD สมาชิกครบ 4 tier พร้อมอัตราส่วนลดถูกต้อง (SPM-25)."""
    tiers = [
        ("M1", "Regular User", "Regular", 0.0),
        ("M2", "Silver User", "Silver", 0.05),
        ("M3", "Gold User", "Gold", 0.10),
        ("M4", "Platinum User", "Platinum", 0.15),
    ]
    for member_id, name, tier, _rate in tiers:
        members.save_member(Member(member_id, name, tier))
    for member_id, _name, tier, rate in tiers:
        found = members.find_by_id(member_id)
        assert found is not None
        assert found.tier == tier
        assert found.discount_rate == rate
    assert len(members.find_all()) == 4
    # แก้ไข tier แล้วต้องเปลี่ยนตาม
    members.save_member(Member("M2", "Silver User", "Gold"))
    assert members.find_by_id("M2").tier == "Gold"
    # ลบแล้วต้องหาย
    assert members.delete_member("M1") is True
    assert members.find_by_id("M1") is None


def test_member_invalid_tier_fallback_regular(members):
    """tier ผิด/ว่างต้อง fallback Regular โดยไม่ error (SPM-25)."""
    assert normalize_tier("Diamond") == "Regular"
    assert normalize_tier("") == "Regular"
    assert normalize_tier(None) == "Regular"
    assert discount_rate_for("Weird") == 0.0
    odd = Member("MX", "Odd", "Diamond")
    assert odd.tier == "Regular"
    assert odd.discount_rate == 0.0
    members.save_member(odd)
    found = members.find_by_id("MX")
    assert found.tier == "Regular"
    assert found.discount_rate == 0.0


def test_checkout_gold_discount_receipt(repo, members, checkout):
    """Gold ซื้อ 1,000 ต้องเหลือ 900 พร้อมใบเสร็จแยกบรรทัด."""
    repo.save(Product("G1", "Gold Item", 10, 500.0, "General"))
    members.save_member(Member("MG", "Gold Member", "Gold"))
    ok, receipt, remaining = checkout.process_checkout(
        "G1", "MG", 2
    )
    assert ok is True
    assert receipt["subtotal"] == 1000.0
    assert receipt["tier"] == "Gold"
    assert receipt["discount_rate"] == 0.10
    assert receipt["discount_value"] == 100.0
    assert receipt["grand_total"] == 900.0
    assert remaining == 8
    assert repo.find_by_id("G1").quantity == 8


def test_checkout_guest_full_price_and_stock_cut(
    repo, members, checkout
):
    """guest (ไม่มีสมาชิก) จ่ายเต็ม พร้อมตัดสต็อก (SPM-26)."""
    repo.save(Product("P9", "Plain", 10, 100.0, "General"))
    ok, receipt, remaining = checkout.process_checkout(
        "P9", None, 3
    )
    assert ok is True
    assert receipt["tier"] == "Regular"
    assert receipt["discount_value"] == 0.0
    assert receipt["grand_total"] == 300.0
    assert remaining == 7
    # member id ที่ไม่มีจริงต้องเป็น guest เช่นกัน
    ok2, receipt2, _rest = checkout.process_checkout(
        "P9", "NO-SUCH-MEMBER", 1
    )
    assert ok2 is True
    assert receipt2["tier"] == "Regular"
    assert receipt2["grand_total"] == 100.0
    # ของไม่พอต้องล้มเหลวพร้อมจำนวนคงเหลือ
    bad_ok, _msg, current = checkout.process_checkout(
        "P9", None, 99
    )
    assert bad_ok is False
    assert current == 6


def test_checkout_keeps_reorder_alert(repo, members, checkout):
    """ตัดสต็อกพร้อมกัน alert จุดสั่งซื้อยังทำงาน (SPM-26)."""
    repo.save(
        Product("L1", "Low Item", 5, 10.0, "General",
                barcode="B1", reorder_point=5)
    )
    assert repo.find_by_id("L1").is_low_stock is True
    ok, receipt, remaining = checkout.process_checkout(
        "L1", None, 1
    )
    assert ok is True
    assert remaining == 4
    assert receipt["low_stock"] is True
    alerts = repo.get_low_stock_alerts()
    assert [p.product_id for p in alerts] == ["L1"]
    summary = repo.get_inventory_summary()
    assert "Low Item" in summary["low_stock_list"]


def test_backward_compat_legacy_json_keys(tmp_path):
    """JSON เก่า (n/q/p/c, ไร้ barcode) โหลดได้ไม่ KeyError."""
    payload = {"77": {"n": "Old", "q": 3, "p": 9.0, "c": "Food"}}
    json_path = str(tmp_path / "legacy.json")
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle)
    manager = InventoryManager(db_path=json_path)
    assert manager.products["77"].name == "Old"
    assert manager.products["77"].barcode == ""
    assert manager.products["77"].reorder_point == 5


# โค้ดส่วนนี้จะทำงานเมื่อสั่งรัน `python test_app.py` โดยตรง
# เพื่อเรียกใช้งาน PyTest พร้อม Plugin เซฟผลลัพธ์เป็นไฟล์ JSON อัตโนมัติ
if __name__ == "__main__":
    import sys

    class JSONReportPlugin:
        """Plugin ภายในเพื่อดักจับผลลัพธ์การรัน PyTest และเซฟลง JSON"""
        def __init__(self):
            self.results = []
            
        @pytest.hookimpl(tryfirst=True, hookwrapper=True)
        def pytest_runtest_makereport(self, item, call):
            outcome = yield
            report = outcome.get_result()
            # สนใจเฉพาะตอน call (คือตอนรันเทสจริง ไม่นับ setup/teardown)
            if report.when == "call":
                doc = item.function.__doc__ or ""
                status = "PASS" if report.passed else "FAIL"
                if not report.passed and not report.failed:
                    status = "ERROR"
                self.results.append({
                    "test_name": item.name,
                    "description": doc.strip(),
                    "status": status,
                    "message": str(report.longrepr)
                    if report.failed else ""
                })

        def pytest_sessionfinish(self, session, exitstatus):
            passed = sum(
                1 for r in self.results if r["status"] == "PASS"
            )
            failed = sum(
                1 for r in self.results if r["status"] == "FAIL"
            )
            errors = sum(
                1 for r in self.results if r["status"] == "ERROR"
            )
            output = {
                "summary": {
                    "total_tests": len(self.results),
                    "passed": passed,
                    "failures": failed,
                    "errors": errors,
                    "was_successful": exitstatus == 0
                },
                "test_cases": self.results
            }
            base = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base, "test.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, ensure_ascii=False)
            print(f"\n[PyTest] results saved to {json_path}")

    # รัน Pytest แบบใช้พารามิเตอร์ -v (verbose) เพื่อแสดงสีและคำอธิบาย
    plugin = JSONReportPlugin()
    sys.exit(pytest.main(["-v", __file__], plugins=[plugin]))
