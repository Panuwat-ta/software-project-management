# SPM-31 — C. Members + Checkout API + UI

- Jira: `SPM-31` (8 SP) → Done
- งาน: API สมาชิก/checkout + UI หน้า members/checkout + ใบเสร็จ

## เกณฑ์ยอมรับ → หลักฐาน

1. สมาชิกครบ → CRUD + `GET /tiers` (4 tiers + อัตรา), tier ผิด fallback
   Regular; curl ตรวจแล้ว
2. Checkout บนเว็บ → สมัคร Gold + ซื้อ 2×500 = 1,000 → ใบเสร็จสุทธิ 900;
   guest ราคาเต็ม; ของไม่พอ 409; UI มีปุ่มแก้ไขสมาชิก + แสดงใบเสร็จ/
   error สวยงาม

## โค้ด

- `web/backend/api_members.py`, `api_checkout.py` (404/409/400 ถูกต้อง),
  หน้า members/checkout ใน `app.js` (receipt render + error box)
