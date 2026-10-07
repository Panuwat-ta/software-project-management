# Desktop Program Plan — Sprint 5

## เป้าหมาย

เปลี่ยนตัวส่งมอบส่วน UI จาก Web App เป็นโปรแกรม Desktop ที่รันด้วย Python โดยตรง
และ reuse business logic เดิมจาก `app.py` ทั้งหมด

## ขอบเขต

| Issue | งาน | SP |
|---|---|---:|
| SPM-29 | GTK4 Desktop Foundation + reuse domain | 8 |
| SPM-30 | Dashboard + Products UI | 8 |
| SPM-31 | Members + Checkout UI | 8 |
| SPM-32 | Hardening + Desktop Release | 5 |

รวม 29 SP และยังอยู่ใน Sprint 5 / Epic SPM-28 เดิม

## สถาปัตยกรรม

```text
program.py (GTK4 UI)
        │
        ├── InventoryRepository
        ├── MemberManager
        ├── CheckoutService
        └── CsvReportExporter
                │
              app.py
                │
             SQLite
```

UI ไม่เขียน SQL และไม่คัดลอก business logic ซ้ำ

## หน้าจอ

1. ภาพรวม — ประเภทสินค้า มูลค่าคงคลัง และรายการใกล้จุดสั่งซื้อ
2. สินค้า — เพิ่ม/แก้ไข/ค้นหา/ตัดสต็อก/ลบ/Export CSV
3. สมาชิก — CRUD สมาชิกและ 4 tiers
4. Checkout — ตัดสต็อก + ส่วนลด + ใบเสร็จ

## UX/UI Hardening

ปรับรอบ UX/UI สำหรับ Desktop Program โดยไม่แก้ business logic:

- Sidebar มี active state และ visual hierarchy ชัดเจน
- Header แสดงสถานะ SQLite และมีปุ่มรีเฟรชข้อมูล
- ใช้ status banner สำหรับ success/error แทน popup ในงานทั่วไป
- ฟอร์มสินค้า/สมาชิกแยกสถานะ "เพิ่ม" และ "กำลังแก้ไข" ชัดเจน
- ตารางมีจำนวนรายการ, empty state และ badge LOW/OK
- การลบสินค้า/สมาชิกต้องยืนยันก่อนดำเนินการ
- Checkout แยก "ข้อมูลการขาย" กับ "สรุปใบเสร็จ" และเน้นยอดสุทธิ
- Checkout สำเร็จแล้ว reset ช่องกรอกสำหรับรายการถัดไป แต่คงใบเสร็จล่าสุดไว้
- เพิ่ม tooltip/helper text ในจุดที่ผู้ใช้มีโอกาสสับสน
- ลด modal interruption เพื่อให้ทำงานหลายรายการต่อเนื่องได้เร็วขึ้น
- เพิ่ม Adaptive/Responsive layout 3 ระดับตามความกว้างหน้าต่าง:
  - Sidebar เมนูหลักคำนวณประมาณ 1/3 ของความกว้างหน้าต่าง และบังคับไม่ให้ GTK ขยายเกินสัดส่วน
  - Desktop ≥ 980 px — แสดงชื่อเมนูเต็ม, Dashboard 3 cards/แถว, Checkout 2 คอลัมน์
  - Compact 760–979 px — Sidebar ยังอยู่ประมาณ 1/3, Forms 2 คอลัมน์, Checkout เรียงแนวตั้ง
  - Narrow < 760 px — Sidebar ยังอยู่ประมาณ 1/3, Forms 1 คอลัมน์, Dashboard card 1/แถว และ toolbar เรียงแนวตั้ง
- ตาราง Products/Members ใช้ horizontal scroll เมื่อพื้นที่ไม่พอ แทนการบีบข้อมูลจนอ่านยาก

## การทดสอบ

- `test_app.py` 14 เคส
- `test_program.py` 7 integration tests (รวม responsive breakpoints)
- รวมชุดหลัก 21 เคส
- regression v2.0 25 เคส
- `flake8 app.py program.py test_program.py tools/build_reports.py` = 0
- `bandit -q -r app.py program.py` = 0

## วิธีรัน

```bash
python3 program.py
```

Fedora:

```bash
sudo dnf install python3-gobject gtk4
```

## หมายเหตุ

implementation แบบ FastAPI/SPA ใน `web/` เป็นงานเดิมก่อนเปลี่ยน scope
และเก็บไว้เพื่อ traceability เท่านั้น ตัวส่งมอบ UI ปัจจุบันคือ `program.py`
