import unittest
import os
import tempfile
from app_v2 import InventoryManager, Product

class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        # สร้าง temporary file สำหรับฐานข้อมูลจำลอง
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8")
        self.temp_db.write("{}")
        self.temp_db.close()
        
        # เริ่มต้น InventoryManager ด้วยไฟล์จำลอง
        self.manager = InventoryManager(db_path=self.temp_db.name)
        
        # เคลียร์ข้อมูลดีฟอลต์ (ถ้ามี) และสร้างข้อมูลจำลองเพื่อการทดสอบโดยเฉพาะ
        self.manager.products = {
            "1": Product("1", "Item A", 20, 100.0, "Cat 1"), # มูลค่า = 2000
            "2": Product("2", "Item B", 10, 50.0, "Cat 2"),  # มูลค่า = 500
            "3": Product("3", "Item C", 4, 200.0, "Cat 3"),  # มูลค่า = 800 (สต็อกต่ำกว่า 10)
        }
        self.manager.save_data()

    def tearDown(self):
        # ลบไฟล์ชั่วคราวหลังทดสอบเสร็จสิ้น
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_calculate_inventory_summary(self):
        """ทดสอบความถูกต้องของการคำนวณมูลค่ารวมและตรวจประเภทสินค้า"""
        summary = self.manager.get_inventory_summary()
        
        # 1. จำนวนประเภทสินค้าทั้งหมดต้องเป็น 3
        self.assertEqual(summary['total_types'], 3)
        
        # 2. มูลค่ารวมคลังสินค้า = (20*100) + (10*50) + (4*200) = 2000 + 500 + 800 = 3300
        self.assertEqual(summary['total_value'], 3300.0)
        
        # 3. สินค้าที่สต็อกต่ำกว่า 10 ชิ้น คือ Item C (มี 4 ชิ้น)
        self.assertIn("Item C", summary['low_stock_list'])
        self.assertNotIn("Item A", summary['low_stock_list'])
        self.assertNotIn("Item B", summary['low_stock_list'])

    def test_cut_stock_success(self):
        """ทดสอบการหักสต็อกสำเร็จเมื่อมีสินค้าพอเพียง"""
        success, msg, remaining = self.manager.cut_stock("1", 5)
        self.assertTrue(success)
        self.assertEqual(remaining, 15)
        self.assertEqual(self.manager.products["1"].quantity, 15)

    def test_cut_stock_not_enough(self):
        """ทดสอบการหักสต็อกล้มเหลวเมื่อจำนวนที่ขอตัดยอดเกินกว่าที่มีในสต็อก"""
        success, msg, remaining = self.manager.cut_stock("2", 15)
        self.assertFalse(success)
        self.assertEqual(msg, "Error: Not enough stock!")
        self.assertEqual(remaining, 10) # สต็อกต้องไม่เปลี่ยน

    def test_cut_stock_not_found(self):
        """ทดสอบการตัดสต็อกด้วย ID ที่ไม่มีในระบบ"""
        success, msg, remaining = self.manager.cut_stock("999", 5)
        self.assertFalse(success)
        self.assertEqual(msg, "Product not found!")
        self.assertIsNone(remaining)

    def test_add_or_update_product(self):
        """ทดสอบการเพิ่มสินค้าใหม่และอัปเดตข้อมูลสินค้าเดิม"""
        # เพิ่มสินค้าใหม่
        self.manager.add_or_update_product("4", "Item D", 100, 5.0, "Cat 4")
        self.assertIn("4", self.manager.products)
        self.assertEqual(self.manager.products["4"].name, "Item D")
        
        # อัปเดตสินค้าที่มีอยู่
        self.manager.add_or_update_product("1", "Item A+", 30, 120.0, "Cat 1")
        self.assertEqual(self.manager.products["1"].name, "Item A+")
        self.assertEqual(self.manager.products["1"].quantity, 30)

class JSONTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_details = []

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return str(test).split()[0] + " - " + doc_first_line
        else:
            return str(test)

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        self.test_details.append({
            "test_name": test._testMethodName,
            "description": test.shortDescription(),
            "status": "PASS",
            "message": ""
        })
        if self.showAll:
            self.stream.writeln("\033[92mOK\033[0m")
        elif self.dots:
            self.stream.write('\033[92m.\033[0m')
            self.stream.flush()

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        self.test_details.append({
            "test_name": test._testMethodName,
            "description": test.shortDescription(),
            "status": "FAIL",
            "message": self._exc_info_to_string(err, test)
        })
        if self.showAll:
            self.stream.writeln("\033[91mFAIL\033[0m")
        elif self.dots:
            self.stream.write('\033[91mF\033[0m')
            self.stream.flush()

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        self.test_details.append({
            "test_name": test._testMethodName,
            "description": test.shortDescription(),
            "status": "ERROR",
            "message": self._exc_info_to_string(err, test)
        })
        if self.showAll:
            self.stream.writeln("\033[91mERROR\033[0m")
        elif self.dots:
            self.stream.write('\033[91mE\033[0m')
            self.stream.flush()

class JSONTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return JSONTestResult(self.stream, self.descriptions, self.verbosity)

if __name__ == '__main__':
    import json
    import sys
    
    # โหลดชุดทดสอบ
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInventoryManager)
    
    # รันการทดสอบพร้อมแสดงผลลัพธ์
    runner = JSONTestRunner(stream=sys.stderr, verbosity=2)
    result = runner.run(suite)
    
    # สรุปผลลัพธ์เป็นโครงสร้าง Dictionary
    output = {
        "summary": {
            "total_tests": result.testsRun,
            "passed": result.testsRun - len(result.failures) - len(result.errors),
            "failures": len(result.failures),
            "errors": len(result.errors),
            "was_successful": result.wasSuccessful()
        },
        "test_cases": result.test_details
    }
    
    # บันทึกข้อมูลลง test.json
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
        
    print(f"Test results generated and saved to {json_path}")
    sys.exit(not result.wasSuccessful())
