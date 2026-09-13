# รายงานการประชุม CCB (CCB Meeting Minutes) — สัปดาห์ที่ 10 (CR-02 + BUG-101)

> กระบวนการ Integrated Change Control: 1. Submit CR → 2. Impact Analysis → 3. CCB Review → 4. Update Baseline — หน้าที่ CCB คือสกัดกั้น Scope Creep (งานงอกนอกรอบโดยไร้การเพิ่มงบ/ขยายเวลา ซึ่งทำให้ทีม Overworked/Burnout ข้อบกพร่องพุ่ง ส่งมอบล่าช้า งบล่ม)

| หัวข้อ (Item) | รายละเอียด (Detail) |
|---|---|
| วาระการประชุม (Agenda) | พิจารณาคำขอด่วน CR-02 (ขอส่งออก CSV รายงานสต็อกต่ำทันที) + รับทราบ BUG-101 |
| ข้อมูลนำเข้า (Inputs) | `Defect_Log_BUG-101.md`, `CR-02_Impact_Decision_Form.md` (ตัวเลข 4.5 Man-Hours / ประมาณ 1,350 บาท) |
| คณะกรรมการ CCB (Members) | Sponsor / อาจารย์ (อำนาจสูงสุดด้านงบประมาณ+ทิศทางธุรกิจ) • User Representative (คุณค่า+การใช้งานจริง) • Project Manager (ผลกระทบเวลา+งบประมาณ+ทรัพยากร) • Tech Lead (สถาปัตยกรรม+ความเสี่ยงเชิงโค้ด) |
| การลงนามรับรอง | Project Manager + Sponsor (อาจารย์) ลงนามร่วมกันเป็นหลักฐานแนบรายงาน |

## สรุปการอภิปราย (Discussion Summary)
1. **BUG-101:** ยืนยันรุนแรงระดับ Critical/Major (โปรแกรม Crash เมื่อเจอข้อมูลเก่าไร้ `barcode`); รากเหง้าคือขาด Data Validation + Default Fallback ในชั้น `InventoryRepository`; วิธีแก้คือ `dict.get('barcode', '')`
2. **CR-02:** ผลประโยชน์ลูกค้าคือได้ไฟล์ CSV ทันทีไปสั่งซื้อเติมคลัง (กันของขาดสต็อก); ผลประโยชน์ทีมคือรักษา Focus งานหลัก Sprint 2 (โดยเฉพาะงาน Barcode) ไม่ให้เกิด Burnout
3. ชั่งน้ำหนัก **Option A: Approve in Sprint 2** (ได้ CSV ทันที แต่ดึงสำรอง 1,350 บาท + เสี่ยงงาน Barcode หลุด) เทียบกับ **Option B: Defer to Sprint 3** (รักษา Focus 100% ไม่ต้องโอที แต่ลูกค้ารอ 1 สัปดาห์ ใช้จดมือชั่วคราว)

## มติที่ประชุม (Decision — เลือก 1 ใน 3)
- [ ]  **Approve (อนุมัติ):** ยอมรับทันที โดยตกลงดึงงบจาก Contingency Reserve หรือขยายเวลา Sprint 2
- [ ]  **Defer (เลื่อนการทำ):** ยกยอดไปเปิดเป็นการ์ด Task แรกของ Sprint 3
- [ ]  **Reject (ปฏิเสธ):** ไม่คุ้มค่าทางธุรกิจ หรือเสี่ยงให้โครงการหลักล้มเหลวรุนแรง
- **BUG-101:** อนุมัติให้แก้ที่ราก (`dict.get` Fallback ใน Repository) พร้อม Defect-Driven Test เป็นเกราะถาวร
- **ข้อตกลงร่วม (หากอนุมัติ CR-02):** อนุมัติ **4.5 Man-Hours @ 300 THB/ชม.** (1,350 บาท จาก Contingency Reserve ที่ตั้งไว้ในสัปดาห์ที่ 5)

## การเจรจาต่อรอง (Principled Negotiation — Fisher & Ury, 2011)
1. **Separate People from Problem:** แยกอารมณ์/ตัวบุคคลออกจากปัญหา มุ่งแก้ที่เนื้องาน
2. **Focus on Interests:** มุ่งผลประโยชน์ทางธุรกิจที่แท้จริง ไม่ยึดติดคำสั่ง
3. **Invent Options for Mutual Gain:** คิดค้นทางเลือกร่วมกัน (Option A vs B) ให้ได้ประโยชน์ทั้งสองฝ่าย — ปกป้องทีม + สร้างความมั่นใจให้ลูกค้า
4. **Use Objective Criteria:** ยืนบนเกณฑ์ที่วัดได้ (ตัวเลข 4.5 Man-Hours และ Team Capacity)
-  ห้ามพูด: "ทำไม่ได้ครับ งานล้นมือแล้ว ลูกค้ามาสั่งช้าเอง ช่วยไม่ได้ครับ" (ทำลายความสัมพันธ์ ลูกค้ากลายเป็น Resistant ทันที)
-  เทคนิค Yes, if...: "เราสามารถส่งมอบ CSV ให้ได้ในสัปดาห์นี้ครับ หากเราขอย้ายการตกแต่ง UI ไปทำใน Sprint 3 แทน"
-  เทคนิค Defer with Priority: "เพื่อให้ระบบบาร์โค้ดเสถียรที่สุด เราขอนำฟังก์ชัน CSV นี้เป็น Task แรกของ Sprint 3 ครับ"

## การปรับปรุงเส้นฐาน (Update Baseline — หากอนุมัติ)
- **Scope:** + ข้อกำหนดส่งออก CSV (เกณฑ์ยอมรับ: รวมระเบียนเก่าไร้ `barcode` ได้); การ์ด Jira ใหม่ Summary: `[CR-02] Export Low Stock Products to CSV`, Original Estimate: 4.5h, Assignee: Senior Dev / Dev ตาม RACI → ลากเข้ากล่อง Active Sprint 2
- **Burndown:** เส้น Actual Line จะ "หักหัวพุ่งสูงขึ้นกะทันหัน (Scope Injection Bump)" — PM เขียน Comment กำกับบน Jira ว่า **"Scope increase due to CCB approval on CR-02"** พร้อมแคปเจอร์กราฟแนบรายงาน
- **Forecast:** หาก Remaining Capacity ไม่พอ → ขออนุมัติขยายวันสิ้นสุด Sprint 2 (Sprint End Date Adjustment); หรือใช้ Scope Swapping ปลดการ์ด Low Priority คืนสู่ Backlog เพื่อรักษาวันปิด Sprint เดิมโดยไม่เพิ่มโหลด
- **Cost:** ตัดยอด 1,350 บาทจาก Contingency Reserve → ดู `Contingency_Reserve_Log.md`
- **Tools:** เช็คโควต้า GitHub Actions ไม่เกิน 2,000 นาทีฟรี/เดือน (Unit Test CSV ทำให้ CI รันบ่อยขึ้น); ตรวจว่าไฟล์ CSV ชั่วคราวไม่กิน Disk Space กระทบค่า Cloud Server

## รายการที่ต้องดำเนินการ (Action Items)
- [ ] PM: ถือ CR-02 Impact Analysis Form เข้าพบ Sponsor นำเสนอตัวเลข 4.5 Man-Hours + ผลกระทบ Iron Triangle เสนอ Option A vs B รับมติและขอลายเซ็น
- [ ] Dev: พัฒนาวิธีแก้ BUG-101 + คลาส `CsvReportExporter` บน Branch `feature/cr02-csv-export` รัน Full Suite ผ่าน 100% แล้ว Push
- [ ] PM: ตัดยอด Contingency Reserve + อัปเดต Log + ปรับ Forecast/Swapping + สื่อสารทีม
