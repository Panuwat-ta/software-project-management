# รายงานปิด Sprint 5 — Phase 5 Evolution (v3.0 + Web)

Sprint 5 (Jira ID 86) งานวิวัฒนาการ รวม 46 story points
สถานะ Done ทั้ง 9 ใบ ข้อมูลสมมติเพื่อการเรียน

## งาน (SPM-23…SPM-27 + SPM-29…SPM-32)

| Issue | งาน | SP |
|---|---|---:|
| SPM-23 | SQLite Singleton + Repository (parameterized 100%) | 5 |
| SPM-24 | Migrate JSON → SQLite ตรวจตรง 100% | 3 |
| SPM-25 | Member CRUD 4 tiers + fallback Regular | 3 |
| SPM-26 | Checkout + ใบเสร็จ (Gold 1,000 → 900) | 3 |
| SPM-27 | 9 เทสต์ใหม่ (รวม 14, injection, legacy) | 3 |
| SPM-29 | Foundation: FastAPI reuse domain + 6 API tests | 8 |
| SPM-30 | Products + Dashboard API + UI | 8 |
| SPM-31 | Members + Checkout API + UI | 8 |
| SPM-32 | Hardening: QA 3 ขนาด, thread bug, docs | 5 |

## สิ่งส่งมอบ

- รายละเอียดส่วน v3.0: `sprint2.md` (+ PDF), `sprint2-report.html`,
  `SPM-23…SPM-27-*.md`, `app.py` + `test_app.py` (snapshot v3.0)
- รายละเอียดส่วน Web: `sprint3.md`, `sprint3-report.html`, `web-plan.md`,
  `SPM-29…SPM-32-*.md`, `web/` (backend + frontend)
- รันเว็บ (จากรากรีโป): `PYTHONPATH=Phase5/Sprint5 uvicorn web.backend.main:app`

## หลักฐานทดสอบรวม

- `test_app.py` + `web/backend/test_web_api.py`: 20 passed
- regression `Phase4/Sprint4/week-12/test_app.py`: 25 passed
- `flake8` clean, `bandit` 0 issues, QA screenshot 360/768/1280

## หมายเหตุชื่อไฟล์

`sprint2.*` = รายละเอียดส่วน v3.0 และ `sprint3.*` = รายละเอียดส่วน Web
ของ Sprint 5 นี้ (ชื่อเดิมก่อนจัด Sprint ใหม่แบบ 1:1)
