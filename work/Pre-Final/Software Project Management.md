รายวิชา ENGSE202: การจัดการโครงการซอฟต์แวร์ (Software Project Management)
คำชี้แจง: จงตอบคำถามอัตนัยต่อไปนี้โดยใช้กรอบมาตรฐานสากล PMBOK Guide (7th Edition), ทฤษฎี Earned Value Management (EVM) และระเบียบวิธี Agile/Scrum ในการวิเคราะห์และแก้ไขปัญหาทางการบริหาร (ข้อละ 10 คะแนน รวม 50 คะแนน)

ข้อที่ 1: การติดตามควบคุมโครงการแบบ Agile และการบริหาร Blocker (สัปดาห์ที่ 8)
1.1 ในการติดตามสุขภาพของรอบการพัฒนาผ่าน Sprint Burndown Chart บน Jira จงวาดภาพและวิเคราะห์ลักษณะเส้นกราฟจริง (Actual Line) ใน 3 สภาวะต่อไปนี้:

สภาวะที่เส้น Actual ทอดตัวอยู่ใต้เส้น Ideal Line
สภาวะที่เส้น Actual ลอยสูงกว่าเส้น Ideal Line
สภาวะที่เส้น Actual เกิดอาการหักหัวพุ่งสูงขึ้นกะทันหันกลาง Sprint (Scope Injection Bump)

1.2 เมื่อสมาชิกในทีมแจ้งใน Daily Standup ว่า "ติด Blocker ไม่สามารถเขียนโค้ดต่อได้เนื่องจากรอเพื่อนส่ง Pull Request" ในฐานะ Project Manager (PM) ท่านมีขั้นตอนในการบันทึกและปลดล็อกปัญหานี้บนกระดาน Jira (เช่น การใช้ระบบ Flagging) อย่างไร?

ข้อที่ 2: การประเมินผลต่างประสิทธิภาพ (EVM) และพิธีกรรม Agile (สัปดาห์ที่ 9)
2.1 โครงการหนึ่งตั้งเป้าหมายใน Sprint 1 ไว้ที่ Planned Value (PV) = 4,000 บาท เมื่อสิ้นสุด Sprint พบว่าทีมทำงานเสร็จสมบูรณ์ผ่าน DoD คิดเป็นมูลค่าเนื้องาน (EV) = 3,000 บาท แต่มีการบันทึก Log Time ค่าแรงจริง (AC) = 4,200 บาท:

จงคำนวณหาค่า Schedule Variance (SV) และ Cost Variance (CV) พร้อมตีความสถานะทางการบริหาร
จงเสนอแนวทางแก้ไขทางการเงินว่า PM ต้องนำเงินจากส่วนใดมาชดเชยผลต่างที่ติดลบนี้

2.2 จงเปรียบเทียบความแตกต่างระหว่างพิธีกรรม Sprint Review กับ Sprint Retrospective และอธิบายว่าการใช้เทคนิค Mad / Sad / Glad หรือ Start / Stop / Continue ช่วยให้ทีมสร้าง Actionable Items ไปปรับปรุงการทำงานใน Sprint ถัดไปได้อย่างไร?

ข้อที่ 3: การควบคุมการเปลี่ยนแปลงขอบเขต และคณะกรรมการ CCB (สัปดาห์ที่ 10)
3.1 Scope Creep คืออะไร และส่งผลร้ายต่อโครงการซอฟต์แวร์อย่างไร? จงอธิบายการรักษาสมดุลของ Project Management Iron Triangle (Scope, Time, Cost) เมื่อลูกค้ายื่นคำขอเปลี่ยนแปลงฉุกเฉิน (CR-02) เข้ามากลางคัน
3.2 จงอธิบายบทบาท หน้าที่ และองค์ประกอบของ Change Control Board (CCB) พร้อมอธิบายคำตัดสิน 3 รูปแบบ (Approve, Reject, Defer) หาก CCB มีมติว่า "Approve ให้ทำฟังก์ชันส่งออก CSV ทันที" PM จะต้องดำเนินการปรับปรุงเอกสารงบประมาณ (Contingency Reserve Utilization Log) และปรับแผนงานบน Jira อย่างไร?

ข้อที่ 4: การวิเคราะห์กระแสงานขั้นสูง (CFD, Burnup) และ Scope Freeze (สัปดาห์ที่ 11)
4.1 ในการวิเคราะห์กระแสการทำงานผ่าน Cumulative Flow Diagram (CFD) บน Jira จุดอุดตันคอขวด (Bottleneck) จะสังเกตเห็นได้อย่างไรบนแผนภูมิ? และการนำกฎของลิตเติล (Little's Law:  Lead Time = WIP /Throughput ) มาใช้โดยการกำหนด WIP Limits ในช่อง Code Review ช่วยลดระยะเวลาการส่งมอบงานได้อย่างไร?
4.2 จงอธิบายความเหนือกว่าของ Burnup Chart เมื่อเปรียบเทียบกับ Burndown Chart ในโครงการที่มีการเปลี่ยนแปลงขอบเขตงานบ่อยครั้ง และเหตุใด PM จึงต้องเจรจาทำข้อตกลง Scope Freeze Agreement กับลูกค้าในสัปดาห์ที่ 11 ก่อนวันส่งมอบจริง?

ข้อที่ 5: การประเมินดัชนี KPIs, ความคุ้มค่า ROI และการปิดโครงการ (สัปดาห์ที่ 12, 13, 14, 15)
5.1 ในการประเมินผลสัมฤทธิ์โครงการขั้นสุดท้ายผ่าน Project KPI Scorecard จงอธิบายความหมายและสูตรคำนวณของดัชนีชี้วัดประสิทธิภาพเชิงลึกทั้ง 2 ตัว ได้แก่:

Cost Performance Index (CPI = EV / AC): บ่งบอกประสิทธิภาพใด และหากคำนวณได้ CPI = 0.96 มีความหมายทางการเงินอย่างไร?
Schedule Performance Index (SPI = EV / PV): บ่งบอกประสิทธิภาพใด และหากคำนวณได้ SPI = 1.00 มีความหมายด้านเวลาอย่างไร?


5.2 ตามมาตรฐาน PMBOK Guide (Close Project or Phase) จงอธิบายความแตกต่างระหว่างกระบวนการ Administrative Closure (การจัดเก็บสินทรัพย์ OPAs และการบันทึก Lessons Learned) กับ Financial & Procurement Closure (การกระทบยอดสัญญาเครื่องมือและการปิดบัญชีเงินสำรอง) พร้อมอธิบายแนวทางการคำนวณผลตอบแทนความคุ้มค่า Maintenance ROI ของโครงการ

💡 คำแนะนำสำหรับการนำชุดข้อสอบ Pre-Final ไปใช้งาน:
เกณฑ์การตอบคำถามที่ดี: นักศึกษาควรเน้นการตอบเป็นลำดับขั้นตอน (Step-by-step) มีการยกตัวอย่างเคสจริงจากระบบคลังสินค้า (เช่น ตัวแปร global x, คลาส Product, ฟังก์ชัน reorder_point, ฟังก์ชัน CSV export, งบประมาณ Contingency Reserve)

การบูรณาการข้ามวิชา: สังเกตว่าโจทย์จะเชื่อมโยงกัน เช่น เมื่อฝั่ง ENGSE225 พบ Defect หรือทำ Impact Analysis จะส่งผลต่อตัวเลข Man-Hours, เส้น Burndown, ตาราง EVM และการตัดสินใจของ CCB ในฝั่ง ENGSE202 เสมอ เพื่อให้นักศึกษาเห็นภาพการทำงานจริงในระดับอุตสาหกรรมซอฟต์แวร์ครับโครงสร้างชุดข้อสอบ Pre-Final Exam แบบอัตนัย (Subjective Exam) ครอบคลุมเนื้อหาครึ่งหลังของภาคการศึกษา (สัปดาห์ที่ 8–15) โดยเน้นการคิดวิเคราะห์ ออกแบบ และประยุกต์ใช้งานจริงในงานวิศวกรรมซอฟต์แวร์



เนื้อหาเพิ่มเติม รายวิชาการจัดการโครงการซอฟต์แวร์ (Software Project Management)
 (Software Requirement Specification & Management / System Analysis)
คำชี้แจง: ข้อสอบอัตนัย 5 ข้อ เน้นการวิเคราะห์ความต้องการ การจัดทำโมเดลความต้องการระดับสูง และการจัดการการเปลี่ยนแปลง (Change Management)

ข้อ 1: การเปลี่ยนผ่านความต้องการสู่สถาปัตยกรรม (Non-Functional Requirements to Architecture)

โจทย์: กำหนด Use Case: "ผู้ใช้ทำธุรกรรมชำระเงินผ่าน Mobile Banking ในช่วงเทศกาลส่งเสริมการขาย" โดยมี Non-Functional Requirements (NFR) ดังนี้


Response Time สำหรับการตัดยอดเงินต้องไม่เกิน 2 วินาที
Availability ของระบบต้องอยู่ที่ 99.95% ตลอด 24/7
ต้องรองรับ Peak Concurrency สูงสุด 5,000 Transactions Per Second (TPS)
คำถาม:


จงอธิบายแนวทางการแปลง NFR ทั้ง 3 ข้อให้เป็นข้อกำหนดทางเทคนิค (Architectural Tactics / Technical Constraints) อย่างเป็นรูปธรรม
ให้ออกแบบ Interaction Overview Diagram หรือ Sequence Diagram แสดงการจัดการเมื่อระบบปลายทาง (Payment Gateway) เกิด Timeout เพื่อรักษาความคงสมบูรณ์ของข้อมูล (Data Consistency)


ข้อ 2: Requirement Traceability Matrix (RTM) & Impact Analysis

โจทย์: ในระหว่างสัปดาห์สุดท้ายของการพัฒนา Sprint ผู้มีส่วนได้ส่วนเสีย (Stakeholder) ขอยื่น Change Request (CR) เพื่อแก้ไขกระบวนการยืนยันตัวตน จากการใช้ OTP ผ่าน SMS เป็นการยืนยันด้วย Biometric + TOTP App
คำถาม:


จงเขียนตาราง Requirement Traceability Matrix (RTM) จำลองที่เชื่อมโยงระหว่าง User Requirement, Functional Requirement, Test Cases และ System Component ที่ได้รับผลกระทบ
จงประเมิน Impact Analysis ทั้งในมิติของ Scope, Schedule, Cost และ Technical Debt หากจำเป็นต้องอนุมัติ CR นี้ทันที

ข้อ 3: การจัดการความขัดแย้งของความต้องการ (Requirement Conflict & Prioritization)

โจทย์: ระบบบริหารจัดการคำสั่งซื้อของธุรกิจแบบ Omni-channel มีความขัดแย้งระหว่างฝ่ายการตลาด (ต้องการบันทึกข้อมูลและ Checkout ให้ไวที่สุดโดยไม่ต้องบังคับกรอกข้อมูลส่วนบุคคล) กับฝ่ายบัญชีและการเงิน (ต้องการบังคับกรอกเลขประจำตัวผู้เสียภาษีและที่อยู่ตามทะเบียนบ้านทันทีก่อนสร้าง Order)
คำถาม:


ให้นำเสนอเทคนิคการทำ Requirement Prioritization (เช่น MoSCoW หรือ Kano Model) พร้อมระบุเกณฑ์การตัดสินใจ
จงเขียนแนวทางการประนีประนอม (Negotiation Resolution) เพื่อออกแบบ Business Flow ใหม่ที่ตอบโจทย์คุณค่าทางธุรกิจของทั้งสองฝ่าย



ข้อ 4: Requirement Validation and Verification (V&V)

โจทย์: เมื่อจัดทำเอกสาร Software Requirement Specification (SRS) ตามมาตรฐาน IEEE 830 หรือ ISO/IEC/IEEE 29148 เสร็จสิ้น
คำถาม:


จงอธิบายความแตกต่างเชิงปฏิบัติระหว่าง Requirement Verification และ Requirement Validation พร้อมยกตัวอย่างกิจกรรมที่ทีมต้องทำในแต่ละมิติ
หากนำเกณฑ์คุณภาพ 3 ด้าน ได้แก่ Unambiguous (ไม่กำกวม), Verifiable (ตรวจสอบ/ทดสอบได้) และ Traceable (ติดตามได้) จงชี้ข้อบกพร่องของประโยค Requirement นี้ และเขียนปรับปรุงใหม่ให้ถูกต้องตามหลักการ:
"ระบบต้องประมวลผลการคำนวณภาษีและออกใบเสร็จได้อย่างรวดเร็วและเป็นมิตรกับผู้ใช้งาน"
ข้อ 5: Formal Modeling & State Transition Specification

โจทย์: ระบบจัดการสถานะคำสั่งซื้อ (Order Lifecycle Management) มีเงื่อนไขการเปลี่ยนสถานะซับซ้อน ได้แก่ Draft, Pending Payment, Paid, Processing, Shipped, Delivered, Cancelled, Refunded
คำถาม:


จงเขียน State Machine Diagram (UML) แสดง State, Transitions, Events และ Guard Conditions ที่ครอบคลุมทุกกรณี รวมถึงกรณีการยกเลิกสินค้าและการขอเงินคืน
จงระบุเงื่อนไข Exception Handling สำหรับกรณีที่สินค้าส่งออกจากคลังแล้ว (Shipped) แต่ผู้ใช้งานต้องการกดยกเลิกคำสั่งซื้อ ว่าระบบต้องจัดลำดับขั้นตอนทางธุรกิจและจัดการสถานะอย่างไร

