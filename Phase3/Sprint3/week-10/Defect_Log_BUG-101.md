# บันทึกข้อบกพร่อง (Defect Log) — BUG-101: KeyError `barcode` บนข้อมูลเก่า data.json

> สัปดาห์ที่ 10 — การติดตามข้อบกพร่อง (Defect tracking) + การวิเคราะห์สาเหตุที่แท้จริง (RCA: 5 Whys) + การทดสอบที่ขับเคลื่อนด้วยข้อบกพร่อง (Defect-Driven Testing)

| ฟิลด์ (Field) | ค่า (Value) |
|---|---|
| รหัสข้อบกพร่อง (Defect ID) | BUG-101 |
| ชื่อเรื่อง (Title) | `KeyError: 'barcode'` เมื่อโหลดข้อมูลเก่า (legacy) ใน `data.json` — Crash when loading legacy JSON |
| ตำแหน่ง (Location) | `app.py: line 45` ใน `Product.__init__` |
| ความรุนแรง / ความเร่งด่วน (Severity & Priority) | **Critical / Major** — โปรแกรมเกิด Runtime Exception แล้ว Crash |
| สภาพแวดล้อม (Environment) | Python **3.11**, Commit Hash, OS Version |
| สถานะวงจรชีวิตบั๊ก (Bug Life Cycle) | New → Assigned (Tech Lead มอบหมายเจ้าของโมดูล) → Fixing (RCA + แก้บน Bugfix Branch) → Verified (Tester รัน PyTest ซ้ำ) → Closed (Merge เข้าสายหลัก) — ปัจจุบันอยู่ขั้น Fixing |
| โมดูลที่เกี่ยวข้อง | `InventoryRepository` (ชั้นโหลดข้อมูล) / โมเดล `Product` |
| ส่วนที่เกี่ยวข้อง (Related) | CR-02 (การส่งออก CSV ต้องทนต่อกรณี `barcode` หายไปด้วย) |

## สาเหตุเบื้องต้น (Context)
ไฟล์ `data.json` เดิมสร้างจากสัปดาห์ที่ 1 ไม่มีฟิลด์ `barcode` ทำให้เกิดข้อบกพร่องขอบเขต (Edge Cases) เมื่อโค้ดสคีมาใหม่เข้าถึงคีย์ตรง ๆ — จัดเป็น **Internal Defects (บั๊กภายใน)**: Legacy Data Incompatibility + Edge Case Blindspots

## ขั้นตอนการทำซ้ำ (Steps to Reproduce — ต้องจำลองซ้ำได้ 100%)
1. เตรียม `data.json` แบบดั้งเดิมที่ไร้ฟิลด์ `barcode` (เช่น `{"P001": {"name": "Pen", "qty": 10, "price": 15.0}}`)
2. โหลดข้อมูลผ่าน `InventoryRepository` (ใช้ `Product.__init__` อ่านคีย์ `barcode` ตรง ๆ)
3. สังเกตผล: โปรแกรม Crash ทันที

## ผลที่คาดหวังกับผลจริง (Expected vs Actual)
- **ที่คาดหวัง (Expected):** ระเบียนเก่าโหลดได้อย่างราบรื่น มี Default Fallback ให้อัตโนมัติ โปรแกรมไม่ล่ม
- **ผลจริง (Actual):** `KeyError: 'barcode'` — Error Stack Trace หยุดการโหลด/แสดงผล (ดูไฟล์ตัวอย่างข้อมูลเก่าใน `mock_legacy_products.json`)

## การวิเคราะห์สาเหตุด้วย 5-Whys (RCA — The 5 Whys Method)
1. **Why 1 — ทำไมเกิด KeyError?**  หาคีย์ `barcode` ไม่เจอ (โค้ดดึงค่าตรง ๆ)
2. **Why 2 — ทำไมหาคีย์ไม่เจอ?**  `data.json` สร้างจากสัปดาห์ที่ 1 (สคีมาดั้งเดิมไม่มีฟิลด์นี้)
3. **Why 3 — ทำไมระบบอ่านข้อมูลเก่าไม่ได้?**  ขาดตรรกะ Schema Migration
4. **Why 4 — ทำไมไม่มี Fallback?**  สมมุติว่าข้อมูลต้องใหม่ (สคีมาใหม่) อย่างเดียว
5. **Why 5 (Root Cause ที่แท้จริง)**  **ขาดกลไก Data Validation และ Default Fallback ในชั้น `InventoryRepository`**

## วิธีแก้ (Fix) — แก้ที่ราก ไม่ใช่ปิดอาการ
-  ห้ามทำ Symptom Fixing: ใส่ `try-except: pass` ปิด Error (ยิ่งซ่อนระเบิดเวลาไว้ลึกขึ้น)
-  Root Cause Fix: ใส่ค่า Default ใน Repository เพื่อรองรับ Backward Compatibility
```python
# Symptom-Prone Code (พังง่าย) — ดึงค่าตรง ๆ ทำให้ Crash เมื่อเจอไฟล์เก่า
code = item['barcode']

# Root Cause Fix (ปลอดภัย) — มี Fallback รองรับ Legacy Schema
code = item.get('barcode', '')
```
- ฟิลด์ที่เกี่ยวข้องในชั้น Repository: `name`, `qty`, `price`, `barcode` (default `''`), `reorder_point`

## การทดสอบที่ขับเคลื่อนด้วยข้อบกพร่อง (Defect-Driven Testing)
> กฎ: ทุกครั้งที่พบบั๊ก ก่อนลงมือแก้โค้ด ต้องเขียน Unit Test ตัวใหม่ที่เลียนแบบบั๊กนั้นขึ้นมาก่อนเสมอ
1. **Reproduce (RED):** เขียน Test Case จำลองบั๊กใน `test_app.py`  รันแล้วต้อง Fail
2. **Fix Code:** แก้ไขโค้ดที่รากเหง้าในชั้น Repository
3. **Verify (GREEN):** รัน Test Case เดิมซ้ำ  ต้องผ่าน 100%
4. **Preserve:** บรรจุ Test Case นี้เข้า Full Regression Suite เป็นเกราะถาวร (ป้องกันเพื่อนร่วมทีมเผลอลบตรรกะ Fallback ออกในอนาคต)

```python
def test_repository_handles_legacy_json_without_barcode(tmp_path):
    # 1. Arrange: จำลองไฟล์ JSON แบบดั้งเดิมที่ไร้ฟิลด์ barcode
    p = tmp_path / "legacy_data.json"
    p.write_text('{"P001": {"name": "Pen", "qty": 10, "price": 15.0}}', encoding="utf-8")
    # 2. Act: โหลดข้อมูลผ่าน Repository
    data = load_all(str(p))
    # 3. Assert: ระบบต้องไม่พัง และใส่ Default Fallback ให้อัตโนมัติ
    assert "P001" in data
    assert data["P001"].get("barcode", "") == ""
```
- ใช้ `tmp_path` ของ PyTest สร้างไฟล์ JSON จำลองในหน่วยความจำชั่วคราวโดยไม่รบกวนไฟล์จริง
- เกณฑ์ปิดงาน: Test ผ่าน + ไม่มี `KeyError` บนไฟล์ข้อมูลเก่าทั้งไฟล์

## กรณีขอบเขตที่ต้องลองเพิ่ม (Bug Bashing — เปิด Issue ติดป้าย `bug`)
- **Case A:** ป้อน Barcode ซ้ำกับสินค้าอื่น
- **Case B:** ป้อน Reorder Point เป็นตัวอักษรหรือค่าติดลบ
- **Case C:** ลบฟิลด์ใน `data.json` แล้วรันระบบ
- เมื่อพบข้อผิดพลาด ให้เปิด Issue บน GitHub Issues ทันที ระบุ Steps to Reproduce; แก้ด้วย TDR แล้ว Commit ด้วยข้อความ `fix: resolve legacy JSON missing barcode crash (fixes #12)`

## อ้างอิงมาตรฐาน
ISO/IEC 14764:2006 & IEEE Std 1219-1998 (Software Maintenance Process); ISO/IEC/IEEE 29119 (Software Testing); Andersen & Fagerhaug (2006) Root Cause Analysis
