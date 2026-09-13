# รายงาน EVM ฉบับสุดท้าย — ระบบสินค้าคงคลัง (สัปดาห์ที่ 12 ข้อมูลสมมติเพื่อการเรียน)

อ้างอิง: ENGSE202 Week 12 (PMBOK 7th, EVM, Procurement Close-out)
ตัวเลขทั้งหมดด้านล่างเป็นตัวเลขสมมติเพื่อใช้ในการเรียน ไม่ใช่ต้นทุนโครงการจริง
กรอบ: เฟสพัฒนา Sprint 1–3 (S1: Refactoring + Velocity ตั้งต้น, S2: CR-01/CR-02 + CCB,
S3: Hardening + Cross-Team UAT + Final Docs)

## 1. ตัวเลขสุดท้าย (Final EVM รวม 3 Sprints)

| ตัวแปร EVM | รายละเอียด | มูลค่า / ดัชนีสรุป |
|-----------|-----------|-------------------|
| Planned Value (PV) | งบประมาณแผนงานรวมทั้งหมด (รวม CR-02) | 15,525 THB |
| Earned Value (EV) | มูลค่างานที่ผ่าน DoD & UAT ครบ 100% | 15,525 THB |
| Actual Cost (AC) | ค่าแรงจริงจาก Log Time + ค่าใช้จ่ายเครื่องมือจริง | 16,100 THB |
| Schedule Index (SPI = EV / PV = 15,525 / 15,525) | ตรงตามแผน | 1.00 (On-Time 100% ) |
| Cost Index (CPI = EV / AC = 15,525 / 16,100) | เกินงบ | 0.96 (Over 3.7% ) |
| Cost Variance (CV = EV − AC = 15,525 − 16,100) | ชดเชยงบสำรอง | −575 THB |
| Schedule Variance (SV = EV − PV) | ตรงเวลา | 0 |

## 2. การตีความ

- **ด้านกำหนดการ:** SPI 1.00 (SPI ≥ 1.0 = เร็วกว่าหรือตรงตามแผน ) — ส่งมอบตรงตามกำหนด 100%
  UAT SC01–SC03 ปิดครบในสัปดาห์ที่ 12
- **ด้านต้นทุน:** CPI 0.96 (CPI < 1.0 = ใช้เงินเกินงบ /) — เกินงบ 3.7%
  ชดเชยด้วยงบสำรอง Contingency Reserve ตามเกณฑ์อนุมัติ
  (เบิกค่าแรงส่วนเกิน Refactoring 575 THB)

## 3. แนวโน้มความเร็ว (Velocity Trend — story points / sprint)

| Sprint | Velocity | ช่วงงาน |
|--------|----------|---------|
| S1 | 15 | ช่วงผ่าตัดโค้ดเดิม (Refactoring) |
| S2 | 22 | ช่วงความเร็วพัฒนาสูงสุด (CR-01/CR-02) |
| S3 | 12 | ช่วง Hardening & UAT |

Epic Burndown: การ์ดงานย่อยทั้งหมดถูก Burned down แตะระดับ 0 ไร้งานคั่งค้าง —
Epic 1 (Refactoring) ปิดงานโครงสร้างคลาส 100%,
Epic 2 (Evolution) ปิดงาน Barcode, Alert, CSV

## 4. การปิดงานจัดซื้อจัดจ้าง (Procurement Close-out)

### 4.1 ตารางกระทบยอดค่าใช้จ่ายเครื่องมือ (Final Reconciliation Sheet)

| Tool / Service Item | Budget Allocated | Actual Incurred | Variance | Contract Status |
|---------------------|-----------------|-----------------|----------|-----------------|
| Jira Software (Cloud) | 0 THB | 0 THB | 0 THB | Free Tier / Closed |
| GitHub Actions Mins | 0 THB | 0 THB | 0 THB | 1,420 / 2,000 Mins (Free) |
| Cloud Server Hosting | 500 THB | 480 THB | +20 THB  | Active / Decommissioned |
| SSL & Domain Cert | 300 THB | 300 THB | 0 THB | Paid & Settled |
| รวมยอดค่าเครื่องมือจริง | 800 THB | 780 THB | +20 THB  | ปิดสัญญาสมบูรณ์  |

### 4.2 กระทบยอดเงินสำรองความเสี่ยง (Contingency Settlement)

- งบสำรองความเสี่ยงตั้งต้น (Week 7 Cost Baseline): +2,823 THB
- เบิกจ่ายคำขอฉุกเฉิน CR-02 (Week 10): −1,350 THB
- เบิกจ่ายค่าแรงส่วนเกิน Refactoring (W12): −575 THB
- เงินสำรองคงเหลือสุทธิ = 898 THB (0.00 THB Deficit )
  — อยู่ในกรอบงบที่อนุมัติ 100% ไม่ต้องขอเงินเพิ่ม

### 4.3 ยกเลิกทรัพยากรคลาวด์ส่วนเกิน (Decommissioning)

- ปิด (Terminate) ฐานข้อมูลทดสอบชั่วคราว
- ปิด Mock Server ที่ใช้ในการรัน PyTest
- คงไว้เฉพาะ Production Server และ GitHub หลัก

## 5. การปิด Sprint 3 และการขอ Sign-off

1. ตรวจว่าการ์ด TASK-301 (UAT), TASK-302 (Security), TASK-303 (Docs) อยู่ช่อง Done ครบ
   แล้วกด Complete Sprint 3 บน Jira
2. ดึงหลักฐาน Velocity Chart (Commitment vs Completed 3 Sprints)
   และ Epic Burndown (แตะ 0) ใส่เล่มรายงาน
3. PM นำเล่ม Final EVM + Velocity + Procurement Sheet + ใบรับรอง UAT
   เข้าพบอาจารย์ (Sponsor) ลงนาม Phase 3 Completion Certificate
   (Deliverables: Refactored Layered Architecture, Barcode, Reorder Alerts,
   CSV Export, Full CI/CD — 25 tests ผ่าน 100%, Tag v2.0.0-evolution)
