# SPM-30 — B. Dashboard + Products Desktop UI

- Jira: `SPM-30` (8 SP) → Done
- งาน: หน้า Dashboard และ Products ในโปรแกรม Desktop

## เกณฑ์ยอมรับ → หลักฐาน

1. Dashboard แสดงจำนวนประเภทสินค้า มูลค่าคงคลัง และจำนวนสินค้าใกล้หมด
2. แสดงรายการสินค้าที่ quantity <= reorder point
3. หน้า Products ค้นหารหัส/ชื่อ/หมวดหมู่ได้
4. เพิ่ม/แก้ไขสินค้าได้จากฟอร์ม
5. ตัดสต็อก ลบสินค้า และ Export CSV ได้
6. สถานะแสดง LOW / OK จาก `Product.is_low_stock`

## โค้ด

- `program.py` — `_build_dashboard`, `_build_products`,
  `refresh_dashboard`, `refresh_products`
- `app.py` — `InventoryRepository`, `CsvReportExporter`
