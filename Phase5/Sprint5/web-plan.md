# [Historical / Superseded] แผนงาน: จาก CLI สู่ Web App (v4.0-web)

> แผนนี้ถูกแทนที่ด้วย `program-plan.md` หลังเปลี่ยน scope เป็น Desktop Program UI

เป้าหมาย: เว็บหน้าตาทันสมัย ใช้งานได้ทั้งคอมพิวเตอร์และมือถือ
Backend Python + Frontend HTML/CSS/JavaScript (ไม่ใช้ framework ฝั่ง frontend
เพื่อไม่ต้องมี build step) โดย reuse ตรรกะเดิมจาก `app.py` v3.0 ทั้งหมด

## 1. ขอบเขต

**ทำ:** เว็บ CRUD สินค้า, Dashboard สรุป + แจ้งเตือน low-stock, จัดการสมาชิก,
Checkout คิดส่วนลดพร้อมใบเสร็จบนเว็บ, ดาวน์โหลด CSV, responsive 360px/768px/1280px
**ไม่ทำ:** ระบบล็อกอิน/สิทธิ์, จ่ายเงินออนไลน์, แอปมือถือ native, หลายสาขา/หลายผู้ใช้พร้อมกัน
(SQLite = single-user ตามข้อจำกัดเดิม)

## 2. Tech Stack

| ชั้น | เลือก | เหตุผล |
|---|---|---|
| Backend | FastAPI + Uvicorn | REST ตรงสเปก, Pydantic ตรวจ input แทน validator เดิม, มี `/docs` ให้เทสต์ API ฟรี |
| Domain/DB | reuse `app.py` v3.0 ทั้งก้อน | `Product`, `MemberTier`, `CheckoutService`, `InventoryRepository`, `MemberManager` ใช้ต่อได้เลย API เป็น wrapper บาง ๆ CLI เดิมไม่พัง |
| Database | SQLite (`inventory.db` ไฟล์เดิม) | ไม่ต้องย้ายข้อมูล, migrate script เดิมใช้ต่อ |
| Frontend | HTML + CSS + JavaScript ล้วน | ตรงสเปกที่ขอ, เปิดไฟล์/serve ง่าย, ไม่ต้อง build |
| Style | CSS custom (variables + grid/flex) + Noto Sans Thai | คุมธีมให้เข้ากับเว็บพอร์ทัลเดิม (`theme.css`), responsive ด้วย media queries |
| Test | pytest + FastAPI TestClient | ต่อจากชุดเดิม 14 เคส ไม่ต้องเปลี่ยนเครื่องมือ |

## 3. สถาปัตยกรรม

```text
Browser (SPA: dashboard/products/members/checkout)
   │  fetch JSON
   ▼
FastAPI (/api/*) ──► Service layer (reuse: CheckoutService ฯลฯ)
                          │
                          ▼
                   SQLite (inventory.db)
CLI เดิมยังรันได้ (ใช้ service ชั้นเดียวกัน)
```

โครงโฟลเดอร์ใหม่ (ไม่แตะของเดิม):

```text
Phase5/Sprint5/web/
├── backend/
│   ├── main.py        # FastAPI app + รวม router
│   ├── api_products.py
│   ├── api_members.py
│   ├── api_checkout.py
│   └── deps.py        # เปิด DB context / repository ร่วมกัน
├── frontend/
│   ├── index.html     # SPA shell + nav (responsive + hamburger)
│   ├── styles.css     # ธีม + responsive
│   └── app.js         # fetch API + render แต่ละหน้า
└── README.md          # วิธีรัน (uvicorn + เปิดเว็บ)
```

## 4. API Design (REST)

| Method | Endpoint | ใช้ทำอะไร |
|---|---|---|
| GET | `/api/health` | ตรวจสถานะ |
| GET/POST | `/api/products` | ดูทั้งหมด / เพิ่ม-อัปเดต |
| GET/PUT/DELETE | `/api/products/{id}` | ดูรายตัว / แก้ / ลบ |
| POST | `/api/products/{id}/cut` | ตัดสต็อก `{qty}` |
| GET | `/api/summary` | ยอดรวม + low-stock list |
| GET | `/api/export.csv` | ดาวน์โหลดรายงาน CSV |
| GET/POST | `/api/members` | ดูทั้งหมด / เพิ่ม-อัปเดต |
| GET/DELETE | `/api/members/{id}` | ดูรายคน / ลบ |
| POST | `/api/checkout` | `{product_id, member_id?, qty}` → ใบเสร็จ JSON |

กฎ: error คืน JSON `{detail}` + HTTP status ถูกต้อง (404/400/409);
ห้ามต่อ SQL string (ใช้ repository เดิม), Pydantic กันค่าติดลบ/`qty<=0`

## 5. หน้าจอ Frontend (4 หน้าใน SPA เดียว)

1. **Dashboard** — การ์ดสรุป (จำนวนแบบ/มูลค่ารวม/low-stock), ตาราง alert,
   ปุ่มลัดไป checkout
2. **Products** — ค้นหา + ตาราง (badge `[LOW]`, barcode, ROP), ฟอร์มเพิ่ม/แก้ไข,
   ปุ่มตัดสต็อก, ปุ่มโหลด CSV
3. **Members** — ตาราง tier + อัตรา, ฟอร์มสมัคร/เปลี่ยน tier, ค้นหารหัส
4. **Checkout** — เลือกสินค้า + จำนวน + รหัสสมาชิก (ว่าง = guest) →
   แสดง Subtotal/Discount/Total + สต็อกคงเหลือ + คำเตือน

Responsive: nav บน desktop / hamburger บนมือถือ, ตารางแนวนอน scroll ได้ที่ 360px,
ฟอร์ม 1 คอลัมน์บนมือถือ 2 คอลัมน์บนจอใหญ่, ปุ่มแตะง่าย (≥44px)

## 6. แผนงาน 4 ช่วง (พร้อมบทบาท)

| ช่วง | งาน | SP | ใคร |
|---|---|---:|---|
| A. Foundation | โครง `Phase5/Sprint5/web/`, FastAPI + reuse domain, `/health`+`/docs`, สคริปต์รัน, API tests แรก | 8 | Tech Lead + Dev |
| B. Products + Dashboard | API สินค้า/summary/CSV + UI 2 หน้า + responsive รอบแรก | 8 | Dev + QA |
| C. Members + Checkout | API สมาชิก/checkout + UI 2 หน้า + ใบเสร็จ + edge cases | 8 | Dev + QA |
| D. Hardening + Release | เทสต์มือถือ 3 ขนาด, E2E smoke, flake8/bandit, README + คู่มือ, demo script, tag `v4.0.0-web` | 5 | ทั้งทีม |

รวม 29 SP ≈ 2 sprints (อิง velocity เดิม Sprint 1 = 15, Sprint 2 = 17)

## 7. ความเสี่ยงและวิธีรับมือ

| ความเสี่ยง | รับมือ |
|---|---|
| Scope creep (อยากได้ auth/จ่ายเงิน) | freeze ตามหัวข้อ 1, ส่วนเกิน → backlog อนาคต |
| แก้ domain แล้ว CLI พัง | API เป็น wrapper บาง ๆ ห้ามแก้ `app.py` domain; regression 14 + 25 ต้องเขียวตลอด |
| SQLite เขียนพร้อมกัน | เอกสารกำกับ single-user; เขียนผ่าน repository เดิม (commit/rollback) |
| JS บานปลาย | แยกฟังก์ชันต่อหน้า ห้าม lib ภายนอก, โค้ดรีวิวก่อน merge |
| หน้าพังบนมือถือ | ตรวจ 3 ขนาดทุกครั้งก่อนปิดงาน (checklist ใน DoD) |

## 8. Definition of Done (รายช่วง)

- pytest (เดิม + API ใหม่) เขียว 100%, `flake8`/`bandit` สะอาด
- เปิดบน 360/768/1280px ใช้งานได้จริงทุกปุ่ม (มีหลักฐานภาพ/เช็กลิสต์)
- เดโมสคริปต์ผ่าน: เพิ่มสินค้า → สมัคร Gold → checkout 1,000 เหลือ 900 →
  โหลด CSV → ตัดเกินสต็อกต้อง error สวยไม่พัง
- CLI เดิมยังรันได้ + regression เขียว, README อัปเดตวิธีรันเว็บ

## 9. ขั้นต่อไป

สร้าง Epic + 4 stories (A–D) ลง Jira แล้วเริ่มช่วง A ได้ทันที
