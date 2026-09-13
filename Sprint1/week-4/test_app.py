import os
import tempfile
import pytest
from app import InventoryManager, Product

@pytest.fixture
def manager():
    """Fixture สำหรับเตรียมฐานข้อมูลจำลองก่อนการรันทดสอบแต่ละครั้ง"""
    # สร้าง temporary file สำหรับฐานข้อมูลจำลอง
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8")
    temp_db.write("{}")
    temp_db.close()
    
    # เริ่มต้น InventoryManager ด้วยไฟล์จำลอง
    mgr = InventoryManager(db_path=temp_db.name)
    
    # กำหนดข้อมูลจำลองเพื่อการทดสอบ
    mgr.products = {
        "1": Product("1", "Item A", 20, 100.0, "Cat 1"), # มูลค่า = 2000
        "2": Product("2", "Item B", 10, 50.0, "Cat 2"),  # มูลค่า = 500
        "3": Product("3", "Item C", 4, 200.0, "Cat 3"),  # มูลค่า = 800 (สต็อกต่ำกว่า 10)
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


# โค้ดส่วนนี้จะทำงานเมื่อสั่งรัน `python test_app1.py` โดยตรง
# เพื่อเรียกใช้งาน PyTest พร้อม Plugin เซฟผลลัพธ์เป็นไฟล์ JSON อัตโนมัติ
if __name__ == "__main__":
    import sys
    import json

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
                self.results.append({
                    "test_name": item.name,
                    "description": item.function.__doc__.strip() if item.function.__doc__ else "",
                    "status": "PASS" if report.passed else "FAIL" if report.failed else "ERROR",
                    "message": str(report.longrepr) if report.failed else ""
                })

        def pytest_sessionfinish(self, session, exitstatus):
            output = {
                "summary": {
                    "total_tests": len(self.results),
                    "passed": sum(1 for r in self.results if r["status"] == "PASS"),
                    "failures": sum(1 for r in self.results if r["status"] == "FAIL"),
                    "errors": sum(1 for r in self.results if r["status"] == "ERROR"),
                    "was_successful": exitstatus == 0
                },
                "test_cases": self.results
            }
            json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, ensure_ascii=False)
            print(f"\n[PyTest Custom Plugin] Test results generated and saved to {json_path}")

    # รัน Pytest แบบใช้พารามิเตอร์ -v (verbose) เพื่อแสดงสีและคำอธิบาย
    plugin = JSONReportPlugin()
    sys.exit(pytest.main(["-v", __file__], plugins=[plugin]))
