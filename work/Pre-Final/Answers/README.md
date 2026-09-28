# Pre-Final ทั้ง 2 วิชา — โจทย์พร้อมแนวคำตอบ

อ่านเอกสารต้นทางใน `work` ครบ 34 ไฟล์: บทเรียน 30 ไฟล์ (วิชาละ 15 สัปดาห์), ข้อสอบ 3 ไฟล์ และดัชนีลิงก์ `work.md` จัดทำเฉลยจากไฟล์ข้อความที่มีในเครื่อง โดยใช้เอกสารปฐมภูมิเสริมสำหรับประเด็นที่ต้องตรวจความแม่นยำ ไม่ได้เปิด Google Slides ทุกลิงก์ซ้ำแทนไฟล์ข้อความ

## เปิดอ่านเฉลย

- [ENGSE225 — Software Evolution and Maintenance: 10 ข้อ](</home/panuwat/work/software-project-management/work/Pre-Final/Answers/ENGSE225-Pre-Final-Answers.md>)
- [ENGSE202 — Software Project Management: 10 ข้อ](</home/panuwat/work/software-project-management/work/Pre-Final/Answers/ENGSE202-Pre-Final-Answers.md>)
- [รายงานตรวจสอบความถูกต้องครบ 20 ข้อ](</home/panuwat/work/software-project-management/work/Pre-Final/Answers/Verification.md>)

แต่ละวิชามีส่วน A ข้อสอบหลัก 5 ข้อ และส่วน B ข้อสอบเพิ่มเติม 5 ข้อ รวม **20 ข้อ** ทุกข้อมีโจทย์ต้นฉบับและคำตอบตามคำถามย่อย พร้อมโค้ด ตาราง วิธีคำนวณ หรือแผนภาพตามโจทย์ ไฟล์ต้นฉบับยังคงเดิม ไม่ได้นำคำถามที่ซ้ำในไฟล์รวมมานับเพิ่ม

แผนภาพ CFG, CI, Sequence และ State Machine ใช้ Mermaid จึงควรเปิดด้วย Markdown viewer ที่รองรับ Mermaid; กราฟ Burndown เป็นภาพ SVG ในโฟลเดอร์ `assets`

## ข้อสังเกตที่อธิบายไว้ในเฉลย

- Atomic replace ลดความเสี่ยงไฟล์เขียนค้าง แต่ไม่รับประกันความปลอดภัย 100% จากทุกสาเหตุ
- SemVer เพิ่ม MAJOR เมื่อสัญญาการใช้งานที่ประกาศไม่ compatible ไม่ใช่เพียงเพราะ refactoring ใหญ่
- ฟังก์ชันส่วนลดมี V(G)=8 เมื่อแยก short-circuit หรือ 6 เมื่อใช้กราฟรวม compound conditions; เฉลยระบุกราฟและวิธีนับชัดเจน
- เงินสำรองและตัวเลขงบในสไลด์แต่ละสัปดาห์ไม่ต่อเนื่องทั้งหมด จึงไม่อ้างว่าเป็นบัญชีจริงชุดเดียวกัน
- ROI จาก 26,400 และ 16,100 เท่ากับ 63.98% หรือ 64.0% เมื่อปัดหนึ่งตำแหน่ง
- TPS ต่างจาก concurrency; timeout ธุรกรรมไม่ได้แปลว่าชำระเงินล้มเหลว
- แบบจำลองคำสั่งซื้อเพิ่มสถานะรอคืนสินค้า/รอคืนเงิน พร้อมระบุสมมุติฐานของ business rules
- ไม่พบหัวข้อ “8.4: Maintenance Records” ในสารบัญ ISO/IEC 14764:2006; รูปแบบ Dossier สามภาคยึดบทเรียนของรายวิชา

## เอกสารโจทย์ต้นทาง

- [Pre-Final Examination.md](</home/panuwat/work/software-project-management/work/Pre-Final/Pre-Final Examination.md>)
- [Software Evolution and Maintenance.md](</home/panuwat/work/software-project-management/work/Pre-Final/Software Evolution and Maintenance.md>)
- [Software Project Management.md](</home/panuwat/work/software-project-management/work/Pre-Final/Software Project Management.md>)
- [ดัชนีลิงก์บทเรียน work.md](</home/panuwat/work/software-project-management/work/work.md>)

## เอกสารรายสัปดาห์ทั้งหมด

| สัปดาห์ | ENGSE225 | ENGSE202 |
|---:|---|---|
| 1 | [Software lifecycle, Lehman และ Technical Debt](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 1.txt>) | [Project Initiation และ Charter](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 1.txt>) |
| 2 | [Maintenance types และ Reverse Engineering](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 2.txt>) | [Scope, WBS และ Risk Management](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 2.txt>) |
| 3 | [SCM, GitFlow และ Regression Safety Net](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 3.txt>) | [RACI, Communication และ DoD](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 3.txt>) |
| 4 | [Verification/Validation และ Baseline Audit](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 4.txt>) | [Integrated Plan และ Phase Gate](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 4.txt>) |
| 5 | [ISO 25010 และ Maintainability](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 5.txt>) | [Cost Estimation และ Reserves](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 5.txt>) |
| 6 | [Re-engineering, Code Metrics และ Quality Gates](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 6.txt>) | [Jira Automation และ Cost Tracking](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 6.txt>) |
| 7 | [Metrics targets, Environment และ CI Audit](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 7.txt>) | [Cost Baseline และ Capacity Planning](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 7.txt>) |
| 8 | [Fowler Refactoring และ CR Impact Analysis](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 8.txt>) | [Burndown, Blockers และ Stakeholders](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 8.txt>) |
| 9 | [CR-01 และ Test-Driven Refinement](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 9.txt>) | [Sprint Review/Retro และ EVM](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 9.txt>) |
| 10 | [Defects, RCA และ CR-02 CSV](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 10.txt>) | [Scope Control, CCB และ Reserve Log](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 10.txt>) |
| 11 | [System Hardening และ Code Freeze](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 11.txt>) | [CFD, Burnup และ Scope Freeze](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 11.txt>) |
| 12 | [UAT และ Production Release](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 12.txt>) | [Final CPI/SPI และ Procurement Closure](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 12.txt>) |
| 13 | [Clean Deployment และ Maintenance Manual](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 13.txt>) | [KPI Scorecard, Lessons Learned และ OPAs](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 13.txt>) |
| 14 | [Packaging, Disaster Recovery และ Complete Dossier](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 14.txt>) | [Maintenance ROI และ Closure Audit](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 14.txt>) |
| 15 | [Technical Defense และ Handover](</home/panuwat/work/software-project-management/work/Software Evolution & Maintenance/ENGSE225_ Software Evolution & Maintenance Week 15.txt>) | [Final Defense และ Formal Closure](</home/panuwat/work/software-project-management/work/Software Project Management/ENGSE202_ Software Project Management Week 15.txt>) |

## ขอบเขตการตรวจทาน

- ตรวจว่ามีโจทย์ครบ 10 ข้อต่อวิชา และข้อความโจทย์ไม่ตกหล่นหลังจัดรูปแบบ
- ตรวจสูตร SV/CV/CPI/SPI, เงินสำรอง, ROI, availability budget และ SUS
- รันฟังก์ชันส่วนลดกับ 8 test cases และตรวจจำนวนเส้นทางเทียบ CFG
- ตัวอย่าง quality gate, RTM, architecture และ business flow เป็นแนวคำตอบ ไม่ใช่รายงานว่าระบบใน repository ผ่านข้อกำหนดเหล่านั้นแล้ว
- การอ้าง ISO/PMBOK ในเฉลยแยกกรอบแนวคิดออกจากกติกาของรายวิชา ตรวจเลขข้อ ISO/IEC 14764:2006 กับสารบัญเผยแพร่แล้ว และไม่อ้างว่าตรวจรับตามมาตรฐานฉบับเต็ม
