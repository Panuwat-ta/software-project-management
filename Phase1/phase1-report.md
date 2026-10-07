# รายงาน Phase 1 — เริ่มโครงการและวางฐาน (W1–W4)

ข้อมูลทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. ภาพรวมเฟส

| รายการ | ค่า |
|---|---|
| Sprint ที่ครอบคลุม | Sprint 1 (Jira ID 84, closed) |
| สัปดาห์ | 1–4 |
| Issues | SPM-6…SPM-10 (15 SP) ปิดครบ |
| เวอร์ชันโค้ดที่ได้ | CLI รุ่นแรกหลัง refactor (JSON + atomic save) |

เฟสนี้วางฐานทั้งระบบ: จากกฎบัตรและการทบทวนโค้ดเดิม ไปสู่การออกแบบพิมพ์เขียว
แล้วลงมือเขียนโค้ดใหม่ที่ทดสอบได้จริง

## 2. สิ่งที่ทำตามสัปดาห์

| สัปดาห์ | เนื้อหา | ไฟล์หลักฐาน |
|---|---|---|
| W1 | Project Charter · Scope · System Understanding (ระบบเดิม 5 เมนู, ความเสี่ยง 3 ระดับรุนแรง, code smell 3 จุด) | `Sprint1/week-1/` |
| W2 | DFD L0/L1 · Hotspot · Static Analysis (LOC 99, Pylint 7.10/10, CC 14) · Blueprint · Member-Discount design | `Sprint1/week-2/` |
| W3 | `app_v2.py` (OOP 3 คลาส) · DoD 5 ข้อ · RACI · ชุดทดสอบ | `Sprint1/week-3/` |
| W4 | ปรับปรุงโค้ดรอบสุดท้ายของเฟส + เทสต์ 5 ผ่าน + `test.json` | `Sprint1/week-4/` |

## 3. ผลลัพธ์หลัก

| ด้าน | ผลลัพธ์ |
|---|---|
| โค้ด | แยก `Product` / `InventoryManager` / `InventoryCLI` ตาม Separation of Concerns |
| ความทนทาน | บันทึกไฟล์แบบ atomic (tmp + `os.replace`), กันค่าติดลบ, ตรวจชนิดข้อมูล |
| ความเข้ากันได้ | อ่านไฟล์เก่าที่ใช้คีย์ `n`/`q`/`p`/`c` ได้ |
| คุณภาพกระบวนการ | มี DoD 5 ข้อและ RACI ที่ชัดเจน |
| การทดสอบ | PyTest 5 เคส พร้อมรายงาน `test.json` |

## 4. สิ่งที่ยังไม่ทำ (ตั้งใจงด)

- SQLite, Member tiers, Checkout — ออกแบบไว้แล้วแต่ยังไม่พัฒนา (ยกยอดไป Sprint 5)
- เว็บ/หน้าจอกราฟิก — อยู่นอกขอบเขตของเฟสนี้

## 5. ปัญหาที่พบและการจัดการ

| ปัญหา | การจัดการ |
|---|---|
| `CC 14` ซับซ้อนเกินเกณฑ์ | แยกเป็นคลาสใน W3 |
| ข้อมูลเสียหายเมื่อเขียน JSON | เปลี่ยนเป็น atomic write |
| โค้ดไม่มี validation | เพิ่ม validator ในชั้น UI และ guard ในชั้น logic |

## 6. รายงานและหลักฐานฉบับเต็ม

- รายงานปิดสปรินต์: [`Sprint1/sprint1.md`](Sprint1/sprint1.md) · [หน้าเว็บ](Sprint1/sprint1.html) · [PDF](Sprint1/sprint1.pdf)
- ข้อเสนอรวมเฟส: [`Sprint1/proposal/Integrated_Planning_Proposal.md`](Sprint1/proposal/Integrated_Planning_Proposal.md)
- README ของเฟส: [`README.md`](README.md)