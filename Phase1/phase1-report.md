# รายงาน Phase 1 — เริ่มโครงการและวางฐาน (W1–W4)

## 1. วัตถุประสงค์

วางกฎบัตร ขอบเขต และบทบาททีม ทำความเข้าใจระบบเดิม ตรวจสุขภาพโค้ด
ออกแบบพิมพ์เขียวปรับโครงสร้าง แล้วลงมือ refactor พร้อมทดสอบ

## 2. งานรายสัปดาห์

| สัปดาห์ | งาน | หลักฐาน |
|---|---|---|
| W1 | Project Charter, Scope, ทบทวนระบบเดิม (global `x`, JSON, ไม่ตรวจ input) | `week-1/` |
| W2 | DFD, Hotspot, Static Analysis (LOC 99, Pylint 7.10, CC 14), Blueprint, ออกแบบ Member-Discount | `week-2/` |
| W3 | `app_v2.py` (OOP/Validation/Atomic), DoD, RACI, ชุดทดสอบ | `week-3/` |
| W4 | ทดสอบ 5 ผ่าน ปรับปรุง `app.py` | `week-4/` |

ข้อเสนอภาพรวม: `proposal/Integrated_Planning_Proposal.md`

## 3. สิ่งส่งมอบ

- โค้ด refactor: `Product`/`InventoryManager`/`InventoryCLI`, Atomic Save,
  รองรับคีย์เก่า `n`/`q`/`p`/`c`
- เกณฑ์คุณภาพ: DoD, RACI, PyTest 5 passed + `test.json`
- แบบออกแบบที่ยกยอด: SQLite, Member tiers, Checkout (ไป Phase 5)

## 4. สถานะ

เสร็จครบ เป็นฐานให้ Phase 2–4 ต่อยอด (Jira: SPM-6…SPM-10 Done)
