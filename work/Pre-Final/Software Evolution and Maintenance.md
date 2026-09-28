รายวิชา ENGSE225: วิวัฒนาการซอฟต์แวร์และการบำรุงรักษา (Software Evolution and Maintenance)
คำชี้แจง: จงตอบคำถามอัตนัยต่อไปนี้โดยแสดงการวิเคราะห์ทางวิศวกรรมซอฟต์แวร์ อธิบายตรรกะการแก้ปัญหา และอ้างอิงมาตรฐานสากล (ISO/IEC, Fowler's Refactoring, Clean Architecture) อย่างเป็นระบบ (ข้อละ 10 คะแนน รวม 50 คะแนน)

ข้อที่ 1: การผ่าตัดโค้ดด้วยเทคนิค Refactoring ของ Martin Fowler (สัปดาห์ที่ 8)
ในการเข้าปรับปรุงซอฟต์แวร์คลังสินค้าดั้งเดิม (app_v1.py) เพื่อขจัดปัญหาหนี้ทางเทคนิค (Technical Debt)
1.1 จงอธิบายความหมายและขั้นตอนเชิงปฏิบัติการของเทคนิค Refactoring ต่อไปนี้ พร้อมยกตัวอย่างชิ้นส่วนโค้ด (Pseudo-code หรือ Python) สั้น ๆ ประกอบการอธิบาย:

Extract Class / Extract Function: การแตกฟังก์ชัน main() ขนาดใหญ่และกระจัดกระจายออกเป็นคลาส Product, InventoryRepository และ InventoryService

Encapsulate Field & Parameterize Object: การขจัดตัวแปรระดับโลก global x แล้วเปลี่ยนมาส่งผ่านอ็อบเจกต์ (Dependency Injection) ผ่านพารามิเตอร์แทน 

1.2 ตามแนวคิดของ Martin Fowler เพราะเหตุใดการทำ Refactoring จึงต้องมี "Safety Net" (เช่น ชุดทดสอบ PyTest) ควบคู่ไปด้วยเสมอ และกฎเหล็กของสภาวะการรัน Test ระหว่างผ่าตัดโค้ดคืออะไร?

ข้อที่ 2: กระบวนการจัดการคำขอเปลี่ยนแปลงและวิวัฒนาการซอฟต์แวร์ (สัปดาห์ที่ 8, 9, 10)
2.1 เมื่อลูกค้าส่งมอบใบคำขอเปลี่ยนแปลง Change Request (CR-01: ขอเพิ่ม Barcode และ Reorder Point) และ Emergency Change Request (CR-02: ขอส่งออกรายงานสต็อกต่ำเป็นไฟล์ CSV ด่วน) จงอธิบายขั้นตอนการจัดการคำขอตามมาตรฐาน ISO/IEC 14764 / IEEE 1219 ตั้งแต่ขั้นตอนการรับคำขอ การวิเคราะห์ผลกระทบ (Impact Analysis) จนถึงการเขียนชุดทดสอบแบบ Test-Driven Refinement (TDR)
2.2 หากการนำระบบไปใช้งานจริงพบข้อบกพร่องว่า "เมื่อเปิดไฟล์ข้อมูลเก่า data.json ที่ไม่มีฟิลด์ barcode โปรแกรมเกิด KeyError และแครชทันที" จงใช้เทคนิค Root Cause Analysis (RCA) - 5 Whys วิเคราะห์หาต้นตอของปัญหานี้ และอธิบายแนวทางแก้ไขในระดับสถาปัตยกรรม (เช่น การทำ Default Fallback Mechanism ใน Repository Layer)

ข้อที่ 3: การเสริมความมั่นคงปลอดภัยและการแช่แข็งโค้ด (สัปดาห์ที่ 11)
3.1 ในช่วงการทำ System Hardening จงอธิบายความเสี่ยงของปัญหา Data Corruption ที่เกิดจากการบันทึกไฟล์แบบดั้งเดิม (open(file, 'w')) เมื่อระบบเกิดไฟดับหรือ Crash กะทันหัน และอธิบายว่าเทคนิค Atomic File Writing (การใช้ไฟล์ชั่วคราวร่วมกับ os.replace) ช่วยแก้ปัญหานี้ให้เกิดความปลอดภัย 100% ได้อย่างไร
3.2 ตามมาตรฐาน ISO/IEC/IEEE 12207 จงอธิบายความหมาย วัตถุประสงค์ และ "กฎเหล็กของการเข้าสู่สภาวะ Code Freeze" เหตุใดทีมวิศวกรซอฟต์แวร์จึงต้องสั่งห้ามเพิ่มฟีเจอร์ใหม่ (No New Features) ในสัปดาห์ที่ 11 ก่อนวันส่งมอบจริง?




ข้อที่ 4: การตรวจรับระบบ UAT และการส่งมอบสู่ Production Baseline (สัปดาห์ที่ 12)
4.1 ในการส่งมอบซอฟต์แวร์ตามมาตรฐาน ISO/IEC/IEEE 12207 (Release Management) จงอธิบายความแตกต่างระหว่าง System Testing กับ User Acceptance Testing (UAT) และเหตุใดกระบวนการตรวจรับจึงต้องแยกแยะระหว่าง "UAT Defect" กับ "New Scope Identification" ให้เด็ดขาดจากกัน?
4.2 จงอธิบายหลักการตั้งชื่อเวอร์ชันตามมาตรฐาน Semantic Versioning 2.0.0 (MAJOR.MINOR.PATCH) พร้อมระบุเหตุผลว่า เพราะเหตุใดโครงการระบบคลังสินค้านี้จึงได้รับการเลื่อนระดับเวอร์ชันจาก v1.0.0-baseline ไปสู่ v2.0.0-evolution บนสาขา main ผ่านการสร้าง Annotated Git Tag?

ข้อที่ 5: การติดตั้งบนสภาพแวดล้อมบริสุทธิ์และการปิดแฟ้มประวัติบำรุงรักษา (สัปดาห์ที่ 13, 14, 15)
5.1 ทำไมการทดสอบติดตั้งซอฟต์แวร์บน "Clean / Fresh Environment" ในสัปดาห์ที่ 13 จึงมีความสำคัญอย่างยิ่งยวดในการแก้ปัญหา "It works on my machine"? และการทำ Smoke Testing แตกต่างจาก Post-Maintenance Full Regression Testing อย่างไร?
5.2 ตามมาตรฐาน ISO/IEC 14764 (Clause 8.4: Maintenance Records) จงระบุองค์ประกอบสำคัญ 3 ประการที่ต้องบรรจุใน Complete System Maintenance Dossier (แฟ้มประวัติวิศวกรรมบำรุงรักษาฉบับสมบูรณ์) เพื่อให้ทีมงานรุ่นถัดไป (Next-Generation Maintenance Team) สามารถรับช่วงดูแลระบบต่อได้อย่างยั่งยืน


เนื้อหาเพิ่มเติม รายวิชา วิวัฒนาการซอฟต์แวร์และการบำรุงรักษา (Software Evolution and Maintenance)
 (Software Testing, Quality Assurance & Metrics)
คำชี้แจง: ข้อสอบอัตนัย 5 ข้อ เน้นการทดสอบเชิงโครงสร้าง กระบวนการประกันคุณภาพตามมาตรฐานสากล การวัดผลเชิงปริมาณ และการทำ Automation Pipeline

ข้อ 1: Control Flow Testing & Cyclomatic Complexity

โจทย์: กำหนดฟังก์ชันคำนวณส่วนลดตามลอจิกดังนี้:


Python
def calculate_discount(customer_type, total_amount, is_first_time):
    discount = 0.0
    if customer_type == "VIP":
        if total_amount > 1000:
            discount = 0.20
        else:
            discount = 0.10
    elif customer_type == "MEMBER":
        if total_amount > 500 or is_first_time:
            discount = 0.05
    else:
        if is_first_time and total_amount > 2000:
            discount = 0.02
    return discount



คำถาม:


จงวาด Control Flow Graph (CFG) ของฟังก์ชันดังกล่าว
จงคำนวณหาค่า Cyclomatic Complexity V(G) โดยแสดงวิธีทำอย่างละเอียด (ทั้งจากสูตร E - N + 2P และ Predicate Nodes + 1)
จงออกแบบชุด Test Cases พื้นฐาน (Basis Paths) ให้ครอบคลุมทุกเส้นทางการทำงานแบบ 100% Path Coverage

ข้อ 2: Integration Testing & Test Doubles Architecture

โจทย์: ในระบบที่มีสถาปัตยกรรมแบบ Microservices หรือ Three-Tier Architecture ฟังก์ชัน OrderService.checkout() ต้องเรียกใช้งาน PaymentGatewayService, InventoryService และ EmailNotificationService
คำถาม:


จงเปรียบเทียบการเลือกใช้ Test Doubles ทั้ง 3 ประเภท ได้แก่ Dummy/Stub, Mock และ Fake ในการทดสอบ Unit/Integration Test ของ OrderService ว่าควรใช้ประเภทใดกับ Service ใด พร้อมให้เหตุผลทางเทคนิค
จงอธิบายกลยุทธ์การทดสอบแบบ Top-Down เทียบกับ Bottom-Up Integration ในกรณีนี้ โดยระบุข้อดีและข้อจำกัดของการใช้ Drivers และ Stubs




ข้อ 3: Automated Testing & Continuous Integration (CI/CD Pipeline)

โจทย์: บริษัทต้องการยกระดับกระบวนการส่งมอบซอฟต์แวร์ให้มีเสถียรภาพ โดยกำหนด Test Automation Pyramid เข้าสู่ระบบ CI Pipeline
คำถาม:


จงอธิบายสัดส่วนและเป้าหมายของแต่ละชั้นใน Test Pyramid (Unit Test, Integration Test, E2E/UI Test) ว่าทำไมจึงไม่ควรสร้าง E2E Test เป็นสัดส่วนหลักของระบบ (Ice-Cream Cone Anti-pattern)
จงเขียน Workflow ขั้นตอนใน CI Pipeline (เช่น Linting, SAST, Unit Test with Coverage, Integration Test, Smoke Test) พร้อมระบุ Quality Gate ที่ควรตั้งค่าเพื่อ Block ไม่ให้ Code ที่มีปัญหาผ่านการ Merge ไปยัง Branch Production

ข้อ 4: Software Process Improvement & ISO/IEC 29110

โจทย์: องค์กรขนาดเล็ก (Very Small Entities - VSEs) ที่พัฒนาระบบตามมาตรฐาน ISO/IEC 29110 Basic Profile ประกอบด้วยกระบวนการ Project Management (PM) และ Software Implementation (SI)
คำถาม:


ในกระบวนการ Software Implementation (SI) กิจกรรมใดบ้างที่ทำหน้าที่เป็น Verification & Validation (V&V) โดยตรงต่อตัว Work Products
ให้นักศึกษาอธิบายแนวทางการจัดทำ Peer Review หรือ Code Review Checklist ที่สอดคล้องกับมาตรฐานนี้ เพื่อให้มั่นใจว่า Requirement ถูกส่งต่อไปยัง Implementation และ Unit Test โดยไม่ตกหล่น


ข้อ 5: Software Quality Metrics & Usability Evaluation

โจทย์: ทีมพัฒนาได้ทำการวัดผลคุณภาพของซอฟต์แวร์ทั้งด้าน Internal Metrics และ External Metrics หลังจากการปล่อยเวอร์ชันทดสอบ
คำถาม:

จงอธิบายความแตกต่างระหว่าง Defect Density, Code Churn และ Test Case Pass Rate พร้อมวิเคราะห์ว่า หากพบสถานการณ์ "Test Case Pass Rate 98% แต่ Defect Density ในช่วง UAT ยังคงสูง" น่าจะเกิดจากสาเหตุใดในขั้นตอนการออกแบบการทดสอบ
ในการประเมินด้านการใช้งาน (Usability) หากทีมเลือกใช้แบบประเมิน System Usability Scale (SUS) จงอธิบายหลักการคำนวณคะแนนรวม (จากสเกล 1-5 ของข้อคำถามเลขคี่และเลขคู่ ไปสู่คะแนน 0-100) และเกณฑ์การแปลผลคะแนนว่าระดับใดจึงจัดว่าอยู่ในเกณฑ์มาตรฐานที่ยอมรับได้ (Acceptable)

