# SPM-29 — A. Foundation: GTK4 Desktop scaffold + reuse domain

- Jira: `SPM-29` (8 SP) → Done
- งาน: สร้าง `program.py` เป็น GTK4 Desktop UI และ reuse domain จาก `app.py`

## เกณฑ์ยอมรับ → หลักฐาน

1. รัน `python3 program.py` แล้วเปิดหน้าต่างโปรแกรมได้จริงบน GNOME/Wayland
2. UI ต่อกับ `InventoryRepository`, `MemberManager`, `CheckoutService` เดิม
3. ไม่มี SQL หรือ business rule ซ้ำใน UI
4. `test_app.py` เดิมยังผ่าน และเพิ่ม `test_program.py`
5. `flake8` และ `bandit` ผ่าน 0 ปัญหา

## โค้ด

- `program.py` — GTK4 application shell, navigation และ domain bridge
- `test_program.py` — integration tests ของ Desktop Program
- `app.py` — business logic / SQLite / Strategy / Repository

> Web implementation เดิมใน `web/` ถูกแทนที่เป็นตัวส่งมอบหลัก แต่เก็บไว้เป็นหลักฐานย้อนหลัง
