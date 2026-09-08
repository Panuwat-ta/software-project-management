# การเปลี่ยนผ่านสปรินต์ (Sprint Transition) — ปิด Sprint 1 → เปิด Sprint 2

## 1. สคริปต์เดโมรีวิวสปรินต์ (Sprint Review Demo Script)

สาธิตด้วย Working Software ที่รันได้จริงเท่านั้น ห้ามใช้สไลด์นิ่ง ("Working software is the primary measure of progress." — Agile Manifesto) เป้าหมาย Sprint 1: โชว์โครงสร้างใหม่ รัน PyTest ไฟเขียว 100% ไร้ global x

1. **Show Architecture:** เปิดโครงสร้างไฟล์แสดงคลาส Product, InventoryRepository, InventoryService
2. **Run PyTest Suite:** สั่งรัน `pytest -v` ใน Terminal โชว์ไฟเขียว 100% ต่อหน้า Sponsor
3. **Demonstrate Execution:** สั่งรันโปรแกรมคลังสินค้า ทดลองเพิ่ม/ลดสต็อกและคำนวณราคารวม
4. **ภาพรวม EVM (2 นาที):** PV 4,000 / EV 3,000 / AC 4,200 → SV −1,000 (Behind ), CV −1,200 (Over ) ชดเชยส่วนเกินจาก Contingency Reserve สัปดาห์ที่ 5

## 2. ความเร็วทีม (Velocity)

Team Velocity คือปริมาณงานที่ส่งมอบเสร็จจริงตาม DoD ใน 1 Sprint — ตัวอย่างตามบทเรียน: ตั้งเป้าไว้ 20 Points ทำเสร็จจริง 15 Points  Velocity = 15 Points ใช้เป็นเกณฑ์ดึงงานเข้า Sprint 2 ห้ามดึงเกิน 15 Points เด็ดขาด เพื่อกันทีมล้า

- Velocity Sprint 1 = **15 Points** (ตั้งเป้า 20 Points)
- ความจุ Sprint 2 คุมไม่ให้เกิน **15 Points**

## 3. ปิด Sprint 1 บน Jira (Close Sprint 1)

1. เข้าหน้า Active Sprints กดปุ่ม "Complete Sprint"
2. ตรวจสอบรายการ Completed Tasks และย้ายงานไม่เสร็จกลับ Backlog
3. สังเกตระบบ Jira บันทึกค่า Team Velocity ของ Sprint 1 อัตโนมัติ
4. คำนวณ EVM (SV = EV − PV, CV = EV − AC) วิเคราะห์สาเหตุ (หนี้เทคนิคใน app_v1.py + เสียเวลา Merge Conflict) แล้วบันทึก Retro (ดู EVM_Sprint1.md, Retrospective_Sprint1.md)

## 4. ผสานงาน Sprint 1 เข้า develop (Merge + Conflict Workflow)

ย้ายโค้ด Refactoring จาก `feature/refactor-core-architecture` เข้าสู่ `develop` ป้องกัน Long-Lived Branches ที่ก่อ Merge Conflict รุนแรง (Conflict เกิดเมื่อบรรทัดเดียวกันในไฟล์เดียวกันถูกแก้ไม่ตรงกันโดย 2 คนคนละสายงาน สัปดาห์ที่ 8 รื้อโครงสร้างหนักจึงเสี่ยงสูง)

ด่านตรวจก่อนกด Confirm Merge บน GitHub (4 ข้อ): Peer Code Review อนุมัติอย่างน้อย 1 คน, Clean Code ไม่มี global x, GitHub Actions รัน pytest ไฟเขียว 100%, เคลียร์ No Unresolved Conversations ครบ

ยุทธวิธีแก้ Merge Conflict (5 ขั้น): 1) `git checkout develop && git pull` 2) `git merge develop` บนสาย feature 3) Resolve ใน IDE (Accept Current / Incoming / Both) 4) รัน `pytest` ยืนยันตรรกะไม่พัง 5) Commit "fix: Resolve merge conflicts with develop" แล้ว Push

หลัง Merge รัน Full Regression Suite ครอบคลุมเคสเดิมทั้งหมด การันตี Zero Regression Defect — ผลตามบทเรียน `4 passed in 0.12s (100%)` สาย develop พร้อมต่อเติมฟีเจอร์ใหม่

## 5. เปิด Sprint 2 ด้วย CR-01 แบบ TDR (Open Sprint 2)

CR-01 (Perfective Maintenance จาก Impact Analysis สัปดาห์ที่ 8): Barcode (String รองรับสแกนเนอร์) + Reorder Point (Integer เกณฑ์ขั้นต่ำ) + แจ้งเตือนเมื่อ `quantity <= reorder_point` — ขยาย Product (`barcode=""`, `reorder_point=5`, เมธอด `is_low_stock() -> bool`) และ InventoryService (`get_low_stock_alerts() -> list[Product]` ผ่าน `load_all()` + วนตรวจ `is_low_stock()` ตรรกะอยู่ใน Service 100% ไม่ปน `print()` ใน ConsoleUI)

วงจร Test-Driven Refinement (TDR): 1) RED  เขียน PyTest ล็อกตรรกะ CR-01 แล้วรันต้อง Fail เพราะยังไม่มีเมธอดจริง 2) GREEN  เขียนโค้ดสั้นที่สุดใน Product & Service ให้ผ่านไฟเขียว 3) REFACTOR  จัดโค้ดให้สะอาดโดย PyTest ยังเขียวสม่ำเสมอ (เขียน Test ก่อนช่วยเข้าใจ CR-01 และกันโค้ดส่วนเกิน)

Edge Cases ตามบทเรียน: TC-CR01-01 quantity 3 < reorder 5 → True  (Alert), TC-CR01-02 quantity 5 == 5 (Boundary) → True  (Alert), TC-CR01-03 quantity 6 > 5 → False  (Normal)

ขั้นตอน: แตก Branch `feature/cr01-barcode-reorder-point` จาก develop → เขียนเทสบาร์โค้ด/Reorder Point ใน test_app.py รันให้ RED → เติม Attributes/เมธอดให้ GREEN → รัน Full Suite `pytest -v` ให้เขียว 100% → Push → ส่งลิงก์ PR ให้ PM ผูก Jira Issue Key และส่ง Man-Hours จริงให้ PM กด Log Work คิด CV

เปิด Sprint บน Jira: ดึงการ์ดบาร์โค้ด + Reorder Point เข้ากล่อง Sprint 2 โดยคุมไม่เกิน Velocity 15 Points → กด "Start Sprint 2" → อัปเดต Procurement Log

## 6. บันทึก Procurement Log (SLA & Quota)

| Tool / Service | Quota Usage Status | Cost Status |
|---|---|---|
| GitHub Actions | 120 / 2,000 Compute Minutes Spent | Free Quota (0 THB) |
| Jira Software | 5 / 10 Active Seats Used | Free Tier (0 THB) |
| Cloud Database | 450 / 500 THB Budget Spent | Under Budget (+50 THB ) |

เป้าหมายคุม SLA: คุมค่าบริการเครื่องมือไม่ให้บานปลาย ติดตามผู้ให้บริการตาม Service Level Agreement (GitHub Actions ตรวจโควต้านาที CI/CD, Jira คุมไม่เกิน Free Tier และ % Uptime คลาวด์)

## 7. เช็กลิสต์ส่งมอบสัปดาห์ที่ 9

1. ภาพประวัติ Commit & Network Graph แสดง Merge งาน Sprint 1 เข้า develop
2. ซอร์สโค้ด + PyTest ครอบคลุม CR-01 บน Feature Branch
3. รายงาน Retrospective Sprint 1 (บอร์ด Mad/Sad/Glad)
4. ตาราง EVM (SV, CV) + ภาพ Active Sprint 2 บน Jira
