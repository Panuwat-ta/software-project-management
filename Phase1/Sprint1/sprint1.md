# รายงานปิด Sprint 1 — Phase 1: เริ่มโครงการและวางฐาน (W1–W4)

เอกสารนี้สรุปหลักฐาน Sprint แรกของโครงการ ครอบคลุมสัปดาห์ที่ 1–4
ตั้งแต่การวางกฎบัตรจนถึงการเขียนโค้ดใหม่และทดสอบ
ข้อมูลโครงการทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. ข้อมูลสปรินต์

| รายการ | ค่า |
|---|---|
| Sprint | Sprint 1 - Phase 1 (W1-4) |
| Jira Sprint ID | 84 (state: closed) |
| Board | SPM board (ID 71) · โปรเจกต์ SPM |
| Story Points | 15 SP (SPM-6…SPM-10) ปิดครบทุกใบ |
| Issues | SPM-6, SPM-7, SPM-8, SPM-9, SPM-10 |
| หลักฐานประจำสัปดาห์ | `week-1/` `week-2/` `week-3/` `week-4/` |
| ข้อเสนอรวมเฟส | `proposal/Integrated_Planning_Proposal.md` (+ `.pdf`) |

เป้าหมายของสปรินต์: ตั้งกฎบัตรและขอบเขต ทำความเข้าใจระบบเดิม ตรวจสุขภาพโค้ด
ออกแบบพิมพ์เขียวปรับโครงสร้าง แล้วลงมือ refactor พร้อมชุดทดสอบอัตโนมัติ

## 2. ทีมและบทบาท

| ชื่อ-นามสกุล | รหัสนักศึกษา | บทบาท | ความรับผิดชอบในสปรินต์นี้ |
|---|---|---|---|
| ภานุวัฒน์ ต๋าคำ | 6754210044-3 | Project Manager / Developer | Input validation, การจัดเก็บข้อมูล, บริหารงาน |
| เอกพันธ์ ทศทิศรังสรรค์ | 67543210050-0 | QA / Tester | ออกแบบ test cases, รัน PyTest, รายงาน `test.json` |
| ณฐภาพ สายหล้า | 67543210054-2 | Tech Lead / Architect | ออกแบบสถาปัตยกรรม, Code Review ตาม PEP 8 |

## 3. งานรายสัปดาห์ (W1–W4)

| สัปดาห์ | งานที่ทำ | ไฟล์หลักฐาน |
|---|---|---|
| W1 | Project Charter, Scope of Work, ทบทวนระบบเดิม 5 เมนู + ระบุความเสี่ยง 3 ระดับรุนแรง | `week-1/Project-Charter.md`, `scope.md`, `doc.md`, `app_v1.py`, `trello.md` |
| W2 | DFD (L0/L1), Hotspot 3 จุด, Static Analysis, พิมพ์เขียว Blueprint, ออกแบบระบบสมาชิก/ส่วนลด | `week-2/DFD.md`, `Hotspot.md`, `Static-Analysis.md`, `blueprint.md`, `Member-Discount.md`, `trello.md` |
| W3 | เขียน `app_v2.py` ตามบลูปริ้นท์ (OOP 3 คลาส, validation, atomic write) + กำหนด DoD 5 ข้อ + RACI | `week-3/app_v2.py`, `dod.md`, `raci.md`, `test_app.py`, `test_app1.py`, `test.json` |
| W4 | ทดสอบและปรับปรุงโค้ดรอบสุดท้ายของสปรินต์ (5 tests ผ่าน) | `week-4/app.py`, `test_app.py`, `test.json`, `test_app.png` |

## 4. สิ่งที่ส่งมอบ

| สถานะ | รายการ | หลักฐาน/ข้อกำหนด |
|---|---|---|
| Delivered | โค้ด refactor 3 คลาส | `Product` / `InventoryManager` / `InventoryCLI` แยก Business Logic ออกจาก UI ตาม SoC |
| Delivered | Atomic Save | เขียนไฟล์ชั่วคราว `*.tmp` แล้ว `os.replace` ทับ ไม่ใช้ `json.dump` เขียนทับตรง |
| Delivered | Input Validation | `_get_input()` + validator ต่อช่อง: ไม่รับค่าติดลบ, `amount > 0`, กัน `ValueError` |
| Delivered | Backward compatibility | `Product.from_dict` รองรับคีย์สั้น `n`/`q`/`p`/`c` และค่าเริ่มต้นเมื่อฟิลด์ขาด |
| Delivered | ชุดทดสอบอัตโนมัติ | PyTest 5 เคส + รายงานผลเป็น `test.json` ผ่าน custom plugin |
| Delivered | เกณฑ์คุณภาพงาน | DoD 5 ข้อ (`week-3/dod.md`) และ RACI (`week-3/raci.md`) |
| ออกแบบเท่านั้น | SQLite, Member tiers, Checkout | อยู่ใน `week-2/blueprint.md`, `Member-Discount.md` ยังไม่ implement |

## 5. หลักฐานทดสอบ

| ชุด | ผล | ครอบคลุม |
|---|---|---|
| `week-3/test_app.py`, `week-4/test_app.py` | 5 passed | สรุปมูลค่าคลัง + low stock, ตัดสต็อกสำเร็จ/ของไม่พอ/ไม่มีสินค้า, เพิ่ม-อัปเดตสินค้า |
| `test.json` | 5/5 PASS | รายงานผลอัตโนมัติทุกครั้งที่รัน |

## 6. ผลตรวจคุณภาพโค้ด

**ก่อนปรับปรุง (ตั้งฐาน สัปดาห์ที่ 2 จาก `week-2/Static-Analysis.md`)**

| ตัวชี้วัด | ค่า | หมายเหตุ |
|---|---|---|
| Lines of Code | 99 (LLOC 77, SLOC 78) | โค้ดเดิมแบบ Monolithic |
| Pylint | 7.10 / 10 | คะแนนรวมกลุ่ม Convention |
| Cyclomatic Complexity (`main`) | 14 (เกรด C) | เป้า ISO 14598 คือ ≤ 8 |
| R0912 (branches) | 17 (เกณฑ์ 12) | เมนู if/elif ซ้อนกันลึก |
| R0915 (statements) | 55 (เกณฑ์ 50) | ฟังก์ชันเดียวทำทุกอย่าง |
| อื่นๆ | C0303 trailing whitespace, C0301 บรรทัดยาว, C0304 ไม่มี newline ท้ายไฟล์ | PEP 8 |

**หลังปรับปรุง:** `app.py` ที่ส่งมอบมีโครงสร้างเป็นคลาสแยกหน้าที่ ตรรกะธุรกิจ
แยกจากการรับ/แสดงผล และเทสต์ผ่านครบ แต่รายงานนี้ไม่ได้วัด Pylint/CC ซ้ำ
หลังปรับ จึงไม่อ้างตัวเลขเดิมเป็นผลหลังปรับปรุง

## 7. Definition of Done ที่ใช้ตรวจ (5 ข้อ)

1. ผ่านการทดสอบอัตโนมัติ 100% (PyTest passed)
2. โค้ดเขียนตามมาตรฐานการออกแบบ (PEP 8 / แยกชั้น)
3. ความปลอดภัยและการดักจับข้อผิดพลาด (validation, atomic write, กันค่าติดลบ)
4. อัปเดตเอกสารคู่มือครบถ้วน (docstrings + doc/)
5. ผ่านการรีวิวและการอนุมัติ (Code Review + Approve)

## 8. EVM และงบประมาณ (ตัวเลขสมมติเพื่อการเรียน)

> บันทึกการวิเคราะห์ใน `week-9/EVM_Sprint1.md` (สัปดาห์ที่ 9) และงบฐานใน `week-7/`

| ตัวแปร | ค่า | ความหมาย |
|---|---:|---|
| PV (Planned Value) | 4,000 THB | ตั้งเป้า 4 tasks งบ task ละ 1,000 |
| EV (Earned Value) | 3,000 THB | ปิด Done ได้ 3 tasks |
| AC (Actual Cost) | 4,200 THB | ชั่วโมงจริงจาก Log Work |
| SV = EV − PV | −1,000 THB | ล่าช้ากว่าแผน |
| CV = EV − AC | −1,200 THB | เกินงบ 1,200 บาท |

- สาเหตุ: หนี้ทางเทคนิคซ่อนใน `app_v1.py` + เสียเวลาแก้ Merge Conflict
- การตอบสนอง: ยกงานหลุดไปสปรินต์ถัดไป, ชดเชยส่วนเกินด้วยเงินสำรอง
- เงินสำรองที่ตั้งไว้ 2,823 บาท (15% ของ baseline 18,823) — เบิกจริงภายหลัง 1,350 บาท (CR-02)

## 9. ความเสี่ยง ข้อจำกัด และหนี้เทคนิค

| รายการ | สถานะ |
|---|---|
| ไฟล์ JSON เสี่ยงพังเมื่อเขียนทับ | ลดด้วย atomic write แต่ยังไม่มี transaction ระดับฐานข้อมูล |
| ข้อมูลเก่าใช้คีย์สั้น | รองรับด้วย fallback ใน `from_dict` (ยังไม่ใช่ migration เต็มรูปแบบ) |
| Flake8 `E501` | ค้างในไฟล์ snapshot ของสัปดาห์ที่ 1–4 (แก้ในโค้ดสดภายหลัง Sprint 5) |
| สเกล | รองรับผู้ใช้คนเดียว ไม่มีการล็อกไฟล์ |

## 10. งานที่ยกยอดไปสปรินต์ถัดไป

- ออกแบบและพัฒนา SQLite + Member tiers + Checkout (เดิมเป็นแบบออกแบบเท่านั้น)
- รับ CR-01 (Barcode + Reorder Point) และ CR-02 (CSV Export) ผ่านกระบวนการ Change Control
- แก้ BUG-101 (`KeyError: barcode` เมื่อเจอข้อมูลเก่า)
- ปิดช่องลายเซ็น UAT และสร้าง tag รีลีส

## 11. Sprint Review (ตามหลักฐานที่มี)

| หัวข้อ | สิ่งที่ยืนยันได้จากหลักฐาน | ผล/ข้อสังเกต |
|---|---|---|
| สิ่งที่สาธิต | โครงสร้าง 3 คลาส + PyTest 5 เคส | เดโมสดของสปรินต์นี้ไม่มีหลักฐานการบันทึก |
| ผลที่ผ่าน | ชุดทดสอบ 5 passed พร้อม `test.json` | ยืนยันได้จากไฟล์ใน `week-3/`, `week-4/` |
| การรับรองจาก Sponsor | ไม่มีหลักฐานลายเซ็น | ไม่อ้างว่าได้รับการรับรอง |

## 12. ตารางงานค้างและงานยกยอด

| งาน | สถานะปิดสปรินต์ | ย้ายไป |
|---|---|---|
| SQLite + Member + Checkout | ออกแบบแล้ว ยังไม่พัฒนา | Sprint 5 (Phase 5) |
| CR-01 / CR-02 / BUG-101 | ยังไม่รับ | Sprint 3 (Phase 3) |
| UAT sign-off, Git tag | ยังไม่ทำ | Sprint 4 (Phase 4) — tag ปิดแล้วในรอบตรวจรับ |
| Flake8 `E501` | ค้างใน snapshot | แก้ใน Sprint 5 (โค้ดสด E501 = 0) |

## 13. ภาคผนวก Evidence Index

| หมวดหลักฐาน | เส้นทาง |
|---|---|
| กฎบัตร/ขอบเขต/ระบบเดิม | `week-1/Project-Charter.md`, `scope.md`, `doc.md`, `app_v1.py`, `trello.md` |
| วิเคราะห์และแบบออกแบบ | `week-2/DFD.md`, `Hotspot.md`, `Static-Analysis.md`, `blueprint.md`, `Member-Discount.md`, `trello.md` |
| โค้ดและเกณฑ์งาน | `week-3/app_v2.py`, `dod.md`, `raci.md`, `week-4/app.py`, `test_app.py`, `test.json` |
| ข้อเสนอภาพรวมเฟส | `proposal/Integrated_Planning_Proposal.md`, `proposal/slides.html` |
| EVM และการส่งต่องาน | `Phase3/Sprint3/week-9/EVM_Sprint1.md`, `Sprint_Transition.md` |
| งบฐาน | `Phase2/Sprint2/week-7/Cost_Baseline_and_Sprint_Plan.md` |
| เวอร์ชันที่ส่งมอบจริง | tag `v2.0.0-evolution` (โค้ดสดที่รากรีโปคือ v3.0 จาก Sprint 5) |