# SPM-30 — B. Products + Dashboard API + UI

- Jira: `SPM-30` (8 SP) → Done
- งาน: API สินค้า/summary/CSV + UI หน้า dashboard/products

## เกณฑ์ยอมรับ → หลักฐาน

1. API ครบ → CRUD + `PUT` แก้ไข + `POST /cut` (404/409 ถูกต้อง) +
   `GET /summary` + `GET /export.csv` (หัวตรง CLI); curl ตรวจแล้ว
2. UI ใช้ได้ → dashboard (การ์ดยอด + ตาราง low-stock), หน้า products
   (ค้นหา, badge LOW/OK, เพิ่ม-แก้ไขผ่านฟอร์ม, ตัดสต็อก, ลบ, โหลด CSV)
3. JS ตรวจ syntax ผ่าน (`node --check`)

## โค้ด

- `web/frontend/`: `index.html` (SPA shell), `styles.css` (responsive),
  `app.js` (hash router + fetch render, ไม่มี dependency)
