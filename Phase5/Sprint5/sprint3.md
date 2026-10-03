# รายงาน Sprint 5 · ส่วน Web — จาก CLI สู่ Web App (v4.0-web)

เอกสารนี้สรุปหลักฐานส่วน Web ในโฟลเดอร์ `Phase5/Sprint5/` สำหรับงานรายวิชา
ข้อมูลโครงการทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. วัตถุประสงค์และขอบเขต (ส่วน Web ของ Sprint 5)

เปลี่ยนระบบคลังสินค้า CLI เป็นเว็บสวยงามทันสมัย ใช้ได้ทั้งคอมพิวเตอร์
และมือถือ โดย Backend Python (FastAPI) reuse ตรรกะ `app.py` v3.0 ทั้งก้อน
และ Frontend HTML/CSS/JavaScript ล้วน ไม่ทำระบบล็อกอิน/จ่ายเงิน
(Epic WEB: SPM-28, 29 SP)

## 2. ทีมและบทบาท

| บุคคล | บทบาท | ความรับผิดชอบหลัก |
|---|---|---|
| Panuwat | PM / Developer | บริหารงานและพัฒนา |
| Ekkapan | QA / Tester | ออกแบบและทดสอบอัตโนมัติ |
| Nattapap | Tech Lead / Architect | ออกแบบสถาปัตยกรรมและทบทวนโค้ด |

## 3. งานตามแผน SPM-29…SPM-32

| Issue | งาน | SP | หลักฐาน |
|---|---|---:|---|
| SPM-29 | A. Foundation: scaffold + FastAPI reuse domain + tests | 8 | `SPM-29-foundation.md`, `web/backend/`, 6 API tests |
| SPM-30 | B. Products + Dashboard API + UI | 8 | `SPM-30-products.md`, หน้า dashboard/products |
| SPM-31 | C. Members + Checkout API + UI | 8 | `SPM-31-checkout.md`, หน้า members/checkout + ใบเสร็จ |
| SPM-32 | D. Hardening + Release | 5 | `SPM-32-hardening.md`, QA 3 ขนาด + lint + docs |

## 4. สิ่งที่ส่งมอบ

| สถานะ | รายการ | หลักฐาน/ข้อกำหนด |
|---|---|---|
| Delivered | REST API 9 กลุ่ม | products CRUD/cut, summary, export.csv, members CRUD/tiers, checkout (404/409/400 ถูกต้อง) |
| Delivered | SPA 4 หน้า responsive | dashboard, products (ค้นหา/แก้ไข/ตัด/ลบ/CSV), members, checkout + ใบเสร็จ; 360/768/1280 ตรวจด้วย screenshot จริง |
| Delivered | Reuse ไม่พังของเดิม | CLI + `test_app.py` 14 เคสยังเขียว; regression week-12 25 passed |
| Delivered | คุณภาพ | `flake8` clean, `bandit` 0 issues, `node --check` ผ่าน |
| Delivered | เอกสาร | `web-plan.md`, `web/README.md` (วิธีรัน + เดโม 2 นาที), รายงานฉบับนี้ + `sprint-report.html` |
| ส่งมอบแล้ว | tag `v4.0.0-web` + `v4.0.1` | สร้าง annotated tag และ push ขึ้น remote แล้ว |

รันเว็บ (จากรากรีโป): `PYTHONPATH=Phase5/Sprint5 uvicorn web.backend.main:app`
แล้วเปิด http://127.0.0.1:8000/ (API docs ที่ `/docs`)

## 5. หลักฐานทดสอบ

| ชุดทดสอบ | ผล | ขอบเขต |
|---|---|---|
| `test_app.py` + `web/backend/test_web_api.py` | 20 passed | 14 CLI + 6 API (health/seed/CRUD/validation/summary/CSV/member/checkout/injection) |
| `Phase4/Sprint4/week-12/test_app.py` | 25 passed | regression v2.0 ไม่แตก |

- E2E บน server จริง: เพิ่มสินค้า → สมัคร Gold → checkout 1,000 → 900 →
  โหลด CSV; ตัดเกินสต็อก/ราคาติดลบได้ error สวย
- QA เจอบั๊กจริง: SQLite thread error ใต้ uvicorn → แก้ด้วย
  `check_same_thread=False` (เทสต์ยังเขียวทั้งหมด)

## 6. Jira และการติดตาม

- Epic SPM-28 + stories SPM-29…SPM-32 (29 SP) Done ทั้งหมด
  อยู่ใน Sprint 5 (ID 86) ซึ่งปิดแล้ว

## 7. ภาคผนวก Evidence Index

| หมวดหลักฐาน | เส้นทาง |
|---|---|
| แผนงาน | `Phase5/Sprint5/web-plan.md` |
| โค้ดเว็บ | `Phase5/Sprint5/web/backend/`, `Phase5/Sprint5/web/frontend/` |
| ชุดทดสอบ API | `Phase5/Sprint5/web/backend/test_web_api.py` |
| หลักฐานราย story | `Phase5/Sprint5/SPM-29-foundation.md` … `SPM-32-hardening.md` |
| รายงานฉบับเว็บ | `Phase5/Sprint5/sprint3-report.html` |
| Domain ที่ reuse | `app.py`, `test_app.py` (รากรีโป) |
