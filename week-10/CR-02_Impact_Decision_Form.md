# แบบฟอร์มผลกระทบและการตัดสินใจ CR-02 (CR-02 Impact & Decision Form) — การส่งออก CSV ฉุกเฉิน

> สัปดาห์ที่ 10 — กระบวนการจัดการคำขอฉุกเฉิน (Emergency Fast-Track) ตาม ISO/IEC 14764 / IEEE 1219: **ห้ามกระโดดไปแก้โค้ดโดยไร้การควบคุม**

| ฟิลด์ (Field) | ค่า (Value) |
|---|---|
| รหัสการเปลี่ยนแปลง (Change ID) | CR-02 (คำขอด่วน — Emergency Change Request) |
| ชื่อเรื่อง (Title) | Export รายชื่อสินค้าสต็อกต่ำเป็นไฟล์ `.csv` ทันที |
| ความจำเป็นทางธุรกิจ (Business Need) | นำไปเปิดใน Excel เพื่อสั่งซื้อสินค้าเติมคลังด่วน ป้องกันสินค้าขาดสต็อก |
| ประเภท (Type) | Emergency Change Request (เทียบ: CR-01 Barcode & Reorder Point สัปดาห์ที่ 8–9 เป็น Normal Change ผ่าน Sprint Planning/Backlog ปกติ) |
| ขั้นตอน Fast-Track | 1. Identify (ตรวจความถูกต้อง+ความเร่งด่วน) → 2. Impact (วิเคราะห์สถาปัตยกรรม+ข้อมูล) → 3. Estimate (ประเมิน Man-Hours ส่งต่อ CCB) → 4. Hotfix & CI (พัฒนาบน Branch เฉพาะ + รัน PyTest) |
| Branch | `feature/cr02-csv-export` (รอรวมเข้า `develop` ตามรอบ Sprint ได้ตามปกติ; ต่างจาก `hotfix/critical-db-crash` ที่แตกจาก `main` ตรงเมื่อบั๊กวิกฤตบน Production) |

## การประเมินผลกระทบ 3 มิติ (Impact Assessment)
1. **Data & Architecture Impact:** อ่านข้อมูลจากโมเดล `Product` และเรียก `is_low_stock()`; สร้างคลาสใหม่ **`CsvReportExporter`** ตามหลัก Single Responsibility แยกขาดจาก UI
2. **Testing Impact:** ต้องเขียน Unit Test **2 เคส** (ทดสอบการสร้างไฟล์ CSV + ความถูกต้องของ Header/Data); Regression: ไม่กระทบฟังก์ชันเดิมใน `InventoryService`
3. **ข้อห้าม (Bad Practice):** ห้ามยัด `import csv` แล้วเขียนไฟล์ลงใน `ConsoleUI` หรือ `InventoryRepository` (ทำให้เกิด Tight Coupling ทำลาย Clean Architecture)

## การออกแบบ CsvReportExporter
- คลาสเฉพาะ `CsvReportExporter` แปลง List ของ `Product` เป็นข้อความ/ไฟล์ CSV อย่างอิสระ (Static Method ไร้ State ทดสอบแยกง่าย)
- Header: `ProductID,ProductName,Barcode,Quantity,ReorderPoint,Price`
- ใช้ Context Manager `with open(..., 'w', newline='', encoding='utf-8')` ปิดไฟล์อัตโนมัติ รองรับภาษาไทยสมบูรณ์
- ตัวอย่างแถวข้อมูลจาก Unit Test: `P01,Sugar,111,2,5,20.0` (ไฟล์ `test_low_stock.csv`, ใช้ fixture `tmp_path` สร้าง/ลบอัตโนมัติ)

## ประมาณการ Effort & Risk (ตัวเลขส่งต่อ PM เข้าที่ประชุม CCB)

| องค์ประกอบงาน (Task Breakdown) | ผู้รับผิดชอบ (Role) | Man-Hours | ระดับความเสี่ยง |
|---|---|---|---|
| 1. สร้างคลาส CsvReportExporter | Senior Developer | 2.0 ชม. | Low  |
| 2. เชื่อมโยงเมนู Console UI | Developer | 1.0 ชม. | Low  |
| 3. เขียน Unit Test ครอบคลุมไฟล์ CSV | QA Tester | 1.5 ชม. | Low  |
| **รวม Technical Effort ทั้งสิ้น** | | **4.5 Man-Hours** | **Overall: Low Risk** |

- **ต้นทุน (Cost):** ประมาณ **1,350 บาท** (4.5 ชม. @ 300 บาท)
- เงื่อนไขด้านบั๊ก: การส่งออก CSV จะสืบทอดอาการล่มของ BUG-101 หากไม่รวมวิธีแก้ `dict.get('barcode', '')` ในชั้น Repository ก่อน

## สามเหลี่ยมเหล็ก (Iron Triangle: Scope–Time–Cost)
กฎเหล็ก: หากลูกค้าขอขยาย Scope (CR-02) ต้องขยาย Cost (งบประมาณ) หรือขยาย Time (เวลา) เสมอ มิฉะนั้น Quality (คุณภาพ) จะพังทลาย

## ทางเลือกทางการบริหาร (Trade-off Analysis)

| ทางเลือก | ข้อดี (Pros) | ข้อแลกเปลี่ยน / ความเสี่ยง (Trade-offs) |
|---|---|---|
| **Option A: Approve in Sprint 2** | ลูกค้าได้รับไฟล์ CSV ทันทีเพื่อสั่งซื้อสินค้าเติมคลัง ไม่เกิดสินค้าขาดสต็อก | ต้องดึงเงินสำรอง 1,350 บาท และเสี่ยงทำให้งาน Barcode หลุดกำหนด |
| **Option B: Defer to Sprint 3** | ทีมรักษา Focus งานหลักของ Sprint 2 ได้ 100% ไม่ต้องทำโอที | ลูกค้าต้องรออีก 1 สัปดาห์ อาจต้องใช้ระบบจดมือสั่งซื้อสินค้าชั่วคราว |

## การตัดสินใจ (สำหรับ CCB — วงกลมเลือก 1 มติ)
- [ ] **Approve (อนุมัติ):** ยอมรับทันที โดยตกลงดึงงบจาก Contingency Reserve หรือขยายเวลา Sprint 2
- [ ] **Defer (เลื่อนการทำ):** เห็นชอบว่ามีประโยชน์ แต่ยกยอดไปเปิดเป็นการ์ด Task แรกของ Sprint 3
- [ ] **Reject (ปฏิเสธ):** ไม่คุ้มค่าทางธุรกิจ หรือส่งผลให้โครงการหลักเสี่ยงล้มเหลวรุนแรง
- ข้อตกลงร่วม (หากอนุมัติ): อนุมัติ **4.5 Man-Hours @ 300 THB/ชม.**
- บันทึกต่อใน: `CCB_Meeting_Minutes.md`, `Contingency_Reserve_Log.md`
