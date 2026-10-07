# SPM-24 — Migrate JSON Data to SQLite with Verification

- Jira: `SPM-24` (3 SP) → Done, comment ผูกโค้ดแล้ว
- เรื่องเล่า: ในฐานะผู้ดูแลข้อมูล ฉันต้องการสคริปต์ย้าย
  `data.json` (รวม legacy keys `n`/`q`/`p`/`c` และ
  `barcode`/`reorder`) ไป SQLite พร้อมยืนยันความถูกต้อง

## เกณฑ์ยอมรับ → หลักฐาน

1. มีไฟล์ JSON เดิม รันสคริปต์ย้ายแล้วจำนวนระเบียนและมูลค่า
   รวมต้องตรงกัน 100% → `migrate_json_to_sqlite` คืน
   `{migrated, json_count, sqlite_count, json_total,
   sqlite_total, match}`; เทสต์ `test_migrate_json_to_sqlite_verifies`
   ใช้ JSON ผสมคีย์เก่า/ใหม่ 2 ระเบียน ยอด 600.0 ตรงกัน
   (`match: True`)
2. ย้ายเสร็จรัน regression แล้วต้องเขียวทั้งหมด →
   `test_app.py` 14 passed, `Phase4/Sprint4/week-12/test_app.py`
   25 passed

## โค้ดและพฤติกรรม

- `app.py`: `migrate_json_to_sqlite` อ่านผ่าน
  `Product.from_dict` (fallback คีย์สั้น + ค่าเริ่มต้น
  `barcode=""`/`reorder_point=5` ต่อเนื่องจาก BUG-101),
  `seed_default_products` เติมสินค้าตัวอย่าง 3 รายการเมื่อ DB ว่าง
- CLI (`__main__`): ถ้า `inventory.db` ว่างและมี `data.json`
  จะ auto-migrate พร้อมพิมพ์สรุป แล้วค่อย seed/รันเมนู
