# เมทริกซ์ผู้มีส่วนได้ส่วนเสีย — Current (C) vs Desired (D) + CR-01 (Stakeholder Matrix)

## คำนิยามและกลุ่ม (ที่มา: ENGSE202 Week 8)
- **Stakeholder คือ:** บุคคล/กลุ่ม/องค์กรที่มีผลกระทบหรือได้รับผลกระทบจากการตัดสินใจและผลลัพธ์ของโครงการ (อ้างอิง PMBOK 7th, Stakeholder Engagement Performance Domain)
- **Sponsor / อาจารย์:** ต้องการงานเสร็จตามงบ เวลา และสเปก
- **Tech Lead / Devs:** ต้องการโค้ดสะอาด ลดหนี้ทางเทคนิค
- **End-Users:** ต้องการฟีเจอร์ใหม่ที่ใช้งานง่าย ไร้บั๊ก

## ระดับการมีส่วนร่วม 5 ระดับ (ที่มา: ENGSE202 Week 8)
1. **Unaware** — ไม่ทราบถึงการมีอยู่หรือผลกระทบโครงการ
2. **Resistant** — ทราบเรื่องแต่ต่อต้าน ไม่เห็นด้วย
3. **Neutral** — ทราบเรื่องแต่ไม่แสดงท่าทีหนุนหรือค้าน
4. **Supportive** — ทราบเรื่องและพร้อมหนุนให้สำเร็จ
5. **Leading** — มีส่วนร่วมเข้มข้น ผลักดันโครงการ

## เมทริกซ์ C vs D (ที่มา: ENGSE202 Week 8 — ตาราง Matrix Structure + Workshop Step 3)

| ผู้มีส่วนได้ส่วนเสีย (Stakeholder) | ปัจจุบัน (Current, C) | ที่ต้องการ (Desired, D) | กลยุทธ์รับมือ CR-01 (จาก transcript) |
|---|---|---|---|
| Sponsor (อาจารย์) | Supportive | Leading | รายงาน Impact Analysis |
| Tech Lead (ทีมงาน/เพื่อนในทีม) | Leading | Leading | จัดสรร Refactoring |
| End-User (ผู้ใช้/ผู้ใช้สมมุติ) | Resistant | Supportive | สาธิตฟีเจอร์ Barcode |

## การทูต CR-01 (ที่มา: ENGSE202 Week 8)
- **ห้ามทำ:** ยอมรับทันทีโดยไม่ประเมิน (ทีม Overwork, Sprint ล้ม) / ปฏิเสธลูกค้ารุนแรงทันที (Stakeholder กลายเป็น Resistant)
- **แนวทางมืออาชีพ:** ใช้ Impact Analysis Form จากฝั่ง Maintenance ชี้แจงผลกระทบเวลา/งบอย่างมีเหตุผล แล้วนำ CR-01 ไปจัดลำดับใส่ **Sprint 2** (ไม่แทรกกลาง Sprint 1)
- **ทางเลือกที่สื่อสารกับ Sponsor** (ผ่าน Communication Matrix): ทำ CR-01 ใน Sprint 2 โดยขยายงบจาก **Contingency Reserve** หรือตัด Scope งานที่ไม่สำคัญออก
- ข้อมูล Impact ที่ใช้ชี้แจง (จาก transcript): เพิ่ม **8 Man-Hours**, กระทบ **2 Class (Product, Repo)**, เขียน PyTest เพิ่ม **3 Cases**

> หมายเหตุ: transcript ไม่ได้ระบุชื่อบุคคลจริง บทบาทอื่นนอกเหนือจาก 3 แถวข้างต้น หรือตัวเลขเพิ่มเติม จึงไม่มีในเอกสารนี้
