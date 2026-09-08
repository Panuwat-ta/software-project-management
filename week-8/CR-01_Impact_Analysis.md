# วิเคราะห์ผลกระทบ CR-01 — Barcode & Reorder Point (CR-01 Impact Analysis)

## ใบคำขอ CR-01 (ที่มา: ENGSE225 Week 8 + ENGSE202 Week 8)
- **CR ID (ตัวอย่างทางการจาก transcript):** CR-01
- **คำขอ:** เพิ่มการเก็บรหัสบาร์โค้ด (Barcode) และจุดสั่งซื้อขั้นต่ำ (Reorder Point)
- **Requester (จาก transcript):** อาจารย์ / Sponsor
- **ข้อบังคับ ISO/IEC 14764 Step 1:** ห้ามรับคำขอผ่านวาจา/แช็ตส่วนตัว/ข้อตกลงลอยๆ — ต้องบันทึก CR Form (CR ID, Requester, Business Justification + สเปกใหม่)

## กระบวนการ ISO/IEC 14764 (ที่มา: ENGSE225 Week 8)
1. **Step 1 Identification:** รับและบันทึก CR Form
2. **Step 2 Impact Analysis:** ประเมินผลกระทบเชิงเทคนิคและงบประมาณ (Technical / Test / Cost → ส่งต่อวิชา SPM)
3. **Step 3 Implementation:** แตก Branch `feature/cr01-barcode-reorder-point` จาก `develop` → ลงมือตาม Impact → รัน pytest ผ่าน 100% (Full Regression Verification)

## ผลกระทบสรุป (ที่มา: ENGSE202 Week 8)
- **Cost Impact:** +**8 Man-Hours**
- **Technical Impact:** กระทบ **2 Class (Product, Repo)**
- **Test Impact:** เขียน PyTest เพิ่ม **3 Cases**

## Traceability Matrix — รายละเอียดจุดกระทบ (ที่มา: ENGSE225 Week 8)

| องค์ประกอบสถาปัตยกรรม | จุดกระทบเชิงเทคนิค (Affected Code) | ผลกระทบด้านการทดสอบ (Test Impact) |
|---|---|---|
| Class Product | เพิ่ม Attributes: `barcode: str` และ `reorder_point: int` | เพิ่ม Unit Test ตรวจชนิดข้อมูล |
| InventoryRepository | ปรับโครงสร้าง JSON serialization / deserialization คีย์ใหม่ | เพิ่ม Test Case อ่าน/เขียนไฟล์ |
| ConsoleUI | เพิ่มช่องรับ Input Barcode และแสดงเตือน Reorder Alert | ทดสอบ UI Mock Inputs |

> หมายเหตุความสอดคล้อง: ภาพรวมฝั่ง ENGSE202 สรุปว่า "กระทบ 2 Class (Product, Repo)" ส่วนตาราง Traceability ฝั่ง ENGSE225 ลงรายละเอียด 3 แถวรวม ConsoleUI — เอกสารนี้เก็บข้อความทั้งสองตาม transcript โดยไม่ตีความเพิ่ม

## บริบท Refactoring ก่อนรับ CR-01 (ที่มา: ENGSE225 Week 8)
- ผ่าตัด `app_v1.py` (หนี้: Global x, Cryptic Variables) บน Branch `feature/refactor-core-architecture`
- หลักการ: ปรับโครงสร้างภายในโดย**ไม่เปลี่ยนพฤติกรรมภายนอก** (ต่างจาก Bug Fix = แก้พฤติกรรมผิด, Feature Addition = เพิ่มพฤติกรรมใหม่)
- 4 เทคนิค: **Rename Variable/Method** (ชื่อลึกลับ `x, a, b` → Intent-Revealing; เพิ่ม Analyzability ตาม ISO 25010), **Extract Function** (ลด v(G) ของ `main()` จาก 22 → 8; เทสต์เฉพาะฟังก์ชันได้), **Extract Class** (Product ห่อหุ้ม id/name/qty/price + Type Safety; InventoryRepository ชั้น CRUD JSON แบบ Repository Pattern; InventoryService ชั้น Business Logic คำนวณรวม/ตัดสต็อก/ตรวจเงื่อนไข), **Encapsulate Field** (เลิก `global x`; ฉีด Repository เข้า Service ผ่าน Constructor — Dependency Injection)
- Safety: Baseline `pytest test_app.py` ต้อง `1 passed` ไฟเขียว 100% ก่อนแตะโค้ด → แก้ทีละน้อย → รัน pytest ซ้ำทันที → ไฟแดงใช้ `git checkout` ถอยกลับ
- การส่งต่อสู่ SPM (จาก transcript): นำ Man-Hours ไปประเมินงบเพิ่มเติม ดึง Contingency Reserve และปรับการ์ดงานบน Jira

## การทูต/การสื่อสาร (ที่มา: ENGSE202 Week 8)
- ไม่รับ CR-01 กลาง Sprint 1 ทันทีและไม่ปฏิเสธรุนแรง — ชี้แจงด้วย Impact Analysis แล้วจัดลำดับเข้า **Sprint 2** พร้อมทางเลือก: ขยายงบจาก Contingency Reserve หรือตัด Scope ไม่สำคัญออก

> หมายเหตุ: transcript ไม่ได้แจกแจง 8 Man-Hours เป็นรายกิจกรรม (ออกแบบ/โค้ด/ทดสอบ/เอกสาร) ไม่ได้ระบุชื่อเมธอด/แฟล็ก CLI/จำนวนเค pytest รวม และไม่มี ticket ID สำหรับ CR-01 (นอกจากตัวอย่าง Issue Key `ENGSE-201` ในบริบท Automation) — ตัวเลขเหล่านั้นจึงถูกลบออกแล้ว
