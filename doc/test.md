#  เอกสารสรุปเตรียมสอบฉบับสมบูรณ์: Software Project Management
**อิงจากโปรเจค: CLI Inventory Management System (Python)** — Phase 1 ถึง Week 7

---

##  สารบัญ
1. [บทที่ 1 — ปัญหาของ Legacy Code และการวิเคราะห์เชิงสถิต (Week 1 & 2)](#1)
2. [บทที่ 2 — การวิเคราะห์ Hotspot และ DFD (Week 2)](#2)
3. [บทที่ 3 — สถาปัตยกรรมเป้าหมาย และ Design Patterns (Week 2, 5, 6)](#3)
4. [บทที่ 4 — บทบาทในทีมและมาตรฐานการทำงาน RACI / DoR / DoD (Week 3 & 6)](#4)
5. [บทที่ 5 — Automated Testing และ CI/CD Pipeline (Week 3, 4 & 7)](#5)
6. [บทที่ 6 — การประเมินคุณภาพซอฟต์แวร์ ISO/IEC 25010 & 14598 (Week 5 & 7)](#6)
7. [บทที่ 7 — การบริหารงบประมาณและ Earned Value Management / EVM (Week 5, 6 & 7)](#7)
8. [บทที่ 8 — Trello และเครื่องมือบริหารโครงการ (Week 1)](#8)

---

## บทที่ 1 — ปัญหาของ Legacy Code และการวิเคราะห์เชิงสถิต (Week 1 & 2) {#1}

### 1.1 ภาพรวมปัญหาของระบบเดิม (`app_v1.py`)
ก่อนจะปรับปรุงระบบได้ ทีมต้องทำ **Legacy Code Review** ให้ครบถ้วน โดยค้นพบปัญหาหลัก 4 ประการ:

| ลำดับ | ปัญหา (Code Smell) | ผลกระทบต่อระบบ | แนวทางแก้ไข |
| :---: | :--- | :--- | :--- |
| 1 | **Global State Conflict**: ประกาศ `global x` เพื่อเก็บข้อมูลสินค้าทั้งหมด | ทุกฟังก์ชันเขียนทับค่า `x` ได้ตรงๆ ทำให้ทดสอบยาก (Untestable) | เปลี่ยนเป็น OOP, เก็บสถานะใน `InventoryManager` class |
| 2 | **Input Type Mismatch**: `c = int(input("Enter Qty: "))` ไม่มี try-except | หากผู้ใช้กรอกอักษรแทนตัวเลข โปรแกรมจะ Crash ทันที (ValueError) | สร้างฟังก์ชัน Helper ที่ใช้ `try-except ValueError` |
| 3 | **Data Corruption Risk**: ใช้ `json.dump()` ทับไฟล์โดยตรง | หากไฟดับระหว่างเซฟ ไฟล์ JSON อาจว่างเปล่าทั้งหมด | ใช้เทคนิค **Atomic Save** ผ่าน Temporary File |
| 4 | **Encoding Risk**: เปิดไฟล์โดยไม่ระบุ `encoding` | ภาษาไทยอ่านเพี้ยนบน OS อื่น (Windows ใช้ CP1252) | กำหนด `encoding='utf-8'` ทุกครั้ง |

### 1.2 ผลการวิเคราะห์เชิงสถิต (Static Code Analysis ด้วย Pylint & Radon)
*   **Lines of Code (LOC):** 99 บรรทัด
*   **Pylint Score:** **7.10 / 10** (ยังต่ำกว่ามาตรฐานที่ควรจะ ≥ 8.0)

#### Cyclomatic Complexity (ความซับซ้อนของลอจิก)
ค่า Cyclomatic Complexity (CC) คือตัวชี้วัดจำนวนเส้นทาง (Paths) ในโค้ด — **ยิ่งสูงยิ่งเสี่ยง**:

| ฟังก์ชัน | ค่า CC | เกรด | ความหมาย |
| :--- | :---: | :---: | :--- |
| `main()` | **14** | **C** |  ซับซ้อนเกินไป — มีกิ่งเงื่อนไขมากจนยากต่อการทดสอบ |
| `load()` | 2 | A |  ดีมาก |
| `save()` | 1 | A |  ดีมาก |

**สูตรคำนวณ CC พื้นฐาน:** `จำนวน if/elif/while/for ทั้งหมดในฟังก์ชัน + 1`

**เกณฑ์มาตรฐานอุตสาหกรรม:**
*   CC ≤ 5 → **A** (เรียบง่าย)
*   CC 6–10 → **B** (พอรับได้)
*   CC 11–15 → **C** (ซับซ้อน — ควรแก้ไข)
*   CC > 20 → **F** (อันตรายสูง — ต้องเร่ง Refactor)

#### ประเด็นที่ Pylint ตรวจพบ (เรียงตามความรุนแรง)

| ความรุนแรง | รหัสปัญหา | รายละเอียด |
| :--- | :--- | :--- |
| **High** | ขาด Input Validation | `int(input(...))` โดยตรง — โปรแกรมหยุดทำงานเมื่อรับค่าผิดประเภท |
| **High** | ขาด Encoding | เปิดไฟล์โดยไม่ระบุ `encoding='utf-8'` |
| **Medium** | R0912 Too many branches | `main()` มี 17 สาขา เกิน 12 ที่กำหนด |
| **Medium** | R0915 Too many statements | `main()` มี 55 คำสั่ง เกิน 50 ที่กำหนด |
| **Low** | C0303 Trailing whitespace | ช่องว่างส่วนเกินท้ายบรรทัด |
| **Low** | C0114/C0116 Missing docstring | ขาด Docstring ทั้งระดับ Module และ Function |

---

## บทที่ 2 — การวิเคราะห์ Hotspot และ DFD (Week 2) {#2}

### 2.1 Hotspot คืออะไร?
**Hotspot** คือจุดที่มี **Coupling สูง** (ผูกมัดกับส่วนอื่นอย่างแน่น) และ **Fragility สูง** (เปราะบาง — แก้ผิดจุดเดียวพังทั้งระบบ) พบ 3 จุดวิกฤตในโปรเจค:

| Hotspot | จุดที่ระบุ | ทำไมถึงอันตราย |
| :--- | :--- | :--- |
| **Hotspot 1** | ตัวแปรโกลบอล `x` | ทุกฟังก์ชันอ่าน/เขียนโดยตรง → ถ้าเปลี่ยนคีย์ `"q"` เป็น `"qty"` จุดเดียว ระบบพังทั้งหมด (KeyError) |
| **Hotspot 2** | ฟังก์ชัน `main()` | UI, Logic, Data Access ปนกันในบล็อก `if/elif` เดียว — CC = 14 |
| **Hotspot 3** | Direct Value Casting | `c = int(input(...))` ไม่มีการป้องกัน — โปรแกรมหยุดทันทีถ้ากรอกผิด |

### 2.2 DFD (Data Flow Diagram) ระดับ 1
แผนภาพกระแสข้อมูลแสดงเส้นทางการไหลของข้อมูลในระบบ:

```
ผู้ใช้ → [P1: load] → ตัวแปร x (In-Memory) → [P2: show_all] → ผู้ใช้
ผู้ใช้ → [P3: add_update] → ตัวแปร x → [P6: save (Atomic)] → data.json
ผู้ใช้ → [P4: cut_stock] → ตรวจยอดจาก x → [P6: save] → data.json
ตัวแปร x → [P5: summary] → ผู้ใช้
```

---

## บทที่ 3 — สถาปัตยกรรมเป้าหมาย (To-Be Architecture) และ Design Patterns {#3}

### 3.1 สถาปัตยกรรม OOP แบบ MVC (`app_v2.py`)
โค้ดเวอร์ชันใหม่แบ่งออกเป็น 3 คลาสตาม **MVC Pattern**:

| ชั้น (Layer) | คลาส | หน้าที่ |
| :--- | :--- | :--- |
| **View** | `InventoryCLI` | รับ Input แสดงผล — ถ้าอยากเปลี่ยนจาก CLI เป็น Web ก็แค่สร้าง View ใหม่ |
| **Controller** | `InventoryManager` | Business Logic ทั้งหมด — เพิ่ม/ลบสินค้า คำนวณมูลค่า ตรวจสต็อก |
| **Model** | `Product` | โครงสร้างข้อมูลสินค้า (id, name, qty, price) |

### 3.2 To-Be Architecture สำหรับ SQLite (Week 6)
สถาปัตยกรรมเป้าหมายขั้นสูงที่ใช้ SQLite ประกอบด้วย 3 Design Patterns หลัก:

---

####  Singleton Pattern — `SQLiteDatabaseContext`
*   **นิยาม:** รับประกันว่าจะมีการสร้าง Object ของคลาสเพียงตัวเดียวตลอดโปรแกรม
*   **ปัญหาที่แก้:** ป้องกัน **Database Locked** เมื่อหลายฟังก์ชันพยายามเขียนไฟล์ SQLite พร้อมกัน
*   **วิธีทำงาน:** ครั้งแรกที่เรียก `getInstance()` จะสร้าง Connection ใหม่ — ครั้งต่อไปจะคืน Connection เดิม
*   **ข้อดี:** จัดการ Transaction (Commit/Rollback) ได้อย่างปลอดภัย ข้อมูลไม่ขัดแย้งกัน

---

####  Repository Pattern — `InventoryRepository`
*   **นิยาม:** ทำหน้าที่เป็นตัวกลาง (Abstraction Layer) คั่นระหว่าง Business Logic และ Database
*   **ปัญหาที่แก้:** ป้องกัน Business Logic มีคำสั่ง SQL ปะปนอยู่ (Separation of Concerns)
*   **วิธีทำงาน:** ครอบ SQL ทั้งหมดไว้ในเมธอด เช่น `findById()`, `save()`, `updateStock()`
*   **ความปลอดภัย:** บังคับใช้ **Parameterized Queries** ป้องกัน **SQL Injection 100%**

```python
#  เสี่ยง SQL Injection
cursor.execute(f"SELECT * FROM items WHERE id='{user_input}'")

#  ปลอดภัยด้วย Parameterized Query
cursor.execute("SELECT * FROM items WHERE id=?", (user_input,))
```

---

####  Strategy Pattern — `MemberTier`
*   **นิยาม:** แยกอัลกอริทึมการทำงาน (ในที่นี้คือการคิดส่วนลด) ออกเป็นคลาสย่อยแยกกัน
*   **ปัญหาที่แก้:** โค้ดเดิมใช้ `if-elif-elif` ยาวในการเช็กระดับสมาชิก ทำให้ผิดหลัก **Open/Closed Principle (OCP)**
*   **OCP คืออะไร?** โค้ดควรเปิดรับการขยาย (Open for Extension) แต่ปิดการแก้ไขโค้ดเดิม (Closed for Modification)

| คลาส | `getDiscountRate()` |
| :--- | :---: |
| `RegularMember` | 0.00 (0%) |
| `SilverMember` | 0.05 (5%) |
| `GoldMember` | 0.10 (10%) |
| `PlatinumMember` | 0.15 (15%) |

เมื่อต้องการเพิ่ม **Diamond** (ส่วนลด 20%) ก็แค่สร้างคลาสใหม่ ไม่ต้องแตะ if-else เดิมเลย

---

### 3.3 กลไก Atomic Save (ความปลอดภัยของข้อมูล)
*   **ปัญหา:** การเซฟทับโดยตรง (`json.dump()`) — หากไฟดับระหว่างเขียน ไฟล์พัง
*   **วิธีแก้ (Safe Write):**
    1. เขียนข้อมูลลงไฟล์ชั่วคราวก่อน (เช่น `data.json.tmp`)
    2. ถ้าเขียนสำเร็จ ใช้ `os.replace("data.json.tmp", "data.json")` สลับทับทันที
    3. ผลลัพธ์: ไฟล์ `data.json` จะเป็น "สมบูรณ์" หรือ "เดิม" เสมอ — ไม่มีสถานะ "กึ่งเขียน"

---

## บทที่ 4 — บทบาทในทีมและมาตรฐานการทำงาน (RACI / DoR / DoD) {#4}

### 4.1 RACI Matrix
ใช้กำหนดบทบาทอย่างชัดเจนในแต่ละ Task ป้องกันความสับสนและการเกี่ยงงานกัน:

| ตัวอักษร | ความหมาย | กฎสำคัญ |
| :--- | :--- | :--- |
| **R – Responsible** | ผู้ลงมือทำงานนั้น | 1 Task มีได้หลายคน |
| **A – Accountable** | ผู้อนุมัติและรับผิดชอบผลลัพธ์สุดท้าย | **1 Task มีได้แค่ 1 คน เท่านั้น** |
| **C – Consulted** | ผู้ให้คำปรึกษา (Two-way communication) | — |
| **I – Informed** | ผู้รับทราบสถานะ (One-way communication) | — |

#### ตาราง RACI ของโปรเจคนี้

| Task | Project Manager (Dev) | QA / Tester | Tech Lead |
| :--- | :---: | :---: | :---: |
| เขียนโค้ด Refactoring (Choice 2) | **R** | C | **A** |
| ปรับโครงสร้างเป็น OOP/MVC | **R** | I | **A** |
| Approve ก่อน Merge | I | I | **R, A** |
| เขียน Automated Test (PyTest) | C | **R** | **A** |
| ย้ายฐานข้อมูลเป็น SQLite | **R** | C | **A** |
| เพิ่มระบบสมาชิกและส่วนลด | **R** | C | **A** |

### 4.2 Communication Matrix
กำหนดช่องทาง ความถี่ และผู้รับผิดชอบในการสื่อสาร:

| วัตถุประสงค์ | ช่องทาง | ความถี่ | ผู้รับผิดชอบ |
| :--- | :--- | :--- | :--- |
| Standup ประจำวัน | Discord Voice | ทุกเย็น (15 นาที) | **Project Manager** |
| แจ้งบั๊ก / ทดสอบไม่ผ่าน | การ์ดบน Trello | ทันทีที่พบ | **QA / Tester** |
| ขอ Review Code | GitHub PR + Discord | เมื่อสร้าง PR เสร็จ | **Tech Lead** |
| ติดตามความคืบหน้า | Trello Board | อัปเดตตลอดเวลา | สมาชิกทุกคน |

### 4.3 Definition of Ready (DoR) — "เกณฑ์พร้อมทำ"
ก่อนที่ Developer จะดึงการ์ดจาก Trello มาลงมือโค้ด ต้องผ่านทุกเงื่อนไขนี้:

- [ ] **มีรายละเอียด (Description):** การ์ดอธิบายฟีเจอร์ชัดเจน
- [ ] **ประเมินความเสี่ยง (Hotspot):** ระบุว่าอาจกระทบส่วนไหน
- [ ] **มอบหมายชัดเจน:** ระบุ R และ A ตาม RACI Matrix
- [ ] **สร้าง Branch:** แตก Branch ใหม่จาก `develop` ใน GitHub เรียบร้อย

### 4.4 Definition of Done (DoD) — "เกณฑ์พร้อมส่ง"
งานจะถือว่าเสร็จ 100% และย้ายเข้า Done ได้ก็ต่อเมื่อ:

- [ ] **ผ่าน Code Review:** Tech Lead ตรวจ PEP 8 และกด Approve Pull Request
- [ ] **ผ่านการทดสอบอัตโนมัติ:** `test_app.py` รันบน CI Pipeline ผ่าน 100% (No Error, No Fail)
- [ ] **Merge สำเร็จ:** โค้ดถูก Merge เข้า `develop` โดยไม่มี Conflict
- [ ] **ทำเอกสาร:** อัปเดต Trello หรือจัดทำรายงาน (เช่น `test.json`)

---

## บทที่ 5 — Automated Testing และ CI/CD Pipeline {#5}

### 5.1 ทำไมต้องทำ Automated Test?
*   ป้องกัน **Regression Bug** — การแก้ฟีเจอร์ใหม่ไปทำให้ฟีเจอร์เก่าพัง
*   รันทดสอบ 100 กรณีเสร็จในไม่กี่วินาที แทนที่จะต้องกด Manual Test เอง

### 5.2 PyTest Framework — ตัวอย่างเคสสำคัญ
การทดสอบครอบคลุม 3 ประเภทหลัก:

```python
import pytest
from app import InventoryManager, Product

# ── Happy Path ──────────────────────────────────────────────────────────────
def test_cut_stock_success(manager):
    """ทดสอบการหักสต็อกสำเร็จ เมื่อของในคลังมีพอ"""
    success, msg, remaining = manager.cut_stock("1", 5)
    assert success is True
    assert remaining == 15          # สต็อกเดิม 20 หัก 5 เหลือ 15

# ── Edge Case ────────────────────────────────────────────────────────────────
def test_cut_stock_not_enough(manager):
    """ทดสอบว่าระบบปฏิเสธการเบิกเกินสต็อก (ป้องกันค่าติดลบ)"""
    success, msg, remaining = manager.cut_stock("2", 15)
    assert success is False
    assert msg == "Error: Not enough stock!"
    assert remaining == 10          # สต็อกต้องไม่เปลี่ยน

def test_cut_stock_not_found(manager):
    """ทดสอบกรณี Product ID ไม่มีในระบบ"""
    success, msg, remaining = manager.cut_stock("999", 5)
    assert success is False
    assert msg == "Product not found!"
    assert remaining is None
```

### 5.3 Fixture — การจำลองฐานข้อมูลสำหรับทดสอบ
`@pytest.fixture` ทำหน้าที่เตรียมสภาพแวดล้อมก่อนทดสอบและทำลายหลังเสร็จ:

```python
@pytest.fixture
def manager(tmp_path):
    """สร้าง InventoryManager ชั่วคราวในโฟลเดอร์ temp — ลบอัตโนมัติหลังเทสต์"""
    db_path = tmp_path / "test_data.json"
    m = InventoryManager(str(db_path))
    m.add_or_update_product(Product("1", "Apple", 20, 10.0))
    m.add_or_update_product(Product("2", "Banana", 10, 5.0))
    return m
```

### 5.4 CI/CD Quality Gate ด้วย GitHub Actions
ไฟล์ `.github/workflows/pytest.yml` ทำหน้าที่เป็น **"ยามรักษาการณ์อัตโนมัติ"**:

**Flow การทำงาน:**
```
Developer push code → GitHub Actions ทำงาน
   ├── ติดตั้ง Python & pip install -r requirements.txt
   ├── cd week-4 && pytest test_app.py -v
   │
   ├──  ผ่านทุกเคส → ปลดล็อก ปุ่ม Merge สีเขียว
   └──  มีเคสพัง → ล็อก Pull Request ทันที → Tech Lead ไม่ต้องเสียเวลารีวิวโค้ดที่พัง
```

---

## บทที่ 6 — การประเมินคุณภาพซอฟต์แวร์ (ISO/IEC 25010 & 14598) {#6}

### 6.1 ISO/IEC 25010 — โมเดลคุณภาพ 8 มิติ
ใช้ประเมินระบบ **ก่อน (As-Is)** เพื่อระบุจุดอ่อน:

| คุณลักษณะ | คะแนน As-Is | เหตุผล | เป้าหมาย To-Be |
| :--- | :---: | :--- | :--- |
| **Functional Suitability** |  | ทำงานพื้นฐานได้ แต่ขาดระบบสมาชิก, ขาด Input Protection |  |
| **Performance Efficiency** |  | JSON ขนาดเล็กเร็ว แต่ถ้าข้อมูลเพิ่มขึ้นจะช้า |  (SQLite) |
| **Compatibility** |  | Python ข้ามแพลตฟอร์มได้ แต่ไม่มี API ออก |  |
| **Usability** |  | ไม่มี Input Validation โปรแกรมหลุดได้ง่าย |  |
| **Reliability** |  | ไม่มี Transaction, ไฟล์พังได้ง่าย |  (Atomic Save + SQLite) |
| **Security** |  | ไม่มี Authentication, ข้อมูลเป็น Plain-text |  (Parameterized Query) |
| **Maintainability** |  | Monolithic, ชื่อตัวแปรสั้น ไม่มี Docstring |  (OOP + Tests) |
| **Portability** |  | Python รันได้ทุก OS |  |

### 6.2 ISO/IEC 14598 — ตัวชี้วัดเชิงปริมาณ (Quantitative Metrics)
ใช้ยืนยันเชิงตัวเลขว่า Refactoring ประสบความสำเร็จจริง:

| ตัวชี้วัด | สถานะ As-Is | เป้าหมาย To-Be |
| :--- | :--- | :--- |
| **Max Cyclomatic Complexity v(G)** | > 20 ใน `main()`  | ≤ 8 ต่อฟังก์ชัน  |
| **Code Coverage** | 0% (ไม่มีเทสต์)  | ≥ 85% จาก `test_app.py`  |
| **Global State Usage** | `global x` ทุกฟังก์ชัน  | ยกเลิก 100% → ใช้ Class Instances  |
| **SQL Injection Vulnerability** | N/A (JSON) | ป้องกัน 100% ด้วย Parameterized Query  |
| **Data Security** | โปรแกรม Crash จากค่าผิดประเภท  | มีระบบ try-except ดักทุก Input  |

---

## บทที่ 7 — การบริหารงบประมาณ (Cost Baseline & EVM) {#7}

### 7.1 WBS (Work Breakdown Structure) และต้นทุน
| รหัส | งาน | บทบาท | เวลา (ชม.) |
| :--- | :--- | :--- | :---: |
| WBS-01 | ออกแบบสถาปัตยกรรม To-Be | Tech Lead | 5 |
| WBS-02 | ย้ายฐานข้อมูล JSON → SQLite | Developer | 5 |
| WBS-03 | เขียน `DatabaseManager` (Singleton) | Developer | 4 |
| WBS-04 | สร้าง `ProductManager` | Developer | 4 |
| WBS-05 | ระบบสมาชิกและส่วนลด `MemberSystem` | Developer | 4 |
| WBS-06 | ปรับ CLI Interface (Facade Pattern) | Developer | 3 |
| WBS-07 | Integration Testing | QA | 10 |
| WBS-08 | ทำเอกสารสรุป | QA | 5 |
| **รวม** | | | **40 ชม.** |

### 7.2 Cost Baseline (งบประมาณฐาน)
| หมวดหมู่ | อัตรา | ชั่วโมง | จำนวนเงิน |
| :--- | :--- | :---: | ---: |
| Project Manager / Developer | 500 THB/ชม. | 20 | 10,000 |
| Tech Lead / Architect | 600 THB/ชม. | 25 | 15,000 |
| QA / Tester | 400 THB/ชม. | 15 | 6,000 |
| **รวมค่าแรง** | | **60** | **31,000** |
| ค่าโครงสร้างพื้นฐาน (Cloud, CI/CD, Tools) | | | 3,000 |
| **ต้นทุนรวมเบื้องต้น (Base Cost)** | | | **34,000** |
| งบสำรองเผื่อฉุกเฉิน 15% (Contingency Reserve) | | | 5,100 |
| **งบประมาณโครงการรวม (Total Budget)** | | | **39,100** |

> **Contingency Reserve** คือ งบที่กันไว้สำหรับ **Known-Unknowns** (ความเสี่ยงที่รู้ว่าจะเกิด แต่ไม่รู้ว่าเมื่อไร เช่น Legacy Code ซับซ้อนกว่าที่คาด)

### 7.3 Earned Value Management (EVM)
เครื่องมือติดตามงบประมาณแบบ Real-time:

| ตัวย่อ | ชื่อเต็ม | ความหมาย |
| :--- | :--- | :--- |
| **PV** | Planned Value | มูลค่างานที่ "วางแผน" ไว้จะเสร็จ ณ วันนี้ |
| **EV** | Earned Value | มูลค่างานที่ "ทำเสร็จจริง" ณ วันนี้ |
| **AC** | Actual Cost | ต้นทุนที่ "จ่ายจริง" ณ วันนี้ |
| **CV** | Cost Variance | `EV - AC` |
| **SV** | Schedule Variance | `EV - PV` |

**การตีความผล:**

| ค่า | ความหมาย | การดำเนินการ |
| :--- | :--- | :--- |
| **CV > 0** |  Under Budget | ดำเนินการตามแผน |
| **CV = 0** |  On Budget | ดำเนินการตามแผน |
| **CV < 0** |  Over Budget | ดึงเงินจาก Contingency Reserve มาใช้ |
| **SV > 0** |  Ahead of Schedule | ดำเนินการตามแผน |
| **SV < 0** |  Behind Schedule | ปรับแผนงาน / เพิ่มทรัพยากร |

#### กรณีศึกษา: งานย้ายฐานข้อมูล JSON → SQLite

| รายการ | มูลค่า |
| :--- | :--- |
| งบประมาณที่ตั้งไว้ (Planned Cost) | 6 ชม. × 400 = **2,400 บาท** |
| งานเสร็จ 100% → Earned Value (EV) | **2,400 บาท** |
| โค้ดเก่าซับซ้อน → ใช้เวลา 10 ชม. จริง (AC) | 10 ชม. × 400 = **4,000 บาท** |
| **Cost Variance (CV = EV - AC)** | 2,400 - 4,000 = **-1,600 บาท ** |

**การแก้ไข (Management Action):**
1. PM แจ้งเตือนทีม (Warning) สถานะ Over Budget
2. PM ดึงเงินจาก **Contingency Reserve** ที่กันไว้ 15% มาชดเชยทันที
3. PM หารือกับ Tech Lead เพื่อปรับ Blueprint ของงานถัดไป (Member System) ให้ละเอียดขึ้น

### 7.4 Capacity Planning (การคำนวณกำลังการผลิต)
ใช้กำหนดขีดสูงสุดของงานที่ดึงเข้า Sprint ได้:

**สูตร:** `จำนวนคน × เวลา (ชม./สัปดาห์) × จำนวนสัปดาห์`

**ตัวอย่าง Sprint 1:**
`3 คน × 6 ชม./สัปดาห์ × 2 สัปดาห์ = 36 Man-Hours`

**กฎ:** งาน Sprint Backlog ทั้งหมดรวมกันต้องไม่เกิน 36 ชม. หากเกินต้องตัดงานออก (Scope Reduction)

### 7.5 เกณฑ์การแจ้งเตือนผลต่างงบประมาณ (Cost Variance Thresholds)

| ช่วง Variance | สถานะ | การดำเนินการ |
| :--- | :--- | :--- |
| 0% – 5% |  ปกติ | ดำเนินการต่อตามแผน |
| > 5% – 10% |  แจ้งเตือน | PM ประชุมทีมหาแนวทางลดเวลาแก้บั๊ก |
| > 10% |  วิกฤต | พิจารณาตัดฟีเจอร์ (Scope Reduction) หรือดึงงบสำรอง |

---

## บทที่ 8 — Trello และเครื่องมือบริหารโครงการ {#8}

### 8.1 Kanban Board บน Trello
แบ่งคอลัมน์งานออกเป็น 5 ช่อง:

```
Backlog → To Do → In Progress → Review → Done
```

*   **Backlog:** งานทั้งหมดที่รู้ว่าต้องทำ ยังไม่ถูกกำหนดตาราง
*   **To Do:** งานที่พร้อมทำใน Sprint นี้ (ผ่าน DoR แล้ว)
*   **In Progress:** กำลังพัฒนาอยู่ (ไม่ควรเกิน 2-3 การ์ดต่อคน)
*   **Review:** รอ Code Review จาก Tech Lead
*   **Done:** ผ่าน DoD ครบทุกข้อ

### 8.2 Project Charter — โครงสร้างพื้นฐาน
เอกสารที่ให้อำนาจโครงการเริ่มต้นได้อย่างเป็นทางการ ประกอบด้วย:
*   **วัตถุประสงค์โครงการ (Project Objectives):** Stability, Refactoring, Data Integrity, Automated Testing
*   **ขอบเขต (Scope):** In-Scope (OOP, SQLite, PyTest) vs Out-of-Scope (GUI, External DB)
*   **ตารางเวลา (Schedule):** Phase 1–4 ตาม WBS
*   **ตารางความเสี่ยง (Risk Matrix):** ระบุความเสี่ยงและ Mitigation Plan

---

##  สรุปสูตรสำคัญที่ต้องจำ

| หัวข้อ | สูตร / ค่า |
| :--- | :--- |
| Cyclomatic Complexity | `จำนวน if/elif/while/for + 1` |
| Cost Variance (CV) | `EV - AC` (ลบ = Over Budget) |
| Schedule Variance (SV) | `EV - PV` (ลบ = ล่าช้า) |
| Team Capacity | `คน × ชม./สัปดาห์ × สัปดาห์` |
| Code Coverage | `บรรทัดที่ทดสอบ / บรรทัดทั้งหมด × 100` |
| Contingency Reserve | ≈ 10–15% ของ Base Cost |

##  คำศัพท์ที่ต้องรู้

| คำศัพท์ | ความหมาย |
| :--- | :--- |
| **Refactoring** | ปรับโครงสร้างโค้ดให้ดีขึ้น โดยไม่เปลี่ยนพฤติกรรมการทำงาน |
| **Regression Testing** | ทดสอบว่าการแก้ไขใหม่ไม่ทำให้ฟีเจอร์เก่าพัง |
| **Atomic Save / Atomic Write** | การบันทึกไฟล์ที่รับประกันว่าไฟล์จะสมบูรณ์หรือไม่เปลี่ยนเลย ไม่มีสถานะ "กึ่งสำเร็จ" |
| **SQL Injection** | การโจมตีด้วยการแทรก SQL ปลอมผ่าน Input ผู้ใช้ |
| **Parameterized Query** | วิธีส่งค่า Input แยกจาก SQL Statement — ป้องกัน SQL Injection |
| **Coupling** | ระดับการผูกมัดระหว่างคลาส/ฟังก์ชัน — ยิ่งน้อยยิ่งดี (Loose Coupling) |
| **Separation of Concerns** | หลักการแบ่งโค้ดให้แต่ละส่วนรับผิดชอบงานเดียวอย่างชัดเจน |
| **Open/Closed Principle** | โค้ดควรขยายได้โดยไม่ต้องแก้ไขโค้ดเดิม |
| **Singleton** | Design Pattern ที่รับประกัน 1 Class มี 1 Instance เท่านั้น |
| **Repository Pattern** | เลเยอร์ที่ซ่อน SQL ทั้งหมด แยก Business Logic จาก Data Access |
| **Strategy Pattern** | แยกอัลกอริทึมออกเป็นคลาสย่อย สลับกันได้ตาม Runtime |
| **Earned Value (EV)** | มูลค่าของงานที่ทำเสร็จแล้ว (วัดเป็นงบประมาณ) |
| **Contingency Reserve** | งบสำรองสำหรับ Known-Unknowns — ไม่ใช่ "กำไร" |
| **Definition of Ready (DoR)** | เกณฑ์ความพร้อม "ก่อนเริ่มทำ" |
| **Definition of Done (DoD)** | เกณฑ์ความสำเร็จ "ก่อนปิดงาน" |
