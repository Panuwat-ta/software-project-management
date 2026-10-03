# SPM-23 — SQLite Database Layer (Singleton + Parameterized)

- Jira: `SPM-23` (5 SP) → Done, comment ผูกโค้ดแล้ว
- เรื่องเล่า: ในฐานะนักพัฒนา ฉันต้องการชั้นฐานข้อมูล SQLite
  แบบ Singleton ที่ใช้ parameterized query เพื่อให้ทนทานและ
  กัน SQL injection

## เกณฑ์ยอมรับ → หลักฐาน

1. มี `SQLiteDatabaseContext` ขอ connection ซ้ำต้องได้ instance
   เดียว → `getInstance(db_path)` คืน instance เดียวต่อ path,
   `reset()` สำหรับเทสต์; เทสต์ `test_singleton_same_instance`
   ผ่าน
2. คำสั่งเขียน/อ่านต้องใช้ parameterized query 100% ไม่มี
   string-concat SQL → ทุก `execute` ใช้ `?` placeholders;
   ตรวจด้วย grep ไม่พบ f-string SQL; `bandit -r app.py` 0 issues

## โค้ด

- `app.py`: `SQLiteDatabaseContext` (`getInstance`/`reset`/
  `execute`/`commit`/`rollback`/`close`, สร้างตาราง `products`
  กับ `members` พร้อม `CHECK` กันค่าติดลบ),
  `InventoryRepository` (`save`/`find_by_id`/`find_all`/
  `update_stock`/`delete`/`count_products`/`total_value`/
  `get_low_stock_alerts`/`get_inventory_summary`)
- ทุก write มี commit/rollback ป้องกันข้อมูลค้างกลางคัน
