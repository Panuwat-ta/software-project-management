# SPM-32 — D. Hardening + Release

- Jira: `SPM-32` (5 SP) → Done
- งาน: QA 3 ขนาดจอ, E2E smoke, lint, docs, เตรียม tag `v4.0.0-web`

## เกณฑ์ยอมรับ → หลักฐาน

1. 3 ขนาดจอ (360/768/1280) ใช้งานได้ทุกปุ่ม → screenshot จริงตรวจแล้ว:
   มือถือใช้ hamburger + การ์ดคอลัมน์เดียว + ตาราง scroll;
   จอใหญ่ nav เต็ม + การ์ด 3 คอลัมน์
2. เจอบั๊กจริงตอน QA: SQLite thread error ใต้ uvicorn →
   แก้ `check_same_thread=False` ใน `SQLiteDatabaseContext`
   (เทสต์ 20 ยังเขียว, sync snapshot Phase2 แล้ว)
3. คุณภาพ → `flake8` clean, `bandit` 0 issues (ไม่นับ assert ในไฟล์เทสต์),
   `node --check` ผ่าน
4. Docs → `web/README.md` (วิธีรัน + API ย่อ + เดโม 2 นาที),
   `web-plan.md`; E2E ผ่านทั้ง CLI (14) + API (6) + regression (25)
5. Tag `v4.0.0-web` รอ commit ก่อนสร้าง (ยังไม่สร้าง tag ลอย)

## หมายเหตุ

- favicon ใส่แบบ inline กัน 404 noise
- `.gitignore` เพิ่ม `inventory.db` (ไฟล์รันไทม์)
