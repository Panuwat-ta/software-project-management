# รายงาน Phase 5 — วิวัฒนาการ v3.0 และ Desktop Program

ข้อมูลทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. ภาพรวมเฟส

| รายการ | ค่า |
|---|---|
| Sprint ที่ครอบคลุม | Sprint 5 (Jira ID 86, closed) |
| Issues | SPM-23…SPM-27 (17 SP) + SPM-29…SPM-32 (29 SP) = **46 SP** |
| Epics | SPM-22 (SQLite + Member), SPM-28 (Desktop Program UI) |
| ตัวส่งมอบหลัก | `app.py` v3.0 + `program.py` Desktop UI |
| สถานะ | งานหลัก Done; release tag ของ Desktop build ยังไม่สร้างในรอบนี้ |

Phase 5 ปิดงานออกแบบที่ค้างจาก Sprint 1 แล้วเพิ่มหน้าตาโปรแกรม Desktop
โดย reuse business logic เดิมและไม่บังคับให้ผู้ใช้เปิด browser หรือรัน server

## 2. ส่วน A — v3.0: SQLite + Member + Checkout

| หัวข้อ | ผลลัพธ์ |
|---|---|
| ฐานข้อมูล | SQLite แบบ Singleton + Repository + parameterized query |
| Transaction | commit/rollback และ schema CHECK กันค่าติดลบ |
| Migration | JSON → SQLite พร้อมตรวจจำนวนและมูลค่า 100% |
| สมาชิก | CRUD + Regular/Silver/Gold/Platinum ด้วย Strategy |
| Checkout | ส่วนลดอัตโนมัติ + ใบเสร็จ + ตัดสต็อก |

## 3. ส่วน B — Desktop Program UI

| หัวข้อ | ผลลัพธ์ |
|---|---|
| Toolkit | GTK4 / PyGObject |
| จุดเริ่ม | `python3 program.py` |
| Dashboard | ประเภทสินค้า มูลค่ารวม และ low-stock |
| Products | เพิ่ม/แก้ไข/ค้นหา/ตัด/ลบ/Export CSV |
| Members | CRUD สมาชิกและ tier |
| Checkout | ส่วนลดสมาชิก + ใบเสร็จบนหน้าจอ |
| Domain reuse | Repository / MemberManager / CheckoutService / CSV จาก `app.py` |

สถาปัตยกรรม:

```text
program.py (GTK4)
      │
      └─ app.py domain
           ├─ InventoryRepository
           ├─ MemberManager
           ├─ CheckoutService
           └─ SQLiteDatabaseContext
                  └─ inventory.db
```

## 4. หลักฐานทดสอบ

| ชุด | ผล |
|---|---|
| `test_app.py` | 14 passed |
| `test_program.py` | 7 passed |
| **รวมชุดหลัก** | **21 passed** |
| regression v2.0 | 25 passed |
| flake8 | 0 |
| bandit | 0 |

## 5. วิธีรัน

Fedora:

```bash
sudo dnf install python3-gobject gtk4
python3 program.py
```

โปรแกรมเปิดเป็นหน้าต่าง Desktop UI บน GNOME/Wayland

## 6. ขอบเขตที่ไม่ทำ

- ระบบล็อกอิน/สิทธิ์ผู้ใช้
- Online Payment
- multi-user concurrent server
- cloud sync

SQLite ปัจจุบันเหมาะกับ desktop single-user; ถ้าต้องการหลายผู้ใช้
สามารถเปลี่ยน persistence ผ่าน Repository ภายหลัง

## 7. Traceability

- `Sprint5/sprint2.md` — v3.0 SQLite + Member + Checkout
- `Sprint5/sprint3.md` — Desktop Program UI
- `Sprint5/program-plan.md` — แผน Desktop
- `Sprint5/SPM-29-foundation.md` … `SPM-32-hardening.md`
- `Sprint5/program.py`, `Sprint5/test_program.py` — snapshot
- `web/`, `web-plan.md` — historical implementation เดิมที่ถูกแทนที่
