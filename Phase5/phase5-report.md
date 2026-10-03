# รายงาน Phase 5 — วิวัฒนาการ v3.0 และเว็บแอป v4.0

ข้อมูลทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. ภาพรวบเฟส

| รายการ | ค่า |
|---|---|
| Sprint ที่ครอบคลุม | Sprint 5 (Jira ID 86, closed) |
| Issues | SPM-23…SPM-27 (17 SP) + SPM-29…SPM-32 (29 SP) = **46 SP** ปิดครบ |
| Epics | SPM-22 (SQLite + Member), SPM-28 (WEB) |
| รุ่นที่ส่งมอบ | `v3.0.0` (CLI+SQLite) และ `v4.0.0-web` (เว็บแอป) |

เฟสนี้เป็นการ "นำแบบออกแบบที่ค้างมาตั้งแต่ Sprint 1 มาทำจริง" และขยายไปถึงเว็บแอป
โดยกำหนดขอบเขตชัดเจน: ไม่ทำระบบล็อกอินและระบบชำระเงินออนไลน์

## 2. สองส่วนของงาน

### ส่วน A — v3.0: SQLite + Member + Checkout

| หัวข้อ | ผลลัพธ์ |
|---|---|
| ฐานข้อมูล | ย้ายจาก JSON เป็น SQLite แบบ Singleton + Repository + parameterized query 100% |
| Transaction | commit/rollback ทุก write พร้อม schema `CHECK` กันค่าติดลบ |
| Migration | สคริปต์ย้าย `data.json` พร้อมตรวจจำนวนและมูลค่าตรง 100% |
| สมาชิก | CRUD + 4 tiers (0/5/10/15%) ด้วย Strategy pattern, tier ผิด fallback Regular |
| Checkout | คิดส่วนลดอัตโนมัติ + ใบเสร็จแยกบรรทัด + ตัดสต็อก atomic |

### ส่วน B — v4.0-web: เว็บแอป responsive

| หัวข้อ | ผลลัพธ์ |
|---|---|
| Backend | FastAPI + Uvicorn reuse domain เดิมทั้งหมด (ไม่แตกโครงสร้างชั้น domain) |
| Frontend | SPA 4 หน้า: แดชบอร์ด · สินค้า · สมาชิก · ขาย |
| Responsive | ใช้งานได้ที่ 360 / 768 / 1280 px (ทดสอบด้วย screenshot จริง) |
| API | products CRUD + cut · summary · export.csv · members CRUD + tiers · checkout |
| UI เด่น | ใบเสร็จบนหน้าจอ, ป้าย LOW, ค้นหาสินค้า, แก้ไขแบบเติมฟอร์มเดิม |

## 3. หลักฐานทดสอบ

| ชุด | ผล |
|---|---|
| `test_app.py` (CLI) | 14 passed (5 เดิม + 9 ใหม่) |
| `web/backend/test_web_api.py` | 6 passed |
| **รวม** | **20 passed** |
| regression `Sprint4/week-12/test_app.py` | 25 passed (ไม่แตก) |

## 4. คุณภาพและความปลอดภัย

| รายการ | ผล |
|---|---|
| flake8 | 0 ปัญหา (โค้ดสด + backend เว็บ + tools) |
| bandit | 0 ปัญหา |
| SQL injection | ทดสอบด้วย `' OR '1'='1` และ `DROP TABLE` แล้วถูกดักเป็น string ธรรมดา |
| บั๊กที่พบใน QA | SQLite cross-thread → แก้ด้วย `check_same_thread=False` |

## 5. ขอบเขตที่ตกลงไม่ทำ

- ระบบล็อกอิน/สิทธิ์ผู้ใช้
- ระบบชำระเงินออนไลน์
- รองรับหลายผู้ใช้พร้อมกัน (SQLite เป็น single-user; ย้าย PostgreSQL ได้ผ่าน Repository)

## 6. งานที่ค้างจากเฟสก่อน

- ช่องลายเซ็น UAT (Sprint 4) ยังรอผู้รับรองลงนาม
- Flake8 `E501` ในไฟล์ snapshot ประวัติการทำงาน 112 จุด (เก็บเป็นหลักฐาน ไม่แก้)
- ตัวเลขรายงานที่อ้างถึงรุ่น v2.0 ยังใช้ตัวเลขเดิมของ Phase 1–4 (ไม่ได้วัดใหม่สำหรับ v3.0)

## 7. รายงานและหลักฐานฉบับเต็ม

- รายงานปิดสปรินต์: [`Sprint5/sprint5.md`](Sprint5/sprint5.md) · [หน้าเว็บ](Sprint5/sprint5.html) · [PDF](Sprint5/sprint5.pdf)
- รายละเอียดส่วน v3.0: [`Sprint5/sprint2.md`](Sprint5/sprint2.md) · [PDF](Sprint5/sprint2.pdf)
- รายละเอียดส่วนเว็บ: [`Sprint5/sprint3.md`](Sprint5/sprint3.md) · [แผนงาน](Sprint5/web-plan.md)
- วิธีรันเว็บ: [`Sprint5/web/README.md`](Sprint5/web/README.md)
- README ของเฟส: [`README.md`](README.md)