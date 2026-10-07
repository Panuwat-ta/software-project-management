# Phase 5 — วิวัฒนาการ v3.0 + Desktop Program (Sprint 5)

ข้อมูลทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

- ขอบเขต: SQLite/Member/Checkout 17 SP + Desktop Program UI 29 SP (รวม 46 SP)
- Sprint หลัก: Sprint 5 (Jira ID 86)
- ส่วน A: `sprint2.md` — v3.0 SQLite + Member + Checkout
- ส่วน B: `sprint3.md` — Desktop Program UI (GTK4) ที่รันด้วย `python3 program.py`
- โค้ดหลัก: `app.py`, `program.py`, `test_app.py`, `test_program.py`
- แผน Desktop UI: `program-plan.md`
- โฟลเดอร์ `web/` และ `web-plan.md` เก็บไว้เป็นหลักฐาน implementation เดิมที่ถูกแทนที่ ไม่ใช่ตัวส่งมอบหลักปัจจุบัน

รันโปรแกรมจากรากรีโป:

```bash
python3 program.py
```

บน Fedora ต้องมี GTK4/PyGObject:

```bash
sudo dnf install python3-gobject gtk4
```
