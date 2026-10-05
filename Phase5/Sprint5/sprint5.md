# รายงานปิด Sprint 5 — Phase 5: v3.0 + Desktop Program

เอกสารนี้สรุป Sprint 5 ซึ่งมีสองส่วน:
1) SQLite + Member + Checkout (v3.0)
2) โปรแกรม Desktop UI ที่รันด้วย Python และ reuse domain เดิม

ข้อมูลทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน

## 1. ข้อมูลสปรินต์

| รายการ | ค่า |
|---|---|
| Sprint | Sprint 5 - Phase 5 |
| Jira Sprint ID | 86 (closed) |
| Story Points | 46 SP |
| Issues | SPM-23…SPM-27 + SPM-29…SPM-32 |
| Epics | SPM-22 + SPM-28 |
| ตัวส่งมอบหลัก | `app.py`, `program.py`, `test_app.py`, `test_program.py` |
| Desktop release tag | ยังไม่สร้างในรอบนี้ เพราะ working tree ยังไม่ได้ commit |

เป้าหมายคือให้ระบบจากเดิมที่ใช้ CLI สามารถเปิดเป็นโปรแกรมหน้าต่าง UI ได้
โดยไม่คัดลอก business logic และไม่ทำ regression กับรุ่นเดิม

## 2. ทีมและบทบาท

| บุคคล | บทบาท | ความรับผิดชอบ |
|---|---|---|
| ภานุวัฒน์ ต๋าคำ | PM / Developer | SQLite migration, Desktop UI, Checkout integration |
| เอกพันธ์ ทศทิศรังสรรค์ | QA / Tester | integration test, regression, edge cases |
| ณฐภาพ สายหล้า | Tech Lead / Architect | domain reuse, architecture, lint/security review |

## 3. งานตามแผน

### ส่วน A — v3.0: SQLite + Member + Checkout (17 SP)

| Issue | งาน | SP |
|---|---|---:|
| SPM-23 | SQLite Database Layer | 5 |
| SPM-24 | JSON → SQLite Migration | 3 |
| SPM-25 | Member CRUD 4 Tiers | 3 |
| SPM-26 | Member Discount + Checkout | 3 |
| SPM-27 | DB/Discount/Injection Tests | 3 |

### ส่วน B — Desktop Program UI (29 SP)

| Issue | งาน | SP |
|---|---|---:|
| SPM-29 | GTK4 Foundation + reuse domain | 8 |
| SPM-30 | Dashboard + Products UI | 8 |
| SPM-31 | Members + Checkout UI | 8 |
| SPM-32 | Hardening + Desktop Release Candidate | 5 |

## 4. สถาปัตยกรรม

```text
Desktop UI: program.py (GTK4)
        │
        ├─ Dashboard
        ├─ Products
        ├─ Members
        └─ Checkout
              │
              ▼
Domain: app.py
        ├─ InventoryRepository
        ├─ MemberManager
        ├─ CheckoutService
        ├─ CsvReportExporter
        └─ SQLiteDatabaseContext
              │
              ▼
         inventory.db
```

UI ไม่เขียน SQL และไม่คำนวณส่วนลดซ้ำเอง

## 5. SQLite / Migration

- ใช้ Singleton connection
- Repository ซ่อน SQL
- ทุก query ที่มี input ใช้ parameterized placeholder
- schema มี CHECK ป้องกันค่าติดลบ
- migration อ่าน legacy JSON ผ่าน `Product.from_dict`
- ตรวจ record count และ total inventory value หลังย้าย

## 6. Member / Discount / Checkout

| Tier | ส่วนลด |
|---|---:|
| Regular | 0% |
| Silver | 5% |
| Gold | 10% |
| Platinum | 15% |

Checkout ใช้ `CheckoutService` เดิม
Guest ได้ราคาเต็ม และใบเสร็จแสดง subtotal / discount / total / remaining stock

## 7. Desktop Program UI

หน้าโปรแกรมมี 4 ส่วนหลัก:

1. **ภาพรวม** — จำนวนประเภทสินค้า มูลค่ารวม และ low-stock
2. **สินค้า** — เพิ่ม/แก้ไข/ค้นหา/ตัดสต็อก/ลบ/Export CSV
3. **สมาชิก** — CRUD + เลือก Tier
4. **Checkout** — ระบุสินค้า จำนวน สมาชิก และแสดงใบเสร็จ

Responsive/Adaptive UI:
- Sidebar เมนูหลักกว้างประมาณ 1/3 ของหน้าต่างจริง และไม่ขยายเกินสัดส่วน
- Desktop ≥980 px: Dashboard 3 cards/แถว, Checkout 2 คอลัมน์
- Compact 760–979 px: form 2 คอลัมน์, Checkout แนวตั้ง
- Narrow <760 px: form/card 1 คอลัมน์, toolbar แนวตั้ง และตารางเลื่อนแนวนอนได้

ไฟล์รัน:

```bash
python3 program.py
```

บน Fedora:

```bash
sudo dnf install python3-gobject gtk4
```

โปรแกรมผ่านการเปิดจริงบน GNOME/Wayland และ process ทำงานต่อโดยไม่มี runtime error

## 8. Compatibility

| รายการ | ผล |
|---|---|
| CLI เดิม | ยังอยู่ใน `app.py` |
| barcode / reorder point | ยังทำงาน |
| CSV | reuse `CsvReportExporter` |
| JSON compatibility | legacy key ยังรองรับ |
| v2.0 regression | 25 passed |

## 9. หลักฐานทดสอบ

| ชุด | ผล |
|---|---|
| `test_app.py` | 14 passed |
| `test_program.py` | 7 passed |
| **รวม** | **21 passed** |
| regression v2.0 | 25 passed |
| flake8 | 0 |
| bandit | 0 |

ตัวอย่าง integration test Desktop:
- responsive breakpoints: Desktop / Compact / Narrow
- seed database
- dashboard metrics
- LOW/OK status
- Gold checkout 1,000 → 900
- receipt formatting
- CSV export

## 10. คุณภาพ

คำสั่งตรวจ:

```bash
python -m pytest test_app.py test_program.py -q
flake8 app.py program.py test_program.py tools/build_reports.py
bandit -q -r app.py program.py
```

ผลล่าสุด: ผ่านทั้งหมด

## 11. Jira

Epic SPM-28 และ Stories SPM-29…SPM-32 ยังคง Sprint, Story Point,
parent และสถานะ Done เดิม แต่เปลี่ยน scope/summary จาก Web เป็น Desktop Program UI

## 12. ข้อจำกัด

- ไม่มี Login / RBAC
- ไม่มี Online Payment
- SQLite เป็น local single-user
- Desktop UI ปัจจุบัน target Linux/Fedora GTK4
- UAT formal sign-off จาก Sprint 4 ยังรอลงนาม

## 13. Sprint Review

| หัวข้อ | ผล |
|---|---|
| โปรแกรมรันได้ | `python3 program.py` เปิด GTK4 window |
| Domain reuse | ใช้ Repository/Member/Checkout เดิม |
| Test | 21 + 25 passed |
| Code quality | flake8 0 / bandit 0 |
| Jira | อัปเดต scope เป็น Desktop Program |

## 14. งานต่อไป

- ทำ packaging เป็น executable/installer ถ้าต้องส่งให้ผู้ใช้ทั่วไป
- รองรับ PostgreSQL หากเปลี่ยนเป็น multi-user
- เพิ่ม role/login หากขยาย scope
- ปิด formal UAT sign-off

## 15. Evidence Index

| หมวด | หลักฐาน |
|---|---|
| v3.0 | `sprint2.md` |
| Desktop UI | `sprint3.md`, `program-plan.md` |
| โค้ด | `app.py`, `program.py` |
| Tests | `test_app.py`, `test_program.py` |
| Jira stories | `SPM-29-foundation.md` … `SPM-32-hardening.md` |
| Historical Web | `web/`, `web-plan.md` — superseded |
