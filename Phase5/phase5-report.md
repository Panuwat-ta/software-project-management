# รายงาน Phase 5 — วิวัฒนาการ v3.0 + Web (Sprint 5)

## 1. วัตถุประสงค์

ลงมือทำ scope ที่ยกยอดจาก Phase 4 (SQLite + Member + Checkout) แล้วยกระดับ
CLI เป็นเว็บ responsive โดย reuse ตรรกะเดิมทั้งหมด

## 2. งานส่วน v3.0 (SPM-23…SPM-27, 17 SP)

| Issue | งาน | หลักฐาน |
|---|---|---|
| SPM-23 | SQLite Singleton + Repository (parameterized 100%) | `SPM-23-sqlite-layer.md` |
| SPM-24 | Migrate JSON → SQLite ตรวจตรง 100% | `SPM-24-migration.md` |
| SPM-25 | Member CRUD 4 tiers + fallback Regular | `SPM-25-member-crud.md` |
| SPM-26 | Checkout + ใบเสร็จ (Gold 1,000 → 900) | `SPM-26-checkout.md` |
| SPM-27 | 9 เทสต์ใหม่ (รวม 14, injection, legacy) | `SPM-27-tests.md` |

รายงาน: `sprint2.md` (+ PDF), `sprint2-report.html`; โค้ด `app.py`/`test_app.py`
(snapshot ตรงรากรีโป)

## 3. งานส่วน Web (SPM-29…SPM-32, 29 SP)

| Issue | งาน | หลักฐาน |
|---|---|---|
| SPM-29 | Foundation: FastAPI reuse domain + 6 API tests | `SPM-29-foundation.md` |
| SPM-30 | Products + Dashboard API + UI | `SPM-30-products.md` |
| SPM-31 | Members + Checkout API + UI | `SPM-31-checkout.md` |
| SPM-32 | Hardening: QA 3 ขนาด, แก้ SQLite thread bug, docs | `SPM-32-hardening.md` |

แผน: `web-plan.md`; โค้ด: `web/` (backend + frontend);
รัน: `PYTHONPATH=Phase5/Sprint5 uvicorn web.backend.main:app`;
รายงาน: `sprint3.md`, `sprint3-report.html`

## 4. หลักฐานทดสอบรวม

- `test_app.py` + `web/backend/test_web_api.py`: 20 passed
- regression `Phase4/Sprint4/week-12/test_app.py`: 25 passed
- `flake8` clean, `bandit` 0 issues, QA screenshot 360/768/1280

## 5. สถานะ

Epic SPM-22 + SPM-28 และ stories ทั้ง 9 ใบ Done; คงค้างพิธีการ:
Jira Sprint 5 (ID 86) ปิดแล้ว; tag `v4.0.0-web` รอ commit
