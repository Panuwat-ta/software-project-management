# บันทึกการจัดซื้อ — Procurement & Tool Log (ที่มา: ENGSE202 Week 8)

## กรอบการจัดซื้อ (ที่มา: ENGSE202 Week 8, PMBOK Procurement Performance Domain)
- **Procurement ในงานซอฟต์แวร์:** จัดหา/จัดซื้อ/บริหารสัญญาซอฟต์แวร์ เครื่องมือพัฒนา และบริการคลาวด์จากผู้ให้บริการภายนอก (SaaS Providers)
- **เป้าหมายการควบคุม:** ไม่ให้ค่าบริการเครื่องมือบานปลายจนกระทบงบรวม (Cost Baseline)
- **องค์ประกอบต้นทุน SaaS (จาก transcript):** Software Licenses (Jira Software, Trello Business, GitHub Enterprise) / Cloud Computing (AWS EC2, Google Cloud Platform, Testing DB) / CI/CD Minutes (GitHub Actions Compute Minutes สำหรับ PyTest)

## ตาราง Procurement & Tool Log (ที่มา: ENGSE202 Week 8)

| Tool / Service | Provider | Cost Model | Estimated | Actual Spent |
|---|---|---|---|---|
| Jira Software | Atlassian | Free Tier (≤ 10 Users) | 0 THB | 0 THB |
| GitHub Actions | GitHub | 2,000 Free Mins/Month | 0 THB | 0 THB |
| Cloud Database | AWS / GCP | Pay-as-you-go | 500 THB | 450 THB  |

## สถานะโควต้า/การเงิน — Workshop Step 4 (ที่มา: ENGSE202 Week 8)

| Tool Item | Quota Usage Status | Financial Status |
|---|---|---|
| Jira Software | 5 / 10 Active Users | Free Tier (0 THB) |
| GitHub Actions | 120 / 2,000 Mins Spent | Free Quota (0 THB) |
| Cloud Database | 450 / 500 THB Budget | Under Budget (+50 THB ) |

## กรณีโควต้าเกิน + Contingency Reserve (ที่มา: ENGSE202 Week 8)
- หาก GitHub Actions Compute Minutes หมดเพราะรัน PyTest บ่อยเกิน → เกิดค่าใช้จ่ายส่วนเกิน (AC > PV)
- แนวทาง PM: ทำเรื่องอนุมัติดึงงบจาก **Contingency Reserve (สัปดาห์ที่ 5)** มาจ่ายชดเชย และบันทึกสาเหตุลง Procurement Log

> หมายเหตุ: transcript ไม่ได้ระบุต้นทุนจริงอื่น (เช่น ค่าเครื่องสแกน/SDK, เวอร์ชัน Python/pytest, ยอดรวมอื่น) จึงไม่มีในเอกสารนี้
