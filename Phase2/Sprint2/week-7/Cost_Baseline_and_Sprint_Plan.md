# ต้นทุนงบประมาณ (Cost Baseline) และแผนงาน Sprint 1

เอกสารนี้รวบรวมต้นทุนของทีมพัฒนา 3 คน สำหรับช่วง Refactoring และการวางระบบใหม่

## 1. ตารางสรุปงบประมาณสุทธิ (Master Financial Statement - Cost Baseline)

อิงจากข้อมูลบทบาทในทีม: Project Manager/Developer, QA/Tester, Tech Lead/Architect

| หมวดหมู่ต้นทุน (Cost Breakdown Category) | สัดส่วน | จำนวนเงิน (บาท) |
| :--- | :--- | :--- |
| **1. ค่าแรงงานทางตรง (Direct Labor Cost)** (งาน Refactoring + ทดสอบระบบ) | 80.0% | 15,000 |
| **2. โครงสร้างพื้นฐานและเครื่องมือ (Infrastructure & Tooling)** (Cloud & Services) | 5.0% | 1,000 |
| **รวมต้นทุนทางตรง (Subtotal Direct Cost)** | **85.0%** | **16,000** |
| **3. งบสำรองเผื่อฉุกเฉิน (Contingency Reserve)** (15% เพื่อรับมือโค้ด Legacy พัง) | 15.0% | 2,823 |
| **ยอดรวมงบประมาณที่อนุมัติ (Total Approved Budget Baseline)** | **100.0%** | **18,823** |

## 2. เกณฑ์การแจ้งเตือนผลต่างงบประมาณ (Cost Variance Thresholds)

ผู้จัดการโครงการจะใช้ Earned Value Management (EVM) เฝ้าระวังงบประมาณบานปลายจากการแก้บั๊ก:
- **ปกติ (Variance 0 - 5%)**: ดำเนินการต่อตามแผน
- **แจ้งเตือน (Variance > 5% - 10%)**: Project Manager (PM) ประชุมทีมเพื่อหาแนวทางลดเวลาแก้บั๊ก
- **วิกฤต (Variance > 10%)**: ต้องพิจารณาตัดฟีเจอร์ย่อย (Scope Reduction) เช่น ยกเลิกระบบ Platinum Member ชั่วคราว หรือต้องดึงเงินจาก **งบสำรอง** ออกมาใช้

## 3. การวางแผนความจุทีมใน Sprint 1 (Sprint 1 Capacity Planning)

**เป้าหมายของ Sprint 1**: สร้างระบบ Member System และเปลี่ยนฐานข้อมูลจาก JSON เป็น SQLite ตามเป้าใน `README.md`
**ระยะเวลา**: 2 สัปดาห์

### การคำนวณกำลังการผลิตของทีม (Team Capacity Calculation)
- **จำนวนสมาชิกทีม**: 3 คน (PM/Dev, QA, Tech Lead)
- **เวลาว่างของแต่ละคน**: 6 ชั่วโมง / สัปดาห์
- **ความจุรวมของ Sprint (Total Capacity)**: 3 คน * 6 ชั่วโมง * 2 สัปดาห์ = **36 Man-Hours**

### กฎการรับงานใน Sprint (Backlog Rules)
งานทั้งหมด (Task Cards) ที่ดึงมาทำใน Sprint 1 จะต้อง:
1. ชัดเจนตามเงื่อนไข **DoR** ใน Communication Matrix
2. ถูกประเมินเวลา (Original Estimate) เป็นชั่วโมง โดยรวมกันทั้งหมดห้ามเกิน **36 Man-Hours** โดยเด็ดขาด
3. งานเขียนโค้ดมอบให้ Developer, งานเขียนเทสต์มอบให้ QA, งานรีวิวและตรวจสอบสถาปัตยกรรมมอบให้ Tech Lead
