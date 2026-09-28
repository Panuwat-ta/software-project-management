# รายงานตรวจสอบ Pre-Final ทั้ง 2 วิชา

ตรวจทานวันที่ **27 กันยายน 2026** เทียบคำตอบกับโจทย์ต้นฉบับ เอกสารรายสัปดาห์ที่เกี่ยวข้อง และเอกสารปฐมภูมิสำหรับมาตรฐาน/แนวคิดที่มีความเสี่ยงต่อการตีความ

**ผลตรวจ:** คำตอบครอบคลุมโจทย์ครบ **20 ข้อ วิชาละ 10 ข้อ** สูตรและผลคำนวณที่ตรวจซ้ำถูกต้อง หลังปรับตัวอย่างโค้ด เกณฑ์ทดสอบและแผนภาพตามรายการด้านล่าง ยังต้องยึดเกณฑ์ให้คะแนนของผู้สอน โดยเฉพาะระดับการนับ CFG และกติกาของกรณีศึกษา

## สิ่งที่ปรับในรอบตรวจนี้

| ตำแหน่ง | ประเด็นที่ตรวจพบ | การปรับ |
|---|---|---|
| ENGSE225 A2 | ตัวอย่าง test และ deserializer ต้องใช้ Product ที่เพิ่มฟิลด์แล้ว แต่รุ่นใน A1 ยังไม่มีฟิลด์นั้น | เพิ่ม Product รุ่น CR-01 พร้อม default และ `is_low_stock()` ให้ตัวอย่างใน A2 ประกอบกันแล้วรันได้ |
| ENGSE225 A5 | หมายเหตุเดิมยังไม่ยืนยันความคลาดเคลื่อนของเลขข้อ “8.4: Maintenance Records” ในโจทย์ | ตรวจสารบัญฉบับ 2006 และระบุชัดว่าไม่พบหัวข้อนี้; แยก Dossier สามภาคของรายวิชาออกจากข้อกำหนดมาตรฐาน |
| ENGSE202 B4 | เกณฑ์ latency เดิมวัดเฉพาะคำขอสำเร็จ แต่ยังไม่มีขั้นต่ำของ success rate และช่วงทดสอบ | เพิ่ม success ≥99.9%, warm-up/ระยะวัด/load profile และให้รายงาน error/timeout ของคำขอที่ถูกต้องทั้งหมด |
| ENGSE202 B5 | ข้อความกล่าวถึงการถอน/ปฏิเสธคำขอคืนสินค้า แต่แผนภาพยังไม่มีทางออกจาก Returning สำหรับกรณีดังกล่าว | เพิ่ม transition กลับ Shipped/Delivered ตามสถานะพัสดุจริงและ guard ว่ายังไม่อนุมัติ refund พร้อมการจัดการข้อพิพาท/สินค้าที่อยู่คลัง |

เพิ่มแหล่งอ้างอิงคู่มือ ISO/IEC 29110 Basic Profile และค่าเฉลี่ยอ้างอิง SUS รวมทั้งปรับถ้อยคำ ROI ไม่ให้สรุปเจตนาของผู้เขียนสไลด์จากตัวเลขเพียงอย่างเดียว

## ผลตรวจรายข้อ

| วิชา/ข้อ | สิ่งที่ตรวจ | ผลและข้อควรใช้ให้ตรงบริบท |
|---|---|---|
| ENGSE225 A1 | Refactoring, Extract Function/Class, encapsulation, DI และ safety net | ตอบครบ; แยก DI จาก Introduce Parameter Object และรักษาพฤติกรรมเดิมขณะ refactor |
| ENGSE225 A2 | CR workflow, TDR, RCA และ legacy fallback | ตอบครบ; default barcode ว่าง/reorder point 5 และเงื่อนไข quantity ≤ threshold ตรง Week 9–10 |
| ENGSE225 A3 | Atomic write และ Code Freeze | ถูกต้อง; แยก atomicity/durability และไม่รับรองปลอดภัย 100% จากทุกเหตุการณ์ |
| ENGSE225 A4 | System Test/UAT, scope และ SemVer/tag | ถูกต้อง; MAJOR ขึ้นกับ public API ที่ incompatible และ suffix `-evolution` เป็น pre-release ตาม SemVer |
| ENGSE225 A5 | Clean environment, Smoke/Regression และ Dossier | ตอบครบ; สามภาคมาจากบทเรียน และแก้หมายเหตุเลขข้อ ISO แล้ว |
| ENGSE225 B1 | CFG, V(G), basis paths และ discount outputs | N=13, E=19, V=8 ตาม short-circuit; มี 8 normal paths และ test ครบทั้ง 8 |
| ENGSE225 B2 | Dummy/Stub/Mock/Fake และ integration strategy | ถูกต้อง; doubles ไม่แทนการพิสูจน์ integration กับ adapter จริง |
| ENGSE225 B3 | Test Pyramid, CI workflow และ quality gates | ตอบครบ; 70/20/10 เป็นตัวอย่าง ส่วน coverage ≥90% ยึดเกณฑ์รายวิชา |
| ENGSE225 B4 | SI V&V และ review/traceability checklist | สอดคล้องระดับกิจกรรม/work product; ไม่อ้างเลข task ที่ไม่ได้ตรวจจากมาตรฐานฉบับเต็ม |
| ENGSE225 B5 | Density/churn/pass rate และ SUS | สูตรถูกต้อง; ตัวอย่าง SUS=75 และแยกค่าเฉลี่ย 68 ออกจากเกณฑ์ acceptability ประมาณ >70 |
| ENGSE202 A1 | Burndown 3 สภาวะและการปลด Blocker | กราฟและการตีความสอดคล้อง; ตรวจ DoD/issue history ประกอบ ไม่สรุปจากกราฟอย่างเดียว |
| ENGSE202 A2 | SV/CV และ Review/Retro | SV=−1,000, CV=−1,200; reserve รองรับเงินได้ตามอำนาจอนุมัติ แต่ไม่ลบ variance |
| ENGSE202 A3 | Scope Creep, Iron Triangle, CCB และ reserve log | ตอบครบ; 675 บาทเป็นกรณีแยก Week 10 ไม่ใช่ยอดต่อเนื่องหลังเบิก 1,200 บาท |
| ENGSE202 A4 | CFD, Little’s Law, Burnup และ freeze | ถูกต้อง; WIP/throughput ต้องใช้ขอบเขตเดียวกัน และ WIP limit ไม่รับประกัน lead time ลดเอง |
| ENGSE202 A5 | CPI/SPI, closure และ ROI | CPI≈0.9643; ROI≈63.975% ปัดหนึ่งตำแหน่งเป็น 64.0%; SPI=1 ตอนจบไม่พิสูจน์ว่าส่งตรงเวลา |
| ENGSE202 B1 | NFR, TPS/concurrency และ payment timeout | ตอบครบ; 99.95% แบบเวลาใน 30 วันคือ downtime 21.6 นาที; timeout คือ unknown ต้อง reconcile |
| ENGSE202 B2 | RTM และ impact ของ Biometric+TOTP | ตอบครบทั้ง scope/schedule/cost/debt; 18,400 บาทเป็นสมมุติฐาน และต้องควบคุม replay/recovery |
| ENGSE202 B3 | MoSCoW และ negotiation flow | ตอบครบ; นโยบายให้ข้อมูลภาษีเป็นสมมุติฐานที่ต้องยืนยัน ไม่ใช่ข้อสรุปกฎหมาย |
| ENGSE202 B4 | Requirement V&V, ambiguity, testability, traceability | ตอบครบ; เพิ่มเกณฑ์ความสำเร็จ/โหลดเพื่อให้ performance requirement ตรวจรับได้ชัดขึ้น |
| ENGSE202 B5 | Order states, guards, cancellation/return/refund | ครบ 8 สถานะโจทย์และสถานะเสริม; รอผล refund ก่อน Refunded และเติมทางออกจาก Returning แล้ว |

## การตรวจด้วยโปรแกรม

- เทียบข้อความโจทย์ทั้งหมดกับต้นฉบับหลังละเว้นช่องว่างและเครื่องหมายจัดรูปแบบ: **ครบ 10 ข้อต่อวิชา**
- ตรวจ syntax ของ Python ทุก code block และรันตัวอย่างคำนวณมูลค่าคลัง: **ผ่าน**
- รันทดสอบ low-stock ที่ quantity 3/5/6 เทียบ threshold 5 และโหลด row ที่ไม่มี barcode/reorder_point: **ผ่าน**
- รัน atomic save กรณีสำเร็จ, serialize ล้มเหลว และ `os.replace` ล้มเหลวก่อนเปลี่ยนไฟล์: **ผ่าน** โดยกรณีผิดพลาดไฟล์เดิมยังอยู่และไม่เหลือ temporary file การตรวจนี้ไม่ได้จำลองไฟดับจริงหรือรับรอง hardware durability
- รัน discount ทั้ง 8 test cases: **ผ่าน**; นับ CFG และตรวจ rank ของ path vectors ได้ 8 ยืนยันว่าเส้นทางที่ใช้เป็นอิสระกัน
- ตรวจ SV/CV/CPI/SPI, ค่าแรง CR, reserve, ROI/payback, availability, Burnup และ SUS: **ผ่าน**
- ตรวจลิงก์ไฟล์ในเอกสารและ code fences: **ผ่าน**

ตัวเลขที่ตรวจซ้ำ ได้แก่ CR ตามอัตราเฉลี่ย **1,350 บาท**, CR ตามอัตราแต่ละบทบาท **1,475 บาท**, reserve กรณีแยก **675 บาท**, reserve เมื่อเบิก 1,200 ต่อเนื่องแล้ว **ขาด 525 บาท**, Burnup **93.103%**, payback สมมุติ **7.318 เดือน** และ SUS **75**

แผนภาพ Mermaid ตรวจตรรกะและข้อความ transition; ไม่ได้รัน payment gateway/Jira/ระบบคำสั่งซื้อจริง และผลข้างต้นไม่ใช่การรับรองว่าซอฟต์แวร์ production ผ่านเกณฑ์เหล่านี้

## ประเด็นในโจทย์/สไลด์ที่ต้องแยกจากหลักวิชาการ

1. **ISO/IEC 14764:** ไม่พบ “8.4: Maintenance Records” ใน [สารบัญฉบับ 2006](https://preview.sist.si/sist-preview/39064/a132a6efa20e47d69ede63804b88a170/ISO-IEC-14764-2006.pdf) จึงไม่ควรท่องเลขข้อนี้เป็นข้อเท็จจริงของมาตรฐาน
2. **SemVer:** refactoring ใหญ่ไม่เพียงพอให้เพิ่ม MAJOR หาก public API ยัง compatible; `-baseline`/`-evolution` เป็น pre-release identifiers ตาม [SemVer 2.0.0](https://semver.org/)
3. **Scrum:** Sprint มี timebox คงที่ การขยายวันจบตามสไลด์เป็นกติกาแบบ hybrid ไม่ใช่ Scrum แบบเคร่งครัด ดู [Scrum Guide](https://scrumguides.org/scrum-guide.html)
4. **เงินสำรอง:** ตัวอย่าง Week 9, 10 และ 12 ต้องกระทบยอดก่อนถือว่าใช้บัญชีเดียวกัน และเงินสำรองที่รวม baseline แล้วไม่ควรถูกนับเป็นงบเพิ่มซ้ำ
5. **ROI:** ผลจากตัวเลขที่ให้คือ 63.975% จึงเป็น 64.0% เมื่อปัดหนึ่งตำแหน่ง; ตัวเลขนี้อิงผลประโยชน์สมมุติในสไลด์ ยังไม่ใช่ benefits realization ที่วัดจริง
6. **Path coverage:** V(G)=8 ใช้กราฟแยก short-circuit; V(G)=6 ใช้กราฟรวม compound conditions การเลือกต้องสอดคล้องกับกราฟและเกณฑ์ผู้สอน ส่วน basis coverage ไม่เท่ากับ all-path coverage สำหรับทุกโปรแกรม

## เปิดคำตอบฉบับตรวจทาน

- [ENGSE225 — โจทย์และคำตอบ](</home/panuwat/work/software-project-management/work/Pre-Final/Answers/ENGSE225-Pre-Final-Answers.md>)
- [ENGSE202 — โจทย์และคำตอบ](</home/panuwat/work/software-project-management/work/Pre-Final/Answers/ENGSE202-Pre-Final-Answers.md>)
- [สารบัญและแหล่งเอกสารรายสัปดาห์](</home/panuwat/work/software-project-management/work/Pre-Final/Answers/README.md>)
