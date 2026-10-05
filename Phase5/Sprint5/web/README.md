# [Historical / Superseded] Inventory Web (v4.0-web)

> implementation นี้ถูกแทนที่ด้วย Desktop Program (`program.py`) และเก็บไว้เพื่อ traceability เท่านั้น

เว็บ responsive สำหรับระบบคลังสินค้า: Backend FastAPI reuse ตรรกะ
`app.py` v3.0 ทั้งก้อน (CLI เดิมยังใช้ได้) Frontend HTML/CSS/JS ล้วน

## วิธีรัน (dev, จากรากรีโป)

```bash
pip install -r requirements.txt
PYTHONPATH=Phase5/Sprint5 uvicorn web.backend.main:app --reload
```

- เปิดเว็บ: http://127.0.0.1:8000/
- API docs: http://127.0.0.1:8000/docs
- ฐานข้อมูล: `inventory.db` ที่รากรีโป (สร้าง + seed อัตโนมัติ);
  เปลี่ยนได้ด้วย env `INVENTORY_DB=/path/to/file.db`

## โครง (อยู่ใน `Phase5/Sprint5/web/`)

- `backend/main.py` — app + `/api/health|summary|export.csv` + serve frontend
- `backend/api_products.py`, `api_members.py`, `api_checkout.py`
- `backend/deps.py` — ต่อ domain เดิมแบบ lazy (import แล้วไม่มี side effect)
- `backend/test_web_api.py` — เทสต์ API
  (`pytest Phase5/Sprint5/web/backend/test_web_api.py -q`)
- `frontend/` — SPA 4 หน้า (dashboard/products/members/checkout)

## API ย่อ

`GET/POST /api/products`, `GET/PUT/DELETE /api/products/{id}`,
`POST /api/products/{id}/cut`, `GET /api/summary`, `GET /api/export.csv`,
`GET/POST /api/members`, `GET/DELETE /api/members/{id}`,
`GET /api/members/tiers`, `POST /api/checkout`

## เดโม 2 นาที (หลังรัน server)

1. เปิด `/` → แดชบอร์ดขึ้นยอด 3 ประเภท / 1,540 THB
2. หน้า `สินค้า` → เพิ่ม `G9 Gold Item 10×500` → กด `-1` ตัดสต็อก
3. หน้า `สมาชิก` → สมัคร `VIP1 / Gold`
4. หน้า `ขาย` → `G9 × 2 + VIP1` → ใบเสร็จ Subtotal 1,000 − Gold 100 = **900**
5. ปุ่ม `โหลด CSV` → เปิดใน Excel ได้เลย
6. ลองตัดเกินสต็อก / กรอกราคาติดลบ → error สวย ไม่ล่ม
