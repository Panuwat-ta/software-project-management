# SPM-32 — D. Desktop Hardening + Release Candidate

- Jira: `SPM-32` (5 SP) → Done
- งาน: hardening, tests, lint, security และคู่มือรัน Desktop Program

## เกณฑ์ยอมรับ → หลักฐาน

1. `python3 program.py` เปิดหน้าต่าง GTK4 จริงบน GNOME/Wayland
2. `test_app.py` 14 + `test_program.py` 7 = 21 passed
3. regression v2.0 = 25 passed
4. `flake8 app.py program.py test_program.py tools/build_reports.py` = 0
5. `bandit -q -r app.py program.py` = 0
6. UI ใช้ SQLite / Repository / Strategy / CheckoutService ชุดเดิม
7. มี `program-plan.md` และคำสั่งรันใน README

## UX/UI hardening รอบล่าสุด

- ปรับ navigation sidebar และ active state ให้เห็นหน้าปัจจุบันชัดเจน
- เพิ่ม inline status banner สำหรับ feedback สำเร็จ/ผิดพลาด
- เพิ่ม empty state และจำนวนรายการใน Products/Members
- เพิ่ม LOW/OK badge และจัด visual hierarchy ของตารางใหม่
- เพิ่ม confirmation ก่อนลบข้อมูล
- ปรับ form state สำหรับ add/edit และ helper text
- ปรับ Checkout เป็นสองส่วน: ข้อมูลการขาย + ใบเสร็จ และเน้น grand total
- โปรแกรมเปิดจริงบน GNOME/Wayland หลังแก้ UX/UI โดยไม่มี runtime error
- เพิ่ม Responsive breakpoints: Desktop ≥980 px, Compact 760–979 px, Narrow <760 px
- Sidebar เมนูหลักถูกจำกัดให้กว้างประมาณ 1/3 ของหน้าต่างจริง โดยตั้ง `hexpand=False`; Compact/Narrow จะปรับจำนวนคอลัมน์ของ form/cards และเรียง Checkout แนวตั้ง
- Products/Members table เลื่อนได้ในแนวนอนเมื่อหน้าต่างแคบ

## ข้อกำหนด runtime

Fedora:

```bash
sudo dnf install python3-gobject gtk4
python3 program.py
```

## หมายเหตุ

- สถานะ Jira เดิมคงเป็น Done
- ไม่สร้าง/แก้ Git tag ในรอบนี้ เพราะ working tree ยังมีการเปลี่ยนแปลงที่ยังไม่ได้ commit
- Web implementation เดิมถูกเก็บเป็น historical evidence เท่านั้น
