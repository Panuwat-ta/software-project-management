# รายงาน Sprint 5 · ส่วน v3.0 — SQLite + Member System

เอกสารนี้สรุปหลักฐานในโฟลเดอร์ `Phase5/` สำหรับงานรายวิชา
ข้อมูลโครงการทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. วัตถุประสงค์และขอบเขต Sprint 2

เป้าหมายจาก epic SPM-22 คือลงมือทำ scope ที่ยกยอดจาก Sprint 1 ซึ่งตอนนั้น
เป็นเพียงแบบออกแบบ (`Phase1/Sprint1/week-2/blueprint.md`, `Phase1/Sprint1/week-2/Member-Discount.md`,
`Phase2/Sprint2/week-6/To_Be_Architecture.md`): ชั้นฐานข้อมูล SQLite แบบ Singleton ที่ใช้
parameterized query, สคริปต์ย้าย `data.json` พร้อมยืนยัน, ระบบสมาชิก CRUD
4 tiers ด้วย Strategy pattern, ผูกส่วนลดเข้า Checkout Flow พร้อมใบเสร็จ
และชุดทดสอบอัตโนมัติครอบชั้น DB + เครื่องคำนวณส่วนลด + กัน SQL injection

ข้อมูลการติดตามจาก Jira: งานชุดนี้อยู่ใน Sprint 5 (ID 86)
5 issues (SPM-23…SPM-27, รวม 17 SP) สถานะ Done ทั้งหมด

## 2. ทีมและบทบาท

| บุคคล | บทบาท | ความรับผิดชอบหลัก |
|---|---|---|
| Panuwat | PM / Developer | บริหารงานและพัฒนา |
| Ekkapan | QA / Tester | ออกแบบและทดสอบอัตโนมัติ |
| Nattapap | Tech Lead / Architect | ออกแบบสถาปัตยกรรมและทบทวนโค้ด |

## 3. งานตามแผน SPM-23…SPM-27

| Issue | งาน | SP | หลักฐาน |
|---|---|---:|---|
| SPM-23 | SQLite Database Layer (Singleton + Parameterized) | 5 | `SPM-23-sqlite-layer.md`, `app.py` (`SQLiteDatabaseContext`, `InventoryRepository`) |
| SPM-24 | Migrate JSON → SQLite พร้อมยืนยัน | 3 | `SPM-24-migration.md`, `app.py` (`migrate_json_to_sqlite`, auto-migrate ใน CLI) |
| SPM-25 | Member CRUD 4 tiers | 3 | `SPM-25-member-crud.md`, `app.py` (`MemberTier` 4 คลาส, `Member`, `MemberManager`) |
| SPM-26 | ส่วนลดเข้า Checkout Flow | 3 | `SPM-26-checkout.md`, `app.py` (`CheckoutService`, เมนู CLI 7) |
| SPM-27 | Tests ชั้น DB + Discount + Injection | 3 | `SPM-27-tests.md`, `test_app.py` (9 เคสใหม่) |

## 4. สิ่งที่ส่งมอบ

| สถานะ | รายการ | หลักฐาน/ข้อกำหนด |
|---|---|---|
| Delivered | Singleton + Repository (parameterized 100%) | `SQLiteDatabaseContext.getInstance`/`reset`; SQL ทุกเส้นใช้ `?` placeholders; `bandit` 0 issues |
| Delivered | Migration + verification | `match: True` (จำนวน + มูลค่าตรง 100%); รองรับคีย์เก่า `n`/`q`/`p`/`c` และค่าเริ่มต้น `barcode`/`reorder_point` ต่อเนื่องจาก BUG-101 |
| Delivered | Member 4 tiers + fallback | Regular 0% / Silver 5% / Gold 10% / Platinum 15%; tier ผิด/ว่าง → Regular โดยไม่ error |
| Delivered | Checkout + ใบเสร็จ | `subtotal`/`discount`/`grand_total` แยกบรรทัด; Gold 1,000 → 900; guest ราคาเต็ม; ตัดสต็อกใน transaction เดียว (commit/rollback); alert `<= reorder_point` ยังทำงาน |
| Delivered | ความเข้ากันได้ถอยหลัง | `InventoryManager` (JSON + Atomic Save), `Product`, `CsvReportExporter` จาก v2.0 อยู่ครบ; CLI 5 → 8 เมนู |
| Delivered | หนี้ Sprint 1 บางส่วน | Flake8 `E501` ใน `app.py`/`test_app.py` เคลียร์หมด (`flake8 app.py` exit 0) |

## 5. หลักฐานทดสอบ

| ชุดทดสอบ | ผล | ขอบเขต |
|---|---|---|
| `test_app.py` ที่รากรีโป | 14 passed | 5 เดิม (JSON) + 9 ใหม่ (singleton, injection, migration, member CRUD, fallback, checkout Gold/guest/alert, legacy JSON) |
| `Phase4/Sprint4/week-12/test_app.py` | 25 passed | regression v2.0 ไม่แตก |

- Injection: `' OR '1'='1` และ `"; DROP TABLE --` ถูก treat เป็น string
  ธรรมดา ตารางไม่พัง ยอดเงินเท่าเดิม
- E2E: JSON legacy ผสมคีย์สั้น/ยาว → migrate (`match: True`) →
  สมัคร Gold → checkout 2×500 = 1,000 → สุทธิ 900 เหลือสต็อก 8
- Fixture แยก DB ต่อเทสต์ด้วย `tmp_path` + `SQLiteDatabaseContext.reset()`
  กัน singleton รั่วข้ามเคส

## 6. คุณภาพโค้ดและหนี้คงเหลือ

- `flake8 app.py` → clean (exit 0); `bandit -r app.py` → 0 issues
- หนี้คงเหลือ: `test_app.py` ยังมี style nits เดิม (E302/W293) ไม่กระทบ
  การรัน; งานพิธีการ (UAT sign-off ลายเซ็น, Git tag `v2.0.0-evolution`)
  ยังเป็นของ Sprint 1 ไม่ได้รวมใน Sprint 2 นี้

## 7. Jira และการติดตาม

- งานชุดนี้อยู่ Sprint 5 (ID 86) ร่วมกับงาน Web (SPM-29…32);
  epic SPM-22 ปิดแล้ว

## 8. ภาคผนวก Evidence Index

| หมวดหลักฐาน | เส้นทาง |
|---|---|
| โค้ด v3.0 | `app.py` (รากรีโป) + snapshot `Phase5/Sprint5/app.py` |
| ชุดทดสอบ | `test_app.py` (รากรีโป) + snapshot `Phase5/Sprint5/test_app.py` |
| หลักฐานราย issue | `Phase5/Sprint5/SPM-23-sqlite-layer.md` … `SPM-27-tests.md` |
| รายงานฉบับเว็บ | `Phase5/Sprint5/sprint2-report.html` |
| งานยกยอดต้นทาง | `Phase1/Sprint1/week-2/blueprint.md`, `Phase1/Sprint1/week-2/Member-Discount.md`, `Phase2/Sprint2/week-6/To_Be_Architecture.md` |
| รายงาน Sprint 1 | `Phase4/Sprint4/sprint1.md` |
