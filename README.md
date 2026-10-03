# Software Evolution and Maintenance & Software Project Management

---

## สมาชิกในโครงการและบทบาทหน้าที่ (Project Members & Roles)

| ชื่อ-นามสกุล (Name)          | รหัสนักศึกษา (Student ID) | บทบาทหน้าที่ความรับผิดชอบ (Key Responsibilities)                                                                                                                                                                                                                                                                               |
| :------------------------ | :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **นาย ภานุวัฒน์ ต๋าคำ**        | 6754210044-3           | **Project Manager / Developer**<br>- บริหารจัดการภาพรวมโครงการ กำหนดกรอบเวลา (Timeline) และจัดการงานในแต่ละช่วง<br>- ติดตามความคืบหน้าของทีม ประสานงาน และจัดการอุปสรรคต่าง ๆ ของทีมพัฒนา<br>- ดำเนินการปรับปรุง แก้ไขบั๊ก และพัฒนาระบบตามที่ Tech Lead มอบหมาย<br>- เขียนโค้ดในส่วนของการดักจับข้อผิดพลาด (Input Validation) และการจัดเก็บข้อมูลให้มีความเสถียร |
| **นาย เอกพันธ์ ทศทิศรังสรรค์** | 67543210050-0           | **QA / Tester**<br>- ออกแบบกรณีการทดสอบ (Test Cases) ครอบคลุมการทำงานทั่วไปและเคสขอบเขตที่เป็นอันตราย (Edge Cases)<br>- จัดทำเอกสารชุดทดสอบและทำ Automated Unit Testing เพื่อยืนยันคุณภาพของระบบ                                                                                                                                            |
| **นาย ณฐภาพ สายหล้า**      | 67543210054-2           | **Tech Lead / Architect**<br>- ออกแบบแนวทางการปรับโครงสร้างโค้ด (Refactoring Architecture)<br>- ตรวจสอบคุณภาพของโค้ด (Code Review) และกำหนดแนวทางเขียนโค้ดที่ถูกต้องตามมาตรฐาน (PEP 8)                                                                                                                                                |

---

## Workspace Links
* **[Project Website](http://panuwat.me/software-project-management/)** - เว็บไซต์นำเสนอโครงการ
* **[Trello Board](https://trello.com/b/bsc6WHDT)** - กระดานติดตามสถานะการดำเนินงาน
* **[draw.io](https://drive.google.com/file/d/1tFYndnVNnFhFePMNs_YaC3N4-rA2QI3y/view?usp=sharing)** - diagram

## โครงสร้างโฟลเดอร์ของโครงการ (Repository Directory Structure)

```text
.
├── Phase1/        # เริ่มโครงการ+วางฐาน (W1-4): week-1…4, proposal/, templates/
├── Phase2/        # ออกแบบ+ต้นทุนฐาน (W5-7): week-5…7
├── Phase3/        # ลงมือ+คุมเปลี่ยนแปลง (W8-11): week-8…11
├── Phase4/        # UAT+ปล่อย v2.0 (W12): week-12, sprint1.*, app.py/test_app.py (v2.0)
├── Phase5/        # วิวัฒนาการ (Sprint 2+3): sprint2.* / sprint3.*, SPM-23…32,
│   #                app.py/test_app.py (v3.0), web/ + web-plan.md
├── app.py         # โค้ดหลัก v3.0 (SQLite + Member + Checkout)
├── test_app.py    # ชุดทดสอบ 14 เคส
├── doc/           # เอกสารเพิ่มเติม (app.md, test.md)
├── work/          # transcript บรรยายรายสัปดาห์
├── index.html     # พอร์ทัลเว็บหลัก (Phase 1-5)
└── README.md      # ไฟล์ปัจจุบัน
```

แต่ละ Phase มี `README.md` + `phaseN-report.md` ของตัวเอง

---

## ขอบเขตการวิวัฒนาการระบบ (Evolution & Refactoring Goals)

1. **Refactoring and Clean Code (การปรับปรุงโครงสร้างโค้ด)**
   - ปรับชื่อตัวแปรทั้งหมดให้เป็นไปตามมาตรฐาน PEP 8 (เปลี่ยนอักษรตัวเดียวเป็น snake_case ที่มีความหมายชัดเจน)
   - แยกตรรกะทางธุรกิจ (Business Logic) ออกจากส่วนแสดงผล CLI UI (CLI Presentation Layer)
   - ปรับโครงสร้างลูปเงื่อนไขที่ซ้ำซ้อนในขั้นตอนการบันทึกและแก้ไขข้อมูลสินค้า

2. **Stability and Security (เสถียรภาพและความปลอดภัย)**
   - ป้องกันระบบ Crash จากการกรอกข้อมูลผิดประเภท (เช่น ตัวอักษรปนในช่องตัวเลข) ด้วย Try-Except Validation
   - ล็อกป้องกันค่าติดลบในส่วนข้อมูลราคาสินค้า จำนวนสินค้า และการตัดของออก (Prevent Negative Input)
   - พัฒนาการบันทึกข้อมูล SQLite ด้วย Parameterized Query เพื่อป้องกันช่องโหว่ SQL Injection 100%

3. **Evolution - SQLite Database & Member System (ระบบสมาชิกและการเปลี่ยนผ่านฐานข้อมูล)**
   - ทำการย้ายฐานข้อมูลหลักจากไฟล์ JSON ไปยังระบบฐานข้อมูล SQLite เพื่อความทนทานของข้อมูลและสนับสนุน Transactions (Commit/Rollback)
   - สร้างโมดูลสมาชิกและระบบลดราคา (Membership Tiers): Regular (0%), Silver (5%), Gold (10%), Platinum (15%)
   - พัฒนาระบบ Checkout Flow ที่คิดคำนวณส่วนลดสมาชิกอัตโนมัติ พร้อมใบเสร็จชี้แจงค่าบริการย่อยอย่างละเอียด

4. **QA and Automated Testing (การประกันคุณภาพและการตรวจสอบ)**
   - เขียนสคริปต์ Unit Test เพื่อทดสอบตรรกะหลักของคลังสินค้า เช่น สูตรคำนวณมูลค่ารวมสินค้าคงคลัง และการจ่ายตัดสต็อก
   - เขียนสคริปต์ทดสอบการคำนวณส่วนลดสมาชิกในระดับ Tier ต่างๆ
   - เขียนสคริปต์ทดสอบระบบความปลอดภัยฐานข้อมูลจากการโจมตีประเภท SQL Injection

---

## คำสั่งที่ใช้บ่อย (Commands)

```bash
# ติดตั้งแพ็กเกจ
pip install -r requirements.txt

# รันชุดทดสอบทั้งหมด (CLI 14 + Web API 6 = 20 เคส)
pytest

# รันเว็บ (Backend FastAPI + Frontend แบบ responsive)
PYTHONPATH=Phase5/Sprint5 uvicorn web.backend.main:app --reload
# เปิด http://127.0.0.1:8000/  ·  API docs ที่ /docs

# สร้างหน้า HTML จากรายงาน Markdown (Phase/Sprint ทั้งหมด)
python3 tools/build_reports.py

# ตรวจว่า HTML ที่ commit ไว้ตรงกับ Markdown (ใช้ใน CI)
python3 tools/build_reports.py --check

# ตรวจสไลด์หลักฐานทุกสัปดาห์
python3 Phase1/Sprint1/templates/verify_evidence_decks.py

# ตรวจคุณภาพโค้ด
flake8 app.py Phase5/Sprint5/web/backend/ tools/
bandit -q -r app.py Phase5/Sprint5/web/backend/
```
