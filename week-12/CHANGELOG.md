# บันทึกการเปลี่ยนแปลง — ระบบสินค้าคงคลัง (วิวัฒนาการสัปดาห์ที่ 12)

อ้างอิง: ENGSE225 Week 12 (SemVer 2.0.0, ISO/IEC 14764, Keep a Changelog)
รายการทั้งหมดเป็นข้อมูลสมมติเพื่อใช้ในการเรียน ปฏิบัติตาม SemVer
จาก v1.0.0-baseline ขยับเป็น v2.0.0-evolution เพราะมีการเปลี่ยนสถาปัตยกรรมใหญ่
และเพิ่มโมเดลข้อมูลทางธุรกิจใหม่

## [2.0.0-evolution] - 2026-08-31

### Added

- ฟังก์ชันใหม่ Barcode (CR-01): `Product.barcode` (ค่าเริ่มต้น `""`)
  รับค่าผ่านขั้นตอนเพิ่ม/อัปเดตใน CLI รวมอยู่ในการจัดเก็บ JSON และรายงาน CSV
- ฟังก์ชันใหม่ Reorder Alert (CR-02): `Product.reorder_point` (ค่าเริ่มต้น `5`),
  `is_low_stock` (`quantity <= reorder_point`) และ `InventoryManager.get_low_stock_alerts()`
- ฟังก์ชันใหม่ CSV Export (CR-02): `CsvReportExporter` พร้อมหัวตาราง
  `ProductID,ProductName,Barcode,Quantity,ReorderPoint,Price` และเมนู CLI 5 (ส่งออกรายงาน CSV)

### Changed

- เปลี่ยนโครงสร้างสู่ Layered Architecture (Repository Pattern):
  ขยายสกีมา `Product.to_dict` / `from_dict` ด้วย `barcode` และ `reorder_point`,
  จัดเลขเมนู CLI ใหม่ (ทางออกย้ายจาก 5 → 6),
  คำเตือนสินค้าใกล้หมดอ้างอิงจุดสั่งซื้อซ้ำของแต่ละสินค้า

### Removed

- ลบตัวแปรสปาเก็ตตี global x (ผ่าตัด Refactoring ป้องกันข้อผิดพลาดอนาคต)

### Fixed

- แก้ไขบั๊กแครชเมื่อเจอไฟล์ JSON ไร้บาร์โค้ด (BUG-101):
  `from_dict` รองรับคีย์สั้นแบบเดิม (`n`/`q`/`p`/`c`) และ
  กำหนดค่าเริ่มต้น `barcode`/`reorder_point` ที่ขาดหายเป็น `""`/`5`

### ประวัติการบำรุงรักษา (ISO/IEC 14764 — ครบ 3 มิติ)

- **Preventive:** ผ่าตัดลบ global x ปรับสถาปัตยกรรมสู่ Repository Pattern เพื่อป้องกันข้อผิดพลาดอนาคต
- **Corrective:** สืบสวนรากเหง้าปัญหา (RCA) และแก้ไขบั๊ก Legacy Data Schema (BUG-101)
- **Perfective:** พัฒนาฟีเจอร์บาร์โค้ด (CR-01) และระบบออกรายงาน CSV (CR-02) ตามความต้องการใหม่

หลักฐานปล่อย: UAT 3 Scenarios ผ่าน 100% (ลงนามครบ), Full Suite PyTest 25 tests
ผ่าน 100% บนสาขา main, Git Tag `v2.0.0-evolution` (Annotated Tag พร้อมชื่อผู้สร้าง วันเวลา Metadata)
