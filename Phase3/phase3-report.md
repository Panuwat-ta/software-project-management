# รายงาน Phase 3 — ลงมือและคุมการเปลี่ยนแปลง (W8–W11)

## 1. วัตถุประสงค์

รับ requirement ใหม่แบบคุมได้ (CR-01/CR-02) แก้บั๊กข้อมูลเก่า (BUG-101)
ติดตามงานด้วย Burndown/EVM แล้ว hardening + แช่แข็งขอบเขตก่อนปล่อย

## 2. งานรายสัปดาห์

| สัปดาห์ | งาน | หลักฐาน |
|---|---|---|
| W8 | CR-01 (Barcode + Reorder Point) Impact Analysis, Sprint Tracking, Burndown | `week-8/` |
| W9 | EVM Sprint 1 (SV −1,000 / CV −1,200), Retrospective, เปิด Sprint 2 | `week-9/` |
| W10 | CR-02 CSV ผ่าน CCB, BUG-101 `KeyError: barcode` (แก้ด้วย `dict.get`), เบิกสำรอง | `week-10/` |
| W11 | Hardening (ลบ code smells, Atomic, Bandit สะอาด, Flake8 ค้าง E501), Scope Freeze 29 pts | `week-11/` |

## 3. สิ่งส่งมอบ

- CR-01/CR-02 + BUG-101 fix รวมในโค้ด evolution
- EVM + Retrospective + แผน Sprint 2
- Scope Freeze Agreement + Hardening Report

## 4. สถานะ

เสร็จครบ (Jira: SPM-15…SPM-19 Done) พร้อมเข้า Phase 4 (UAT/Release)
