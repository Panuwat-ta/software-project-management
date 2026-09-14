# รายงานปิด Sprint 1 — ระบบจัดการสินค้าคงคลังแบบ CLI

เอกสารนี้สรุปหลักฐานในโฟลเดอร์ `Sprint1/` สำหรับงานรายวิชา ข้อมูลโครงการทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. วัตถุประสงค์และขอบเขต Sprint 1

เป้าหมายจาก Project Charter คือเพิ่มความเสถียรของ CLI, ปรับโครงสร้างเพื่อนำตัวแปร global `x` ออกและแยกโมดูล, รักษาความถูกต้องของข้อมูลด้วยการเขียน JSON แบบอะตอมมิก และเพิ่มการทดสอบอัตโนมัติ การทบทวนระบบเดิมพบ CLI 5 เมนู ใช้ JSON และตัวแปร global `db` กับ `x`; มีการแปลง `int`/`float` โดยไม่มี `try/except` และยอมรับค่าติดลบได้

ข้อมูลการติดตามที่ยืนยันจาก Jira: Sprint 1 (ID 45) ปิดแล้ว มี 20 issues สถานะ Done ภายใต้เวอร์ชัน `v2.0.0`; Sprint 2 (ID 48) ยังเปิดเพื่อทำ v3.0 แบบ SQLite และงาน Member ต่อไป ข้อมูลตัวเลขเชิงแผนงานและต้นทุนในรายงานนี้เป็นข้อมูลสมมติเพื่อการเรียน

## 2. ทีมและบทบาท

| บุคคล | บทบาท | ความรับผิดชอบหลัก |
|---|---|---|
| Panuwat | PM / Developer | บริหารงานและพัฒนา |
| Ekkapan | QA / Tester | ออกแบบและทดสอบอัตโนมัติ |
| Nattapap | Tech Lead / Architect | ออกแบบสถาปัตยกรรมและทบทวนโค้ด |

อ้างอิงบทบาทจาก `README.md` และการกำหนดความรับผิดชอบใน `week-3/raci.md`.

## 3. งานรายสัปดาห์ W1-W12

**W1:** จัดทำกฎบัตร ขอบเขต และความเข้าใจระบบเดิมใน `week-1/Project-Charter.md`, `week-1/scope.md`, `week-1/doc.md` และใช้ `week-1/app_v1.py` เป็นฐานเปรียบเทียบความเสี่ยงของ CLI/JSON เดิม

**W2:** วิเคราะห์ data flow และ hotspot พร้อมกำหนดแนวทาง refactor ใน `week-2/DFD.md`, `week-2/Hotspot.md`, `week-2/Static-Analysis.md` และ `week-2/blueprint.md`; `week-2/Member-Discount.md` เป็นงานออกแบบต่อยอด ไม่ใช่ฟังก์ชันที่ส่งมอบแล้ว

**W3:** พัฒนาโค้ดปรับโครงสร้างและกำหนดเกณฑ์งาน/บทบาทผ่าน `week-3/app_v2.py`, `week-3/dod.md`, `week-3/raci.md` และชุดทดสอบในโฟลเดอร์เดียวกัน

**W4:** ทดสอบและปรับปรุงเวอร์ชัน refactor ใน `week-4/app.py` และ `week-4/test_app.py`; ตรวจเทียบไฟล์แล้ว `week-3/app_v2.py`, `week-4/app.py` และ `app.py` ที่รากรีโปเป็นไฟล์เหมือนกันทุกไบต์

**W5:** บันทึกการประเมินสถาปัตยกรรม คุณภาพ และตารางต้นทุนใน `week-5/architecture.md`, `week-5/iso25010_evaluation.md`, `week-5/budget_worksheet.md` และ `week-5/work.md`

**W6:** จัดทำเกณฑ์การสื่อสาร/DoD และสถาปัตยกรรมเป้าหมายใน `week-6/Communication_Matrix_and_DoD.md` กับ `week-6/To_Be_Architecture.md`; SQLite, Member tier และ Checkout ในส่วนนี้เป็นแบบออกแบบเท่านั้น

**W7:** จัดทำ baseline และแผน Sprint ใน `week-7/Cost_Baseline_and_Sprint_Plan.md` และรายงานคุณภาพใน `week-7/ISO_14598_Quality_Report.md`

**W8:** วิเคราะห์ผลกระทบ CR-01 และติดตาม Sprint ด้วย `week-8/CR-01_Impact_Analysis.md` และ `week-8/Sprint1_Tracking.md`; CR-01 ถูกจัดเป็น Normal Change เพื่อทำใน Sprint 2

**W9:** สรุป EVM ของ Sprint 1 การทบทวน และการส่งต่องานใน `week-9/EVM_Sprint1.md`, `week-9/Retrospective_Sprint1.md` และ `week-9/Sprint_Transition.md`

**W10:** บันทึกการตัดสินใจ CR-02 และการแก้ BUG-101 ผ่าน `week-10/CR-02_Impact_Decision_Form.md`, `week-10/CCB_Meeting_Minutes.md`, `week-10/Defect_Log_BUG-101.md` และ `week-10/Contingency_Reserve_Log.md`

**W11:** ควบคุมคุณภาพและแช่แข็งขอบเขตใน `week-11/Hardening_Report.md`, `week-11/Flow_Metrics.md` และ `week-11/Scope_Freeze_Agreement.md`

**W12:** รวมการวิวัฒนาการผลิตภัณฑ์ หลักฐานทดสอบ EVM และการเตรียมปล่อยใน `week-12/app.py`, `week-12/test_app.py`, `week-12/CHANGELOG.md`, `week-12/Final_EVM.md`, `week-12/UAT_Sign_Off_Sheet.md` และ `week-12/Release_Checklist.md`

## 4. สิ่งที่ส่งมอบ

| สถานะ | รายการ | หลักฐาน/ข้อกำหนด |
|---|---|---|
| Delivered | โค้ด refactor: `Product`, `InventoryManager`, `InventoryCLI` | `InventoryManager` บันทึกผ่านไฟล์ชั่วคราวและ `os.replace`; รองรับคีย์เก่า `n`/`q`/`p`/`c`; CLI ตรวจข้อมูลนำเข้า |
| Delivered | ความเข้ากันได้กับข้อมูลเก่าและการแก้ BUG-101 | `dict.get` fallback สำหรับ `barcode`; โหลดข้อมูลเก่าโดยไม่เกิด `KeyError` |
| Delivered | การวิวัฒนาการ W12 | `barcode` ค่าเริ่มต้นเป็นสตริงว่าง, `reorder_point` ค่าเริ่มต้น 5, low stock ใช้ `<=`, และ `CsvReportExporter` มีหัวตาราง `ProductID,ProductName,Barcode,Quantity,ReorderPoint,Price` |
| ออกแบบเท่านั้น | SQLite, Member tiers และ Checkout | อยู่ใน `week-2/blueprint.md`, `week-2/Member-Discount.md`, `week-6/To_Be_Architecture.md`; ยังไม่ implement |
| คงค้าง | SQLite v3.0 และงาน Member | Sprint 2 backlog ตามสถานะที่ยืนยันจาก Jira |

ค่ารายงาน Static Analysis ที่รายงานไว้เดิมคือ LOC 99, Pylint 7.10/10 และความซับซ้อนของ `main()` CC 14 ระดับ C; เป็นค่าที่รายงานไว้ ไม่ได้วัดซ้ำในรายงานฉบับนี้

## 5. หลักฐานทดสอบ

| ชุดทดสอบ | ผลที่ยืนยัน | ขอบเขต |
|---|---|---|
| `test_app.py` ที่รากรีโป | 5 passed | พฤติกรรมหลักของระบบ refactor |
| `week-12/test_app.py` | 25 passed | 5 baseline + 4 CR-01 + 6 CR-02 + 4 BUG-101 + 3 CLI + 3 integration |

![ผลรันชุดทดสอบหลัก 5 passed บนสาขา phase2](img/test.png)

*ภาพ: ผลรันชุดทดสอบหลัก 5 passed (หลักฐานชุดราก ไม่ใช่ชุด week-12 25 tests)*

![ผลรันชุดทดสอบ week-12 25 passed บนสาขา phase2](img/test1.png)

*ภาพ: ผลรัน `python -m pytest test_app.py -q` ใน week-12 25 passed (หลักฐานชุดวิวัฒนาการ)*

ต้องรันสองชุดแยกกัน เพราะการ collect ร่วมกันชนกันจากชื่อไฟล์ร่วม `test_app.py` หลักฐานฮาร์ดเดนนิงยืนยันการเขียนแบบอะตอมมิกและการจับข้อยกเว้นแบบเจาะจงเท่านั้น; Bandit สะอาด ขณะที่ Flake8 ยังรายงานรายการ line-length `E501` จึงยังไม่ถือว่าสะอาดครบทุกกฎ lint

## 6. EVM และงบประมาณ

ตัวเลขทุกตารางในหัวข้อนี้เป็นข้อมูลสมมติเพื่อการเรียน และใช้เพื่อสรุปการควบคุมโครงการในรายวิชาเท่านั้น

| ช่วง | PV | EV | AC | SV / CV หรือดัชนี |
|---|---:|---:|---:|---|
| Sprint 1 | 4,000 | 3,000 | 4,200 | SV -1,000; CV -1,200 |
| Sprint 2 | 11,350 | 11,000 | 11,500 | SPI 0.97; CPI 0.96 |
| Final | 15,525 | 15,525 | 16,100 | SPI 1.00; CPI 0.96; CV -575 |

Sprint 1 ล่าช้าและเกินงบตาม SV/CV ข้างต้น ส่วนผลรวมสุดท้ายตรงตามแผนด้านเวลา แต่เกินงบ 575 บาท หรือ 3.7% ซึ่งครอบคลุมด้วยเงินสำรอง ข้อมูลสมมติเพื่อการเรียน

| รายการงบประมาณ | ค่า | หมายเหตุ |
|---|---:|---|
| Baseline ที่อนุมัติจาก Week 7 | 18,823 THB | ข้อมูลสมมติเพื่อการเรียน |
| เงินสำรองคงเหลือ | 2,823 - 1,350 - 575 = 898 THB | ข้อมูลสมมติเพื่อการเรียน |
| Burnup | 27/29 points (93%) | ข้อมูลสมมติเพื่อการเรียน |
| Velocity | S1 15 / S2 22 / S3 12 | ข้อมูลสมมติเพื่อการเรียน |

ต้องไม่รวมตัวเลขคนละชุดเข้าด้วยกัน: worksheet ของ Week 5 ระบุ 39,100 THB และ transcript ระบุ 15,525 THB ซึ่งต่างจาก baseline ที่อนุมัติ 18,823 THB ทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียนและมีฐานอ้างอิงต่างกัน

## 7. สรุป CR และ Defect

| รายการ | ผลสรุป | ผลกระทบ/สถานะ |
|---|---|---|
| CR-01 | เพิ่ม Barcode และ Reorder Point | Normal Change, เพิ่ม 8 man-hours (ข้อมูลสมมติเพื่อการเรียน), วางใน Sprint 2 |
| BUG-101 | `KeyError: barcode` เมื่อ JSON เก่าไม่มีฟิลด์ | แก้ด้วย `dict.get` fallback เพื่อทนต่อข้อมูลเก่า |
| CR-02 | ส่งออก CSV ฉุกเฉิน | ผ่าน CCB; 4.5 ชั่วโมง x 300 THB/ชั่วโมง = 1,350 THB จาก contingency (ข้อมูลสมมติเพื่อการเรียน) |

CR-02 ใช้ `CsvReportExporter` แยกหน้าที่ออกจาก CLI และมีหัว CSV ตามที่ระบุในหัวข้อสิ่งที่ส่งมอบ การอนุมัติและค่าใช้จ่ายที่กล่าวถึงในตารางเป็นข้อมูลสมมติเพื่อการเรียน

## 8. UAT และความพร้อมปล่อย

`UAT_Sign_Off_Sheet.md` กำหนดสถานการณ์ UAT-SC01 ถึง UAT-SC03 ได้แก่ รับสินค้า, ตัดสต็อกให้ถึงจุดแจ้งเตือน และส่งออก CSV เพื่อตรวจใน Excel แต่ช่องลายเซ็นของผู้ทดสอบและ Tech Lead ยังว่าง ดังนั้นสถานะคือรอการลงนามยอมรับอย่างเป็นทางการ ไม่ควรระบุว่า UAT sign-off เสร็จแล้ว

`CHANGELOG.md` สำหรับ `v2.0.0-evolution` จัดเตรียมแล้ว แต่ยังไม่มี Git tag `v2.0.0-evolution` บน `main`; แท็กที่พบคือ `v1.0.0` เท่านั้น ความพร้อมปล่อยจึงเป็น “เตรียมเอกสารและทดสอบแล้ว แต่รอ formal sign-off, การรวมสายตาม checklist และการติดแท็ก”

## 9. ความเสี่ยง ข้อจำกัด และหนี้เทคนิค

- ข้อมูล JSON แบบเก่ายังเป็นความเสี่ยงด้าน compatibility; การ fallback ปัจจุบันบรรเทา BUG-101 แต่ไม่ใช่ schema migration เต็มรูปแบบ
- Flake8 ยังมี `E501` จึงมีหนี้ด้านรูปแบบโค้ด แม้ Bandit สะอาดและมีมาตรการ atomic write แล้ว
- SQLite, Member tiers และ Checkout ยังเป็นแบบออกแบบเท่านั้น จึงไม่ควรถูกนำเสนอเป็นความสามารถที่ปล่อยแล้ว
- UAT formal sign-off และ Git tag รีลีสยังคงค้างอยู่ ทำให้การปล่อยจริงยังไม่สมบูรณ์

## 10. งานต่อ Sprint 2

- นำ SQLite v3.0 จากแบบออกแบบมาวางแผนและพัฒนา โดยไม่อ้างว่าเสร็จแล้ว
- พัฒนาระบบ Member tiers และ Checkout ตาม `blueprint.md`, `Member-Discount.md` และ To-Be Architecture
- จัดการ CR-01 ตามแผน Sprint 2 และรักษา regression tests สำหรับข้อมูล legacy
- ปิด formal UAT sign-off, ดำเนินรายการใน release checklist และสร้าง tag หลังเงื่อนไขการปล่อยครบ
- แก้รายการ Flake8 `E501` ที่คงค้าง และรักษาผล Bandit ให้สะอาด

## 11. Sprint Review

Sprint 1 ปิดแล้วโดยมี 20 issues สถานะ Done ภายใต้เวอร์ชัน v2.0.0 (ข้อมูลสมมติเพื่อการเรียน) ส่วนผลเดโมต่อหน้าผู้รับการสาธิต วันเวลา ผู้เข้าร่วม และการอนุมัติ: หลักฐานไม่พบ

| หัวข้อ | สิ่งที่ยืนยันได้จากหลักฐาน | ผล/ข้อสังเกต |
|---|---|---|
| สิ่งที่จะสาธิต | สคริปต์ใน Transition กำหนดให้แสดงโครงสร้าง Product/Repository/Service รัน PyTest ทดลองเพิ่ม/ลดสต็อกและคำนวณราคารวม | เป็นขอบเขตของสคริปต์เดโม ไม่ใช่หลักฐานว่าเดโมเกิดครบทุกขั้น (ชื่อคลาสในสคริปต์ไม่ตรงชื่อจริง `InventoryManager` ทั้งหมด) |
| ผลที่ผ่าน | Transition บันทึก regression บน develop ผ่าน 4 tests ใน 0.12 วินาที (ข้อมูลสมมติเพื่อการเรียน) รายงานปัจจุบันยืนยัน week-12 ผ่าน 25 tests (ข้อมูลสมมติเพื่อการเรียน) | ยืนยันความพร้อมทดสอบตามหลักฐาน แต่การรับรองจาก Sponsor: หลักฐานไม่พบ |
| สิ่งที่ส่งมอบเพื่อสาธิต | refactor การรองรับข้อมูลเก่า Barcode/Reorder Point และ CSV reporting | SQLite Member tiers และ Checkout ยังเป็นแบบออกแบบ ไม่ควรนำเสนอว่าเสร็จแล้ว |
| ข้อเสนอแนะจากผู้เข้าร่วมเดโม | หลักฐานไม่พบ | ไม่บันทึกความเห็นหรือการอนุมัติโดยอนุมาน |

**Mad/Sad/Glad จาก Retrospective:** Mad — เสียเวลากับ Merge Conflict จากการผ่าตัดโครงสร้างใหญ่จน SV −1,000 CV −1,200 (ข้อมูลสมมติเพื่อการเรียน); Sad — ประเมินงาน refactor ต่ำไปเพราะหนี้เทคนิคใน `app_v1.py`; Glad — PyTest จับบั๊กได้ก่อนเดโมและทีมแก้ conflict สำเร็จ **Action สู่ Sprint 2:** สื่อสาร blocker ทุก Daily Standup ตรวจ PR ภายใน 12 ชั่วโมงหลังแจ้งเตือน (ข้อมูลสมมติเพื่อการเรียน) และเริ่มงานแบบเขียนเทสต์ก่อนโค้ด (TDR)

## 12. ตารางงานค้างและงานยกยอด

| งาน | สถานะ | สาเหตุ | ย้ายไป Sprint 2 อย่างไร |
|---|---|---|---|
| SQLite v3.0 | ออกแบบเท่านั้น | ยังไม่มีการ implement | พัฒนาและทดสอบใน SQLite/Member epic ขนาด 17 story points (ข้อมูลสมมติเพื่อการเรียน) |
| Member tiers | ออกแบบเท่านั้น | ยังไม่มีการ implement | อยู่ใน epic เดียวกันข้างต้น |
| Checkout | ออกแบบเท่านั้น | มีเพียงพิมพ์เขียวและเอกสารสถาปัตยกรรม | แตกงานพัฒนา/ทดสอบเข้า Sprint 2 backlog ภายใต้ขอบเขต SQLite/Member |
| พิธีลงนาม UAT | ตัดออก | ข้อมูลจำลองไม่ต้องมีพิธีลงนาม เหลือแค่ผล SC01–SC03 ทางเทคนิคในเอกสาร |
| Release checklist | ค้าง | รายการ 3 ด่านยังไม่ถูกติ๊กครบ | ปิดทีละด่านตาม checklist เดิมก่อนผสานสายหลัก |
| Git tag `v2.0.0-evolution` | ค้าง | มีเพียง tag `v1.0.0` | สร้าง annotated tag หลัง UAT checklist และเงื่อนไขปล่อยครบ |
| Flake8 `E501` | ค้าง (หนี้เทคนิค) | ยังมี line-length violations แม้ Bandit สะอาด | งานแก้ lint พร้อมรันตรวจซ้ำใน Sprint 2 |

หมายเหตุ: CR-01 (Barcode/Reorder Point) ถือว่าส่งมอบแล้วใน `week-12/app.py` พร้อมเทสต์ ไม่ใช่งานยกยอด

## 13. ภาคผนวก Evidence Index

| หมวดหลักฐาน | เส้นทาง |
|---|---|
| ทีมและบทบาท | `README.md`, `Sprint1/week-3/raci.md` |
| Charter และระบบเดิม | `Sprint1/week-1/Project-Charter.md`, `Sprint1/week-1/scope.md`, `Sprint1/week-1/doc.md`, `Sprint1/week-1/app_v1.py` |
| การวิเคราะห์และแบบออกแบบ | `Sprint1/week-2/DFD.md`, `Sprint1/week-2/Hotspot.md`, `Sprint1/week-2/Static-Analysis.md`, `Sprint1/week-2/blueprint.md`, `Sprint1/week-2/Member-Discount.md` |
| โค้ดและเกณฑ์งาน refactor | `Sprint1/week-3/app_v2.py`, `Sprint1/week-3/dod.md`, `Sprint1/week-4/app.py`, `app.py`, `test_app.py` |
| แผนบูรณาการ | `Sprint1/Phase1/Integrated_Planning_Proposal.md` |
| แผน/งบ/สถาปัตยกรรม | `Sprint1/week-5/`, `Sprint1/week-6/`, `Sprint1/week-7/` |
| การติดตามและ EVM Sprint 1 | `Sprint1/week-8/CR-01_Impact_Analysis.md`, `Sprint1/week-8/Sprint1_Tracking.md`, `Sprint1/week-9/EVM_Sprint1.md`, `Sprint1/week-9/Sprint_Transition.md` |
| Change และ defect | `Sprint1/week-10/CR-02_Impact_Decision_Form.md`, `Sprint1/week-10/CCB_Meeting_Minutes.md`, `Sprint1/week-10/Defect_Log_BUG-101.md`, `Sprint1/week-10/Contingency_Reserve_Log.md` |
| Hardening และ scope freeze | `Sprint1/week-11/Hardening_Report.md`, `Sprint1/week-11/Flow_Metrics.md`, `Sprint1/week-11/Scope_Freeze_Agreement.md` |
| Release และ UAT | `Sprint1/week-12/app.py`, `Sprint1/week-12/test_app.py`, `Sprint1/week-12/CHANGELOG.md`, `Sprint1/week-12/Final_EVM.md`, `Sprint1/week-12/UAT_Sign_Off_Sheet.md`, `Sprint1/week-12/Release_Checklist.md` |
