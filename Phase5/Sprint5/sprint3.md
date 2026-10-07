# รายงาน Sprint 5 · ส่วน Desktop Program — จาก CLI สู่โปรแกรม UI

เอกสารนี้สรุปงานส่วน UI ของ Sprint 5 หลังเปลี่ยน scope จาก Web App
มาเป็นโปรแกรม Desktop ที่รันด้วย Python โดยตรง
ข้อมูลทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน

## 1. วัตถุประสงค์และขอบเขต

เปลี่ยนระบบคลังสินค้า CLI ให้มีหน้าตาโปรแกรม Desktop โดยใช้ GTK4/PyGObject
และ reuse `app.py` v3.0 ทั้งก้อน ไม่คัดลอก business logic หรือ SQL ซ้ำใน UI

Epic: SPM-28 · Stories: SPM-29…SPM-32 · รวม 29 SP · Sprint 5 (ID 86)

## 2. งานตามแผน

| Issue | งาน | SP | หลักฐาน |
|---|---|---:|---|
| SPM-29 | GTK4 Foundation + reuse domain | 8 | `SPM-29-foundation.md`, `program.py` |
| SPM-30 | Dashboard + Products Desktop UI | 8 | `SPM-30-products.md` |
| SPM-31 | Members + Checkout Desktop UI | 8 | `SPM-31-checkout.md` |
| SPM-32 | Hardening + Desktop Release Candidate | 5 | `SPM-32-hardening.md` |

## 3. สิ่งที่ส่งมอบ

| รายการ | ผล |
|---|---|
| โปรแกรม Desktop | `program.py` รันแล้วเปิด GTK4 window |
| Dashboard | จำนวนประเภทสินค้า มูลค่ารวม และ low-stock |
| Products | เพิ่ม/แก้ไข/ค้นหา/ตัด/ลบ/Export CSV |
| Members | CRUD + 4 tiers |
| Checkout | ส่วนลดอัตโนมัติ + ใบเสร็จ |
| Persistence | SQLite ผ่าน Repository เดิม |
| Migration | ใช้ `migrate_json_to_sqlite` เดิม |
| Compatibility | CLI เดิมใน `app.py` ยังใช้งานได้ |

## 4. UX/UI ที่ปรับปรุง

- Sidebar ระบุหน้าปัจจุบันด้วย active state
- Header แสดงสถานะ SQLite และมีคำสั่งรีเฟรช
- Form สินค้าและสมาชิกแสดงโหมดเพิ่ม/แก้ไขชัดเจน
- Products/Members มี item count และ empty state
- สถานะ stock ใช้ badge LOW/OK ที่สแกนด้วยสายตาได้เร็ว
- การลบต้องยืนยันก่อนเพื่อป้องกันการกดพลาด
- Success/error ใช้ status banner ไม่ขัดจังหวะ workflow ด้วย dialog ทุกครั้ง
- Checkout แบ่งข้อมูลการขายกับใบเสร็จ พร้อมแสดงยอดสุทธิเด่น
- Responsive 3 ระดับ: Desktop ≥980 px, Compact 760–979 px และ Narrow <760 px
- Sidebar เมนูหลักกว้างประมาณ 1/3 ของหน้าต่างจริงและไม่ขยายกินพื้นที่เกินสัดส่วน; เมื่อหน้าต่างแคบ form/card จะลดจำนวนคอลัมน์ และ Checkout เปลี่ยนเป็นแนวตั้ง
- ตารางสินค้า/สมาชิกใช้ horizontal scroll เพื่อรักษาความอ่านง่าย

## 5. วิธีรัน

Fedora:

```bash
sudo dnf install python3-gobject gtk4
python3 program.py
```

โปรแกรมเปิดเป็นหน้าต่าง GUI ไม่ต้องเปิด browser และไม่ต้องรัน server

## 6. หลักฐานทดสอบ

| ชุด | ผล |
|---|---|
| `test_app.py` | 14 passed |
| `test_program.py` | 7 passed |
| **รวมชุดหลัก** | **21 passed** |
| regression `Phase4/Sprint4/week-12/test_app.py` | 25 passed |
| flake8 | 0 |
| bandit | 0 |

## 7. สถาปัตยกรรม

```text
GTK4 program.py
   ├─ Dashboard / Products / Members / Checkout
   └─ reuse app.py
        ├─ InventoryRepository
        ├─ MemberManager
        ├─ CheckoutService
        ├─ CsvReportExporter
        └─ SQLiteDatabaseContext
             └─ inventory.db
```

## 8. Jira และ traceability

Epic SPM-28 และ stories SPM-29…SPM-32 คงสถานะ Done
แต่แก้ Summary/Description จาก Web เป็น Desktop Program UI
โดยไม่เปลี่ยน Story Point หรือ parent

## 9. หลักฐาน

- แผน: `program-plan.md`
- โค้ด: `program.py`, `app.py`
- ทดสอบ: `test_program.py`, `test_app.py`
- ราย story: `SPM-29-foundation.md` … `SPM-32-hardening.md`
- `web/` และ `web-plan.md`: historical implementation ที่ถูกแทนที่
