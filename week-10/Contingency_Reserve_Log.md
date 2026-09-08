# บันทึกเงินสำรองฉุกเฉิน (Contingency Reserve Log) — สัปดาห์ที่ 10

> หลักธรรมาภิบาลทางการเงิน: เมื่อ CCB มีมติ **Approved** ให้เพิ่มงาน CR-02 PM ต้องตัดยอดจาก **Contingency Reserve (ที่ตั้งไว้ในสัปดาห์ที่ 5)** มาจ่ายค่าแรง 4.5 ชม. และบันทึกอย่างโปร่งใสลงใน **Contingency Reserve Utilization Log** เพื่อให้ตรวจสอบได้ในการทำ Audit ท้ายโครงการ

## กติกาเบิกใช้ (Reserve Drawdown Rules)
- เบิกใช้ได้เฉพาะเมื่อ CCB มีมติ **Approve** เท่านั้น; **Defer / Reject = ไม่เบิก**
- เบิกจากเงินสำรองที่ตั้งไว้ในสัปดาห์ที่ 5 เพื่อจ่ายงาน CR-02 (4.5 ชม. @ 300 บาท = 1,350 บาท)
- ทุกครั้งที่เบิกต้องปรับปรุงเส้นฐาน (Scope / Schedule / งบสำรอง) และสื่อสารทีม

## ตารางบันทึกการใช้เงินสำรอง (Reserve Audit Trail)

| CR ID | รายละเอียดการเบิกใช้เงินสำรอง | อนุมัติโดย | จำนวนเงิน | งบสำรองคงเหลือ |
|---|---|---|---|---|
| Initial | งบสำรองความเสี่ยงเริ่มต้น (ที่ตั้งไว้ใน Week 7 Cost Baseline) | Sponsor | - | 2,823 THB |
| CR-02 | Export Low Stock to CSV (4.5 ชม. @ 300 บาท) | CCB Board | -1,350 THB | 1,473 THB  |
| (กรณี Defer) | เลื่อน CR-02 ไปเป็นการ์ด Task แรกของ Sprint 3 | CCB Board | 0 (ไม่เบิก) | คงเดิม (ลูกค้าใช้จดมือชั่วคราว 1 สัปดาห์) |

 เงินสำรองคงเหลือ **1,473 บาท** เก็บรักษาไว้รองรับความเสี่ยงใน **Sprint 3** ต่อไป

## งานที่ต้องทำคู่กัน (Jira & Tool Log)
- สร้างการ์ด `[CR-02] Export Low Stock Products to CSV` (Original Estimate: 4.5h) ลากเข้า Active Sprint 2; เขียน Comment กำกับว่า **"Scope increase due to CCB approval on CR-02"** พร้อมแคปเจอร์ Burndown ที่มี Scope Bump แนบรายงาน
- ตรวจสอบโควต้า GitHub Actions ไม่เกิน 2,000 นาทีฟรี/เดือน และที่เก็บไฟล์ CSV ชั่วคราวไม่กระทบค่า Cloud Server (อยู่ในโควต้าฟรี 0 THB)
