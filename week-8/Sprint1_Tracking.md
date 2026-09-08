# การติดตามสปรินต์ที่ 1 — Active Board, Burndown & Blocker (Sprint 1 Tracking)

## Active Board & Work Log (ที่มา: ENGSE202 Week 8)
- ดึงการ์ด Refactoring เข้าช่อง **In Progress** แล้วกด **Log Work** ใส่ชั่วโมงจริง (Man-Hours)
- เส้น Burndown ขยับลงตามชั่วโมงงานที่เหลืออยู่จริง
- ส่ง Pull Request บน GitHub โดยใส่ Jira Issue Key ในชื่อ PR (ตัวอย่างจาก transcript: `ENGSE-201`) แล้วสอบทานว่า Automation ขยับการ์ด **In Progress → Code Review** อัตโนมัติ
- หลัก Governance: Transparency (งาน+ชั่วโมงจริงบนบอร์ด) / Inspection (ส่อง Burndown) / Adaptation (เคลียร์ Blocker ใน Daily Standup)
- สิ่งส่งมอบ: ภาพแคปเจอร์ Sprint Burndown Chart บน Jira + รายงาน Work Log

## Burndown Chart — แกนและเส้น (ที่มา: ENGSE202 Week 8)
- แกน X: วันทำงานใน Sprint (เช่น Day 1 ถึง Day 10)
- แกน Y: ปริมาณงานที่เหลือ (Man-Hours หรือ Story Points)
- **Ideal Burndown Line:** เส้นตรงอุดมคติจากงานรวมลงสู่ 0
- **Actual Burndown Line:** เส้นจริงขยับตามการกด Log Work

## รูปแบบ Burndown 3 แบบ (ที่มา: ENGSE202 Week 8)
1. **Ahead of Schedule ** — เส้น Actual อยู่ใต้ Ideal Line → ปิดงานเร็วกว่าแผน (ประสิทธิภาพสูงหรือเผื่อเวลามากไป)
2. **Behind Schedule ** — เส้น Actual อยู่เหนือ Ideal Line → ล่าช้ากว่าแผน เสี่ยงปิด Sprint ไม่ทัน ต้องหาสาเหตุ Blocker
3. **Scope Increase ** — เส้น Actual พุ่งสูงขึ้นกลาง Sprint → มีงานแทรกกลางคัน หรือประมาณเวลาเพิ่มจาก Change Request

> หมายเหตุ: ไม่มีการระบุตัวเลขรายวัน (actual/ideal รายวัน, story points รวม, capacity ชั่วโมง) ใน transcript จึงไม่มีตารางตัวเลขรายวันในเอกสารนี้

## การจัดการ Blocker / Jira Flag (ที่มา: ENGSE202 Week 8)
- **Blocker คือ:** ปัญหาหรือความเสี่ยงที่เกิดจริงแล้วทำให้สมาชิกทำต่อไม่ได้
- **ตัวอย่างจาก transcript:** ติดขัดเพราะไร้ Mock Data / รอ Peer Review บน GitHub นานเกิน 24 ชม.
- **บทบาท PM ใน Daily Standup:** บันทึกลง Impediment Backlog แล้วรีบเข้าช่วยปลดล็อกเพื่อรักษาสปีดทีม
- **Jira Flagging:** กด **Add Flag** บนการ์ด → การ์ดเปลี่ยนเป็นสีแดง/เหลือง มีสัญลักษณ์ธงเด่นบน Active Board → PM เข้าเคลียร์
- **ข้อบังคับ:** ต้องใส่ Comment ระบุสาเหตุและชื่อผู้ที่ต้องเข้าช่วย

## Refactoring ที่ถูกติดตามบนบอร์ดนี้ (ที่มา: ENGSE225 Week 8)
- Branch ปฏิบัติการ: `feature/refactor-core-architecture`
- 4 เทคนิค Fowler: Rename Variable/Method, Extract Function, Extract Class, Encapsulate Field
- กฎเหล็ก: รักษา PyTest ไฟเขียว 100% ตลอดกระบวนการ (Baseline: `pytest test_app.py` ต้อง `1 passed` ก่อนแตะโค้ด; แก้ทีละน้อยแล้วรัน pytest ซ้ำทันที; ไฟแดงให้ `git checkout` ถอยกลับ; ห้ามเพิ่มฟีเจอร์ใหม่ตอน Refactor)
