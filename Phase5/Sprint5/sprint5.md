# รายงานปิด Sprint 5 — Phase 5: วิวัฒนาการ v3.0 และเว็บแอป v4.0

เอกสารนี้สรุปหลักฐานสปรินต์ที่ห้า ซึ่งเป็นการนำแบบออกแบบที่ค้างไว้ตั้งแต่ Sprint 1
มาพัฒนาเป็นโค้ดจริงสองส่วน: ฐานข้อมูล SQLite กับระบบสมาชิก/ส่วนลด (v3.0)
และเว็บแอป responsive ที่ reuse ตรรกะเดิมทั้งหมด (v4.0-web)
ข้อมูลโครงการทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. ข้อมูลสปรินต์

| รายการ | ค่า |
|---|---|
| Sprint | Sprint 5 - Phase 5 (v3+Web) |
| Jira Sprint ID | 86 (state: closed) |
| Story Points | 46 SP (SPM-23…SPM-27 + SPM-29…SPM-32) ปิดครบทุกใบ |
| Epics | SPM-22 (SQLite + Member), SPM-28 (WEB) |
| หลักฐานราย issue | `SPM-23-sqlite-layer.md` … `SPM-32-hardening.md` |
| รุ่นที่ส่งมอบ | tag `v3.0.0`, `v4.0.0-web`, `v4.0.1` |

เป้าหมาย: ยกระดับจาก CLI เป็นเว็บที่ใช้งานได้ทั้งคอมพิวเตอร์และมือถือ
โดยไม่ทิ้งฟีเจอร์เดิมและไม่ให้ regression

## 2. ทีมและบทบาท

| บุคคล | บทบาท | ความรับผิดชอบในสปรินต์นี้ |
|---|---|---|
| ภานุวัฒน์ ต๋าคำ | PM / Developer | API, หน้าเว็บ, migration, checkout flow |
| เอกพันธ์ ทศทิศรังสรรค์ | QA / Tester | เทสต์ชั้น DB/ส่วนลด, เทสต์ injection, QA ขนาดจอ |
| ณฐภาพ สายหล้า | Tech Lead / Architect | ตัดสินใจ reuse domain, ตรวจสถาปัตยกรรมและ lint |

## 3. งานตามแผนและหลักฐาน

### ส่วน A — v3.0: SQLite + Member + Checkout (17 SP)

| Issue | งาน | SP | หลักฐาน |
|---|---|---:|---|
| SPM-23 | SQLite Database Layer (Singleton + Parameterized) | 5 | `SPM-23-sqlite-layer.md` |
| SPM-24 | Migrate JSON Data to SQLite with Verification | 3 | `SPM-24-migration.md` |
| SPM-25 | Member CRUD Module with 4 Tiers | 3 | `SPM-25-member-crud.md` |
| SPM-26 | Integrate Member Discount into Checkout Flow | 3 | `SPM-26-checkout.md` |
| SPM-27 | Automated Tests for DB Layer and Discount Engine | 3 | `SPM-27-tests.md` |

### ส่วน B — v4.0-web: เว็บแอป (29 SP)

| Issue | งาน | SP | หลักฐาน |
|---|---|---:|---|
| SPM-29 | Foundation: scaffold + FastAPI reuse domain | 8 | `SPM-29-foundation.md` |
| SPM-30 | Products + Dashboard API + UI | 8 | `SPM-30-products.md` |
| SPM-31 | Members + Checkout API + UI | 8 | `SPM-31-checkout.md` |
| SPM-32 | Hardening + Release | 5 | `SPM-32-hardening.md` |

แผนงานละเอียดของส่วน B: `web-plan.md`

## 4. ส่วน A: สถาปัตยกรรม v3.0

| แนวทาง | การถือปฏิบัติ | รายละเอียด |
|---|---|---|
| Singleton | `SQLiteDatabaseContext` | จุดเชื่อมต่อฐานข้อมูลจุดเดียว ป้องกัน Database Locked มี `commit`/`rollback`/`reset` |
| Repository | `InventoryRepository` | ซ่อน SQL ไว้ชั้นเดียว: save/find_by_id/find_all/update_stock/delete + summary |
| Strategy | `MemberTier` + 4 คลาส | Regular 0% · Silver 5% · Gold 10% · Platinum 15% เพิ่มระดับใหม่ไม่ต้องแก้ if-else |
| Transaction | commit/rollback ทุก write | ข้อมูลไม่ค้างกลางคันเมื่อเกิดข้อผิดพลาด |

ตารางฐานข้อมูล:
- `products` — product_id (PK), name, quantity, price, category, barcode, reorder_point พร้อม `CHECK (>= 0)`
- `members` — member_id (PK), name, tier, discount_rate

## 5. ส่วน A: การย้ายข้อมูลและผลตรวจสอบ

| รายการ | ผล |
|---|---|
| ฟังก์ชัน | `migrate_json_to_sqlite()` อ่านผ่าน `Product.from_dict` จึงรองรับคีย์เก่า `n`/`q`/`p`/`c` |
| ค่า default ของฟิลด์ใหม่ | `barcode=""`, `reorder_point=5` (ต่อเนื่องจาก BUG-101) |
| การตรวจสอบ | เทียบจำนวนระเบียนและมูลค่ารวมก่อน/หลังย้าย ต้องตรงกัน 100% (`match: True`) |
| ตัวอย่างผลตรวจ | JSON 2 ระเบียน (ผสมคีย์เก่า/ใหม่) มูลค่า 600.0 → SQLite 600.0 |
| การใช้งานจริง | เปิดโปรแกรมครั้งแรกจะย้าย `data.json` อัตโนมัติเมื่อฐานข้อมูลยังว่าง |

## 6. ส่วน A: ระบบสมาชิกและส่วนลด

| Tier | อัตราส่วนลด | ตัวอย่างซื้อ 1,000 บาท |
|---|---:|---:|
| Regular | 0% | 1,000.00 |
| Silver | 5% | 950.00 |
| Gold | 10% | 900.00 |
| Platinum | 15% | 850.00 |

- ชื่อ tier ผิด/ว่าง/ไม่ใช่ string → `normalize_tier` คืน `Regular` โดยไม่ error
- ไม่กรอกรหัสสมาชิก หรือรหัสไม่มีในระบบ → คิดราคาเต็ม (Graceful Guest-Only)
- ใบเสร็จแยกบรรทัด: subtotal, tier + อัตรา, discount_value, grand_total, สต็อกคงเหลือ, ธง low stock

## 7. ส่วน B: เว็บแอป

| หัวข้อ | รายละเอียด |
|---|---|
| Backend | FastAPI + Uvicorn, รวม router 3 ตัว, เสิร์ฟ frontend แบบ static |
| Frontend | SPA 4 หน้า (แดชบอร์ด/สินค้า/สมาชิก/ขาย) + HTML/CSS/JS ล้วน ไม่มี build step |
| Responsive | ทดสอบ 360 / 768 / 1280 px: มือถือใช้ hamburger, การ์ดคอลัมน์เดียว, ตารางเลื่อนแนวนอน |
| API | `/api/products` CRUD + cut · `/api/summary` · `/api/export.csv` · `/api/members` CRUD + tiers · `/api/checkout` |
| การจัดการ error | 404 ไม่พบข้อมูล · 409 สต็อกไม่พอ · 422 ข้อมูลผิดประเภทจาก Pydantic |
| เอกสาร API | เปิด `/docs` ได้อัตโนมัติจาก FastAPI |

วิธีรัน (จากรากรีโป):

```bash
PYTHONPATH=Phase5/Sprint5 uvicorn web.backend.main:app --reload
```

## 8. ส่วน A: การรักษาความเข้ากันได้

| หลักการ | ผลลัพธ์ |
|---|---|
| ไม่แก้โครงสร้างโดเมนเดิม | ชั้น API เป็น wrapper บาง ๆ ทับของเดิม |
| CLI ยังทำงาน | `app.py` ยังรันเมนูเดิมครบ (เพิ่มเมนูสมาชิก/ขาย) |
| ฟีเจอร์เดิมไม่หาย | barcode, reorder point, `is_low_stock`, CSV, atomic save |
| regression รุ่นเก่า | `Phase4/Sprint4/week-12/test_app.py` ผ่าน 25 เคสไม่แตก |

## 9. หลักฐานทดสอบรวม

| ชุด | ผล | ครอบคลุม |
|---|---|---|
| `test_app.py` (CLI) | 14 passed | 5 เดิม + 9 ใหม่ (singleton, injection, migration, CRUD 4 tiers, fallback, checkout ×3, legacy) |
| `web/backend/test_web_api.py` | 6 passed | health, seed, CRUD+validation, summary+CSV, member/checkout, injection |
| **รวมชุดหลัก** | **20 passed** | — |
| regression รุ่น v2.0 | 25 passed | ยืนยันว่าไม่มีการถดถอย |

## 10. คุณภาพโค้ดและความปลอดภัย

| รายการ | ผล |
|---|---|
| flake8 (โค้ดสด + backend เว็บ + tools) | 0 ปัญหา |
| E501 (บรรทัดยาวเกิน 79) ในโค้ดสด | 0 |
| E501 ในไฟล์ snapshot ประวัติการทำงาน | 112 จุด (Phase1/Sprint1 86, Phase4/Sprint4 26) เก็บเป็นหลักฐาน ไม่ได้แก้ |
| bandit | 0 ปัญหา |
| SQL injection | input `' OR '1'='1` และ `"; DROP TABLE --` ถูกปฏิบัติเป็น string ธรรมดา ตารางไม่เสียหาย |
| การจับ exception | เจาะจงชนิด ไม่กลืน error |

## 11. บั๊กที่พบระหว่าง QA และการแก้ไข

| อาการ | รากเหง้า | การแก้ |
|---|---|---|
| `sqlite3.ProgrammingError` เมื่อรันบน uvicorn | FastAPI ทำงานหลาย thread แต่ connection เดียวถูกสร้างใน thread หนึ่ง | เปิด `check_same_thread=False` ใน `SQLiteDatabaseContext` แล้วรันสอบครบทั้งชุด |
| 404 noise จาก favicon | หน้าเว็บไม่มีไฟล์ favicon | ใส่ favicon แบบ inline ใน HTML |

## 12. ความเสี่ยงและข้อจำกัดที่เหลือ

| รายการ | สถานะ |
|---|---|
| ระบบล็อกอิน/สิทธิ์ผู้ใช้ | ไม่ทำ (อยู่นอกขอบเขตที่ตกลงไว้) |
| ระบบชำระเงินออนไลน์ | ไม่ทำ |
| SQLite แบบ single-user | รองรับผู้ใช้คนเดียว หลายคนพร้อมกันต้องย้าย PostgreSQL ผ่าน Repository |
| ช่องลายเซ็น UAT | ยังรอผู้รับรองลงนาม (จาก Sprint 4) |
| ข้อมูลผู้ใช้ตัวอย่าง | เป็นข้อมูลสมมติเพื่อการเรียน |

## 13. Sprint Review (ตามหลักฐานที่มี)

| หัวข้อ | หลักฐาน | ผล/ข้อสังเกต |
|---|---|---|
| สิ่งที่สาธิต | โค้ด v3.0 + เว็บที่รันได้จริง | สคริปต์เดโม 6 ขั้นตอนใน `web/README.md` |
| ผลที่ผ่าน | 20 + 25 tests, lint สะอาด, QA 3 ขนาดจอ | ยืนยันได้จากคำสั่งที่รันซ้ำได้ |
| ผู้เข้าร่วมเดโม/ผู้รับรอง | ไม่มีหลักฐานลงชื่อ | ไม่อ้างว่าได้รับการรับรอง |

## 14. งานที่ยกยอดไป

- เพิ่มระดับสมาชิกใหม่ (เช่น Diamond) โดยเพิ่มคลาสในกลุ่ม Strategy
- ย้ายไป REST/Web API ของฝ่ายขายเกินหนึ่งร้าน (ยังใช้ Repository เดิม)
- ปิดช่องลายเซ็น UAT และจัดทำคู่มือผู้ใช้ฉบับเต็ม

## 15. ภาคผนวก Evidence Index

| หมวดหลักฐาน | เส้นทาง |
|---|---|
| หลักฐานราย issue | `SPM-23-sqlite-layer.md`, `SPM-24-migration.md`, `SPM-25-member-crud.md`, `SPM-26-checkout.md`, `SPM-27-tests.md` |
| หลักฐานราย story เว็บ | `SPM-29-foundation.md`, `SPM-30-products.md`, `SPM-31-checkout.md`, `SPM-32-hardening.md` |
| รายละเอียดส่วน v3.0 | `sprint2.md` (+ `sprint2.pdf`, `sprint2-report.html`) |
| รายละเอียดส่วนเว็บ | `sprint3.md`, `sprint3-report.html`, `web-plan.md` |
| โค้ด | `app.py`, `test_app.py`, `web/backend/`, `web/frontend/` |
| ชุดทดสอบ | `test_app.py`, `web/backend/test_web_api.py` |
| รุ่นที่ส่งมอบ | tag `v3.0.0`, `v4.0.0-web`, `v4.0.1` |