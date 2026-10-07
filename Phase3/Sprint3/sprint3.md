# รายงานปิด Sprint 3 — Phase 3: ลงมือและคุมการเปลี่ยนแปลง (W8–W11)

เอกสารนี้สรุปหลักฐานสปรินต์ที่สาม ซึ่งเป็นช่วงลงมือทำงานจริงภายใต้การควบคุม
— รับคำขอเปลี่ยนแปลงผ่าน Impact Analysis และ CCB, ติดตามความคืบหน้าด้วย
Burndown/EVM, แก้บั๊กจากข้อมูลเก่า และปิดท้ายด้วยการ harden โค้ดกับ scope freeze
ข้อมูลโครงการทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. ข้อมูลสปรินต์

| รายการ | ค่า |
|---|---|
| Sprint | Sprint 3 - Phase 3 (W8-11) |
| Jira Sprint ID | 85 (state: closed) |
| Story Points | 16 SP (SPM-15…SPM-19) ปิดครบทุกใบ |
| Issues | SPM-15, SPM-16, SPM-17, SPM-18, SPM-19 |
| หลักฐานประจำสัปดาห์ | `week-8/` `week-9/` `week-10/` `week-11/` |

## 2. ทีมและบทบาท

| บุคคล | บทบาท | ความรับผิดชอบในสปรินต์นี้ |
|---|---|---|
| ภานุวัฒน์ ต๋าคำ | PM / Developer | Impact analysis, CCB, Log Work, ติดตาม EVM |
| เอกพันธ์ ทศทิศรังสรรค์ | QA / Tester | Defect-driven test, integration test, coverage |
| ณฐภาพ สายหล้า | Tech Lead / Architect | การแก้บั๊กที่รากเหง้า, code review, hardening |

## 3. งานรายสัปดาห์ (W8–W11)

| สัปดาห์ | งานที่ทำ | ไฟล์หลักฐาน |
|---|---|---|
| W8 | รับ CR-01 ด้วย Impact Analysis, ตั้ง Active Board/Burndown, Blocker Flag, Stakeholder Matrix, Procurement Log | `week-8/CR-01_Impact_Analysis.md`, `Sprint1_Tracking.md`, `Stakeholder_Matrix.md`, `Procurement_Log.md` |
| W9 | สรุป EVM, Retrospective (Mad/Sad/Glad), เตรียมปิดสปรินต์และส่งต่องาน | `week-9/EVM_Sprint1.md`, `Retrospective_Sprint1.md`, `Sprint_Transition.md` |
| W10 | CR-02 ผ่าน CCB (4.5 man-hours), แก้ BUG-101 ด้วย 5 Whys + Defect-driven test, เบิกเงินสำรอง | `week-10/CCB_Meeting_Minutes.md`, `CR-02_Impact_Decision_Form.md`, `Defect_Log_BUG-101.md`, `Contingency_Reserve_Log.md` |
| W11 | Hardening sprint, วิเคราะห์ flow/WIP, Burnup และ Scope Freeze | `week-11/Hardening_Report.md`, `Flow_Metrics.md`, `Scope_Freeze_Agreement.md` |

## 4. สิ่งที่ส่งมอบ

| สถานะ | รายการ | หลักฐาน/ข้อกำหนด |
|---|---|---|
| Delivered | CR-01: Barcode + Reorder Point | `Product.barcode` (ค่าเริ่มต้น `""`), `reorder_point` (ค่าเริ่มต้น 5), แจ้งเตือนเมื่อ `quantity <= reorder_point`; ผลกระทบประเมิน +8 man-hours; branch `feature/cr01-barcode-reorder-point`; เทสต์แบบ RED→GREEN→REFACTOR |
| Delivered | CR-02: ส่งออก CSV | อนุมัติผ่าน CCB 4.5 man-hours × 300 THB = **1,350 THB** จากเงินสำรอง; `CsvReportExporter` แยกคลาสตาม SRP ไม่ฝัง `import csv` ใน UI |
| Delivered | BUG-101 แก้ที่รากเหง้า | `KeyError: barcode` เมื่ออ่านไฟล์ JSON รุ่นเก่า → ใช้ `dict.get` + ค่า default; มี Defect Log และ 5 Whys |
| Delivered | กระบวนการ Change Control | 4 ขั้น: Submit CR → Impact Analysis → CCB Review → Update Baseline; CCB มี 4 ฝ่าย (Sponsor, User Rep, PM, Tech Lead) |
| Delivered | รายงาน EVM + Retrospective | ตัวเลขและบทเรียนพร้อม action item |
| Delivered | Hardening + Scope Freeze | กำจัด code smell, บังคับ atomic write, Bandit สะอาด, แช่แข็งขอบเขต 29 points |

## 5. Change Control และผลกระทบ

| รายการ | CR-01 | CR-02 |
|---|---|---|
| ประเภท | Perfective (Normal Change) | Perfective (Emergency/Fast-Track) |
| ผลกระทบต่นทุน | +8 man-hours | 4.5 man-hours (1,350 THB) |
| กลุ่มแตะ | Product + Repository + ConsoleUI | Service (exporter) เพิ่มใหม่ |
| การอนุมัติ | ผ่าน Impact Analysis, เลื่อนไปสปรินต์ถัดไป | ผ่าน CCB (Approve) พร้อมดึงเงินสำรอง |
| ทดสอบ | เพิ่มเคส barcode/ROP | เพิ่มเคส CSV header/เนื้อหา |

## 6. Defect: BUG-101

| หัวข้อ | รายละเอียด |
|---|---|
| อาการ | โปรแกรม crash ด้วย `KeyError: 'barcode'` เมื่อโหลด `data.json` ที่เขียนก่อนมีฟิลด์นี้ |
| ระดับ | Critical/Major |
| รากเหง้า (5 Whys) | ขาด Data Validation และ default fallback ในชั้น Repository ทำให้ schema ใหม่กระทบข้อมูลเก่า |
| วิธีแก้ | `from_dict` ใช้ `dict.get('barcode', '')` และ `dict.get('reorder_point', 5)` |
| มาตรการป้องกัน | Defect-driven test เป็นเคสถาวร + backward compatibility test |
| สถานะ | แก้แล้วและมีเทสต์รองรับ |

## 7. ผลติดตามความคืบหน้า

| ตัวชี้วัด | ค่า | ความหมาย |
|---|---|---|
| Burnup (scope vs done) | 27 / 29 points (93%) | เหลือ 2 points นอกขอบเขตที่แช่แข็ง |
| WIP limit ช่อง Review | 3 ใบ | ใช้กฎของ Little's Law ลดงานค้างสะสม |
| EVM Sprint 1 | PV 4,000 / EV 3,000 / AC 4,200 | SV −1,000, CV −1,200 (ตัวเลขสมมติเพื่อการเรียน) |
| Reserve ที่เบิกจริง | 1,350 THB (CR-02) | เหลือสำรอง 1,473 THB ก่อนเบิกปิดงาน |

## 8. Retrospective (Mad / Sad / Glad)

| ด้าน | สิ่งที่พบ |
|---|---|
| Mad | เสียเวลา merge conflict จากการตัดโครงสร้างใหญ่ในสัปดาห์เดียว (สะท้อน SV −1,000 / CV −1,200) |
| Sad | ประเมินงาน refactor ต่ำกว่าความจริงเพราะหนี้เทคนิคใน `app_v1.py` ซ่อนอยู่ |
| Glad | PyTest จับบั๊กได้ก่อนเดโม และทีมแก้ conflict สำเร็จ |
| Action | แจ้ง blocker ทุก daily standup · PR ต้อง review ภายใน 12 ชั่วโมง · เริ่มใช้ TDR (เขียนเทสต์ก่อนโค้ด) |

## 9. Scope Freeze Agreement

| ข้อ | เนื้อหา |
|---|---|
| ขอบเขตที่ล็อก | 29 story points (20 + 5 + 4) |
| สิ่งที่อนุญาตหลัง freeze | เฉพาะ Critical bug, Security fix, Test |
| สิ่งที่ไม่อนุญาต | ฟีเจอร์ใหม่, เปลี่ยน UI, Change Request ใหม่ |
| เงื่อนไขออกจาก freeze | เมื่อ entry criteria ครบ (งาน 27/29, hardening แล้ว, lint/deck ผ่าน) |

## 10. ความเสี่ยงและข้อจำกัด

| รายการ | สถานะ |
|---|---|
| Flake8 `E501` | ยังค้าง ณ สัปดาห์ที่ 11 (Bandit สะอาดแล้ว) — แก้ใน Sprint 5 |
| ข้อมูล legacy ใช้ `dict.get` | เป็น fallback ไม่ใช่ migration เต็มรูปแบบ — Sprint 5 ทำ migration + verification |
| งานค้าง 2 points ของ burnup | ต้องกลับมาทำในสปรินต์ถัดไปหรือตัด scope อย่างเป็นทางการ |
| UAT formal sign-off | ยังรอการลงนาม |

## 11. Sprint Review (ตามหลักฐานที่มี)

| หัวข้อ | หลักฐาน | ผล/ข้อสังเกต |
|---|---|---|
| สิ่งที่สาธิต | CR-01/CR-02 ทำงานจริงในโค้ด | มีหลักฐานโค้ดและเทสต์ |
| ผลที่ผ่าน | burnup 27/29, EVM คำนวณครบ | ตัวเลขสมมติเพื่อการเรียน |
| ข้อเสนอแนะ/ผู้เข้าร่วมเดโม | ไม่มีหลักฐาน | ไม่อ้างว่ามี |

## 12. งานยกยอดไปสปรินต์ถัดไป

- ปิดงานค้าง 2 points ให้ครบ 29/29
- รัน UAT SC01–SC03 และเตรียม release checklist
- แก้ Flake8 `E501` และสร้าง tag รีลีส

## 13. ภาคผนวก Evidence Index

| หมวดหลักฐาน | เส้นทาง |
|---|---|
| Change request | `week-8/CR-01_Impact_Analysis.md`, `week-10/CR-02_Impact_Decision_Form.md`, `week-10/CCB_Meeting_Minutes.md` |
| Defect | `week-10/Defect_Log_BUG-101.md`, `week-10/mock_legacy_products.json` |
| การติดตามและ EVM | `week-8/Sprint1_Tracking.md`, `week-8/mock_sprint_log.json`, `week-9/EVM_Sprint1.md`, `week-9/mock_evm.json`, `week-9/Retrospective_Sprint1.md` |
| Hardening และ freeze | `week-11/Hardening_Report.md`, `Flow_Metrics.md`, `Scope_Freeze_Agreement.md`, `mock_burnup.json` |
| งบสำรอง | `week-10/Contingency_Reserve_Log.md` |
| Stakeholder และครึ่งภาพ | `week-8/Stakeholder_Matrix.md`, `Procurement_Log.md` |