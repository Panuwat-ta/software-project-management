# รายงานปิด Sprint 2 — Phase 2: ออกแบบและตั้งต้นทุนฐาน (W5–W7)

เอกสารนี้สรุปหลักฐานสปรินต์ที่สอง ซึ่งทำหน้าที่ "วางแผนก่อนลงมือ" — ออกแบบสถาปัตยกรรมเป้าหมาย
ประเมินคุณภาพตามมาตรฐาน และตั้งงบฐานกับเกณฑ์คุมงบก่อนเข้าสู่การลงมือทำงาน
ข้อมูลโครงการทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. ข้อมูลสปรินต์

| รายการ | ค่า |
|---|---|
| Sprint | Sprint 2 - Phase 2 (W5-7) |
| Jira Sprint ID | 82 (state: closed) |
| Story Points | 13 SP (SPM-11…SPM-14) ปิดครบทุกใบ |
| Issues | SPM-11, SPM-12, SPM-13, SPM-14 |
| หลักฐานประจำสัปดาห์ | `week-5/` `week-6/` `week-7/` |

เป้าหมาย: ออกแบบ To-Be architecture ที่รองรับ SQLite/สมาชิก, ประเมินคุณภาพ
ISO 25010/14598, ตั้ง Cost Baseline ที่อนุมัติแล้ว พร้อมเกณฑ์แจ้งเตือนผลต่างงบ

## 2. ทีมและบทบาท

| บุคคล | บทบาท | ความรับผิดชอบในสปรินต์นี้ |
|---|---|---|
| ภานุวัฒน์ ต๋าคำ | PM / Developer | ประมาณการต้นทุน, จัดทำ budget worksheet, WBS |
| เอกพันธ์ ทศทิศรังสรรค์ | QA / Tester | กำหนดเป้าหมาย coverage และ quality gate |
| ณฐภาพ สายหล้า | Tech Lead / Architect | ออกแบบ To-Be, สถาปัตยกรรม, มาตรการ CI |

## 3. งานรายสัปดาห์ (W5–W7)

| สัปดาห์ | งานที่ทำ | ไฟล์หลักฐาน |
|---|---|---|
| W5 | As-Is vs To-Be flowchart, ประเมินคุณภาพ ISO 25010 (SQuaRE 8 มิติ), จัดทำ budget worksheet | `week-5/architecture.md`, `iso25010_evaluation.md`, `budget_worksheet.md`, `work.md` |
| W6 | Communication Matrix + DoR/DoD, ออกแบบ To-Be Architecture (Singleton/Repository/Strategy), วิเคราะห์ Cost Variance | `week-6/Communication_Matrix_and_DoD.md`, `To_Be_Architecture.md`, `Cost_Variance_Analysis.md` |
| W7 | ปิด Cost Baseline พร้อมเกณฑ์ Threshold, Capacity Planning, รายงาน ISO/IEC 14598 + Quality Gate | `week-7/Cost_Baseline_and_Sprint_Plan.md`, `ISO_14598_Quality_Report.md` |

## 4. สิ่งที่ส่งมอบ

| สถานะ | รายการ | หลักฐาน/ข้อกำหนด |
|---|---|---|
| Delivered | สถาปัตยกรรม To-Be | รองรับ SQLite, Member tier, Checkout ด้วย Repository Pattern |
| Delivered | แบบออกแบบฐานข้อมูล | ตารางสินค้า/สมาชิก + กลยุทธ์ย้ายข้อมูลจาก JSON (`week-6/To_Be_Architecture.md`) |
| Delivered | Cost Baseline ที่อนุมัติ | 18,823 THB แบ่งเป็นแรงงาน 15,000 / โครงสร้างพื้นฐาน 1,000 / สำรอง 2,823 |
| Delivered | เกณฑ์คุมผลต่างงบ | ปกติ ≤5%, แจ้งเตือน 5–10%, วิกฤต >10% (ให้พิจารณาตัด scope) |
| Delivered | Capacity Planning | 3 คน × 6 ชั่วโมง × 2 สัปดาห์ = 36 man-hours ต่อสปรินต์ |
| Delivered | Communication Matrix + DoR/DoD | ช่องทางสื่อสาร, เกณฑ์รับงาน (DoR) และเกณฑ์ส่งมอบ (DoD) |
| Delivered | เป้าหมายคุณภาพ ISO 14598 | v(G) ≤ 8, CBO ≤ 4, DIT ≤ 2, Coverage ≥ 85% |

## 5. ผลประเมินคุณภาพ ISO/IEC 25010 (As-Is)

| มิติ | สถานะ As-Is | เป้าหมาย |
|---|---|---|
| Functional suitability | ผ่าน (ทำงานตามเมนูได้) | คงเดิม |
| Performance efficiency | ผ่าน (ไม่มีระบบคิวขนาดใหญ่) | คงเดิม |
| Compatibility | ผ่าน (เป็น CLI สแตนด์อโลน) | คงเดิม |
| Usability | ต้องปรับ (เมนูซับซ้อน, ไม่มี validation) | ปรับด้วย validator |
| Reliability | **ตก** (เขียน JSON ทับตรง, ข้อมูลเสียได้) | atomic write → ต่อยอด SQLite |
| Security | **ตก** (ไม่มีการป้องกัน SQL injection เพราะยังไม่มี SQL) | parameterized query 100% |
| Maintainability | **ตก** (Monolithic, CC 14, global state) | แยกชั้น + OOP |
| Portability | ผ่าน (Python ล้วน) | คงเดิม |

## 6. Cost Baseline และงบประมาณ (ตัวเลขสมมติเพื่อการเรียน)

| หมวด | สัดส่วน | จำนวน (THB) |
|---|---:|---:|
| ค่าแรงงานทางตรง (งาน refactor + ทดสอบ) | 80% | 15,000 |
| โครงสร้างพื้นฐานและเครื่องมือ | 5% | 1,000 |
| งบสำรองเผื่อฉุกเฉิน | 15% | 2,823 |
| **ยอดรวมที่อนุมัติ** | **100%** | **18,823** |

> [!IMPORTANT]
> **ต้องไม่รวมตัวเลขคนละชุด:** worksheet ของสัปดาห์ที่ 5 ระบุ 39,100 THB
> (แรงงาน 31,000 + โครงสร้างพื้นฐาน 3,000 + สำรอง 5,100) ซึ่งเป็นฐานคำนวณอีกชุดหนึ่ง
> ในรายงานนี้ใช้ **18,823 THB ที่อนุมัติในสัปดาห์ที่ 7** เป็นตัวควบคุมงบ

## 7. ตัวอย่างการวิเคราะห์ Cost Variance (สัปดาห์ที่ 6)

| ตัวแปร | ค่า | ผล |
|---|---:|---|
| PV | 2,400 THB | งบตามแผนของงานย้าย JSON → SQLite |
| EV | 2,400 THB | ทำเสร็จครบตาม DoD |
| AC | 4,000 THB | ใช้จริงสูงกว่าแผน |
| CV = EV − AC | −1,600 THB | เกินงบ → เสนอดึงเงินสำรอง 15% |

บทเรียน: การย้ายระบบฐานข้อมูลมีต้นทุนแฝงเรื่อง validation/rollback ที่ไม่ได้อยู่ใน
ประมาณการเดิม จึงต้องมีเงินสำรองและเกณฑ์แจ้งเตือนล่วงหน้า

## 8. Definition of Ready / Done ที่กำหนด

**DoR (เกณฑ์รับเข้าสปรินต์):** คำอธิบายงานครบ · ประมาณการเวลาและผู้รับผิดชอบชัดเจน ·
บทบาท RACI ระบุแล้ว · ความเสี่ยงหลักถูกระบุ

**DoD (เกณฑ์ส่งมอบ):** ผ่าน peer code review ตาม PEP 8 · PyTest ผ่าน 100% ·
ไม่เพิ่มหนี้ทางเทคนิค · อัปเดต CHANGELOG · merge เข้า develop พร้อม Log Work

## 9. ความเสี่ยงและข้อจำกัด

| รายการ | สถานะ |
|---|---|
| ประมาณการต้นทุนต่างฐาน (39,100 vs 18,823) | ต้องระบุฐานให้ชัดทุกครั้งที่อ้างอิง |
| Capacity 36 man-hours ต่ำกว่างานจริงในภายหลัง | พิสูจน์แล้วว่างานวิวัฒนาการล้นความจุ |
| เป้าหมาย ISO 14598 ยังไม่ถูกวัดจริง | ปิดกับ Sprint 3/4 (Hardening) |

## 10. Sprint Review (ตามหลักฐานที่มี)

| หัวข้อ | หลักฐาน | ผล/ข้อสังเกต |
|---|---|---|
| สิ่งที่ส่งมอบ | เอกสาร 6 ชุดใน `week-5`–`week-7` | ครบตาม DoR |
| ผลที่ผ่าน | Cost Baseline + เกณฑ์ + Capacity | ตัวเลขสอดคล้องในเอกสารสัปดาห์ที่ 7 |
| การรับรอง | ไม่มีลายเซ็น | ไม่อ้างว่าได้รับการรับรอง |

## 11. งานยกยอดไปสปรินต์ถัดไป

- ปฏิบัติแผนที่อนุมัติ: รับ CR-01 ผ่าน Impact Analysis, ติดตามด้วย Burndown/EVM
- เก็บข้อมูล Log Work จริงเพื่อคำนวณ AC ให้ตรงกับแผน
- วัดเป้าหมาย ISO 14598 จริงในรอบ Hardening

## 12. ภาคผนวก Evidence Index

| หมวดหลักฐาน | เส้นทาง |
|---|---|
| สถาปัตยกรรมและคุณภาพ | `week-5/architecture.md`, `iso25010_evaluation.md`, `week-7/ISO_14598_Quality_Report.md` |
| งบประมาณ | `week-7/Cost_Baseline_and_Sprint_Plan.md`, `week-5/budget_worksheet.md`, `week-6/Cost_Variance_Analysis.md` |
| เกณฑ์การทำงาน | `week-6/Communication_Matrix_and_DoD.md` |
| แบบออกแบบที่พัฒนาต่อใน Sprint 5 | `Phase1/Sprint1/week-2/blueprint.md`, `Phase1/Sprint1/week-2/Member-Discount.md` |