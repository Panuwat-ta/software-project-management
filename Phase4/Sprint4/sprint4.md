# รายงานปิด Sprint 4 — Phase 4: UAT ปล่อยรุ่น v2.0 (W12)

เอกสารนี้สรุปหลักฐานสปรินต์ที่สี่ ซึ่งปิดวงจร W1–12 ด้วยการทดสอบการยอมรับผู้ใช้ (UAT)
การเตรียมปล่อยรุ่น และการสรุปสถานะการเงิน/ความคืบหน้าของโครงการ
ข้อมูลโครงการทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. ข้อมูลสปรินต์

| รายการ | ค่า |
|---|---|
| Sprint | Sprint 4 - Phase 4 (W12) |
| Jira Sprint ID | 83 (state: closed) |
| Story Points | 5 SP (SPM-20, SPM-21) ปิดครบทุกใบ |
| Issues | SPM-20 (UAT), SPM-21 (Release + Final EVM) |
| หลักฐานประจำสัปดาห์ | `week-12/` |
| รุ่นที่ส่งมอบ | `v2.0.0-evolution` (annotated tag) |

## 2. ทีมและบทบาท

| บุคคล | บทบาท | ความรับผิดชอบในสปรินต์นี้ |
|---|---|---|
| ภานุวัฒน์ ต๋าคำ | PM / Developer | จัดทำ release checklist, final EVM, procurement |
| เอกพันธ์ ทศทิศรังสรรค์ | QA / Tester | ออกแบบ UAT scenario และ cross-team test |
| ณฐภาพ สายหล้า | Tech Lead / Architect | ตรวจ release gate, merge ขึ้น main |

## 3. งานสัปดาห์ที่ 12

| งาน | หลักฐาน |
|---|---|
| โค้ดวิวัฒนาการรวม CR-01, CR-02 และ fix BUG-101 | `week-12/app.py`, `app.py` (snapshot ที่รากของสปรินต์นี้) |
| ชุดทดสอบเติบโตจาก 5 → 25 เคส | `week-12/test_app.py` |
| UAT scenario SC01–SC03 + sign-off sheet | `week-12/UAT_Sign_Off_Sheet.md` |
| Release checklist 3 ด่าน | `week-12/Release_Checklist.md` |
| CHANGELOG รุ่น 2.0.0-evolution | `week-12/CHANGELOG.md` |
| Final EVM และการเคลียร์งบ | `week-12/Final_EVM.md` |

## 4. สิ่งที่ส่งมอบ (เทียบกับรุ่นก่อนหน้า)

| รายการ | v1.0 | v2.0.0-evolution |
|---|---|---|
| ฐานข้อมูล | JSON เขียนทับตรง | JSON + atomic write (tmp + `os.replace`) |
| โครงสร้าง | Monolithic + global `x` | OOP 3 คลาส แยก Logic/UI |
| Barcode | ไม่มี | `Product.barcode` + แสดงในรายการ/CSV |
| Reorder Point | เตือนที่ค่าคงที่ | แจ้งเตือนเมื่อ `quantity <= reorder_point` |
| CSV Export | ไม่มี | `CsvReportExporter` (หัวตาราง 6 คอลัมน์) |
| เทสต์ | 5 เคส | 25 เคส |

หัวตาราง CSV: `ProductID,ProductName,Barcode,Quantity,ReorderPoint,Price`

## 5. หลักฐานทดสอบ

| ชุด | ผล | โครงสร้าง |
|---|---|---|
| `week-12/test_app.py` | **25 passed** | baseline 5 + CR-01 4 + CR-02 6 + BUG-101 4 + CLI 3 + integration 3 |
| regression ปัจจุบัน | 25 passed ยังไม่แตก | ยืนยันว่าการพัฒนา Sprint 5 ไม่ทำให้รุ่นเก่าเสีย |

## 6. UAT: สถานการณ์ SC01–SC03

| Scenario | ผู้ใช้ | ขั้นตอน | เกณฑ์ผ่าน | ผล |
|---|---|---|---|---|
| SC01 | Inventory Manager | เพิ่มสินค้า Milk (885) สต็อก 10 ชิ้น ROP = 5 | บันทึกสำเร็จ ไร่ crash | ผ่าน |
| SC02 | Store Cashier | ตัดสต็อก 6 ชิ้น เหลือ 4 | แจ้งเตือนสต็อกต่ำทันที | ผ่าน |
| SC03 | Purchasing Officer | ส่งออก CSV แล้วเปิดใน Excel | มีคอลัมน์ Barcode และข้อมูลถูกต้อง | ผ่าน |

> [!IMPORTANT]
> **สถานะที่ยืนยันได้:** ผลทางเทคนิคของทั้ง 3 scenario ผ่าน และมีการคัดแยกประเด็น
> (Defect ต้องแก้ก่อน merge / ขอใหม่ไปรุ่นถัดไป) แต่ **ช่องลายเซ็นของผู้ทดสอบและ
> Tech Lead ยังไม่ได้ลงนาม** จึงไม่ถือว่าการรับรองแบบทางการเสร็จสมบูรณ์

## 7. Release Checklist 3 ด่าน

| ด่าน | เนื้อหา | สถานะปิดรอบนี้ |
|---|---|---|
| 1. คุณภาพก่อนปล่อย | UAT SC01–03 ผ่าน + แยกประเด็น | ผ่าน (ลายเซ็นยังรอ) |
| 2. Technical gate | regression 25/25, PR develop→main, CI เขียว, Tech Lead merge | ผ่านในรอบปิดสปรินต์ถัดไป |
| 3. การปล่อยจริง | merge main + annotated tag + release note + Final EVM | tag `v2.0.0-evolution` สร้างแล้ว |

## 8. Final EVM และการเคลียร์งบ (ตัวเลขสมมติเพื่อการเรียน)

| ตัวแปร | ค่า | ผล |
|---|---:|---|
| PV | 15,525 THB | ตามแผนรวมทั้งโครงการ |
| EV | 15,525 THB | เสร็จตามแผน |
| AC | 16,100 THB | เกินจริง 575 บาท |
| SPI = EV / PV | 1.00 | ตรงเวลา |
| CPI = EV / AC | 0.96 | เกินงบเล็กน้อย |
| CV | −575 THB | คิดเป็น 3.7% ของยอดใช้จริง |

**การเคลียร์เงินสำรอง:** 2,823 (ตั้งไว้) − 1,350 (CR-02) − 575 (เบิกปิดงาน) = **เหลือ 898 THB**
Velocity: Sprint 1 = 15 · Sprint 2 = 22 · Sprint 3 = 12 points

## 9. CHANGELOG รุ่น 2.0.0-evolution

| หมวด | รายการ |
|---|---|
| Added | Barcode (CR-01), Reorder Alert (CR-02), CSV Export (CR-02) |
| Changed | สกีมา `Product` ขยาย 2 ฟิลด์, เลขเมนู CLI ปรับเป็น 6 |
| Removed | ตัวแปรสปาเก็ตตี global `x` |
| Fixed | BUG-101 รองรับคีย์เก่าและค่า default |

## 10. ความเสี่ยงและข้อจำกัด

| รายการ | สถานะปิดรอบนี้ |
|---|---|
| ช่องลายเซ็น UAT | ว่าง — รอผู้รับรองลงนาม |
| การรองรับข้อมูลเก่า | เป็น fallback ไม่ใช่ migration เต็มรูปแบบ |
| Flake8 `E501` | ยังค้างในโค้ดรุ่นนี้ |
| ขอบเขต SQLite/Member | ยังเป็นแบบออกแบบ ยกยอดไป Sprint 5 |

## 11. Sprint Review (ตามหลักฐานที่มี)

| หัวข้อ | หลักฐาน | ผล/ข้อสังเกต |
|---|---|---|
| สิ่งที่ส่งมอบ | โค้ด + 25 เทสต์ + เอกสาร release | ครบตาม release checklist |
| ผลที่ผ่าน | EVM, procurement, contingency settlement | ตัวเลขสอดคล้องกัน |
| การรับรองจาก Sponsor | ไม่มีลายเซ็น | ไม่อ้างว่าได้รับการรับรอง |

## 12. งานยกยอดไปสปรินต์ถัดไป

- พัฒนา SQLite + Member tiers + Checkout ตามแบบออกแบบที่ค้างไว้
- แก้ Flake8 `E501`
- ปิดช่องลายเซ็น UAT ให้ครบถ้วน

## 13. ภาคผนวก Evidence Index

| หมวดหลักฐาน | เส้นทาง |
|---|---|
| โค้ดและเทสต์รุ่นนี้ | `week-12/app.py`, `week-12/test_app.py`, `app.py`, `test_app.py` |
| UAT และ release | `week-12/UAT_Sign_Off_Sheet.md`, `week-12/Release_Checklist.md`, `week-12/mock_demo.json` |
| การเงินและปิดรอบ | `week-12/Final_EVM.md` |
| บันทึกการเปลี่ยนแปลง | `week-12/CHANGELOG.md` |
| สไลด์/สรุปรอบ W1–12 | `sprint1-slides.html`, `summary-w1-w12.pdf`, `sprint-report.html` |
| รุ่นที่ปล่อย | tag `v2.0.0-evolution` |