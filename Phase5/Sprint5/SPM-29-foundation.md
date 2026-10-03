# SPM-29 — A. Foundation: web scaffold + FastAPI reuse domain

- Jira: `SPM-29` (8 SP) → Done
- งาน: โครง `web/backend` + `web/frontend`, FastAPI reuse `app.py` v3.0,
  `/health` + `/docs`, สคริปต์รัน, API tests แรก

## เกณฑ์ยอมรับ → หลักฐาน

1. โครง web รันได้ reuse domain ไม่แตะ CLI → `deps.py` ต่อ
   `Product`/`MemberTier`/`CheckoutService`/`Repository` เดิม;
   `test_app.py` 14 เคสยังเขียว (CLI ไม่พัง)
2. API tests แรกเขียว → `test_web_api.py` 6 เคส
   (health, seed, CRUD+validation, summary+CSV, member+checkout Gold,
   injection) ผ่าน
3. คุณภาพ → `flake8` clean, `bandit` 0 issues

## โค้ด

- `web/backend/main.py` (app + `/api/health|summary|export.csv` +
  serve frontend), `deps.py` (lazy DB + migrate/seed แบบ CLI),
  `api_products.py`, `api_members.py`, `api_checkout.py`
- smoke: `uvicorn` จริง health/summary/frontend/checkout 200 ทั้งหมด
