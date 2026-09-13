# รายการตรวจสอบก่อนปล่อย — v2.0.0-evolution (สัปดาห์ที่ 12)

อ้างอิง: ENGSE225 Week 12 (Release ISO 12207, SemVer 2.0.0, ISO 14764) และ ENGSE202 Week 12 (Final EVM)
ตัวเลขและข้อมูลทั้งหมดในเอกสารนี้เป็นข้อมูลสมมติเพื่อใช้ในการเรียนเท่านั้น

## ด่านที่ 1 — UAT ผ่านและลงนามแล้ว

- [ ] ดำเนิน Cross-Team UAT ตาม 3 Scenarios แล้ว (UAT-SC01 รับเข้า Milk 885/10 ชิ้น/ROP 5,
  UAT-SC02 ตัด 6 เหลือ 4 เกิด Alert, UAT-SC03 Export CSV เปิดใน Excel)
- [ ] `UAT_Sign_Off_Sheet.md` สรุป Total Scenarios Passed 100% และลงนามครบ 2 ฝ่าย
  (ตัวแทนผู้ทดสอบ + Tech Lead)
- [ ] ประเด็น UAT ถูกคัดแยกแล้ว: Defect (ไม่ตรงสเปกเดิม เช่น ≤ ROP แต่ไม่ Alert → แก้ด่วนก่อน Merge)
  กับ New Scope (เช่น ขอส่งอีเมลหาซัพพลายเออร์ → บันทึก Future Backlog v3.0 ห้ามทำสัปดาห์นี้)

## ด่านที่ 2 — Regression ผ่านและ Tech Lead อนุมัติแล้ว

- [ ] `python -m pytest week-12/test_app.py -q` จบด้วยรหัส 0 (25 tests ผ่าน 100%:
  baseline 5 + CR-01 4 + CR-02 6 + BUG-101 4 + CLI 3 + integration 3)
- [ ] เปิด Pull Request บน GitHub: base `main` ← compare `develop`
  (รวม Refactored Architecture + CR-01 + CR-02)
- [ ] รอท่อ CI/CD รัน PyTest ผ่านไฟเขียว แล้ว Tech Lead กดปุ่ม Confirm Merge
  (สาขา main กลายเป็น Gold Master Release)

## ด่านที่ 3 — Merge, Tag, CHANGELOG แล้ว

- [ ] รวมสายเข้า main แล้ว (สาขา main คือเวอร์ชันทางการของโครงการ)
- [ ] สลับไป main ดึงล่าสุด แล้วสร้าง Annotated Tag ตาม SemVer 2.0.0
  (จาก v1.0.0-baseline ขยับเป็น v2.0.0-evolution เพราะเปลี่ยนสถาปัตยกรรมใหญ่
  และเพิ่มโมเดลข้อมูลธุรกิจใหม่):

```bash
git checkout main
git pull origin main
git tag -a v2.0.0-evolution -m "Production Release v2.0.0: Refactored Repository Pattern, Barcode Support, Reorder Point Alerts, and CSV Reporting."
git push origin v2.0.0-evolution
```

- [ ] ตรวจหน้า GitHub Releases: มีแท็ก `v2.0.0-evolution` ชื่อ `Mini Inventory System v2.0.0`
  พร้อมป้ายสีเขียว Latest Release (GitHub สร้าง .zip/.tar.gz ให้อัตโนมัติ)
- [ ] `CHANGELOG.md` มีหัวข้อ `## [2.0.0-evolution] - 2026-08-31` ครบหมวด
  Added / Changed / Removed / Fixed และมิติ ISO 14764 ครบแล้ว Push ขึ้น main แล้ว
- [ ] ตัวเลขใน `Final_EVM.md` กระทบยอดแล้ว (PV 15,525 / EV 15,525 / AC 16,100 /
  SPI 1.00 / CPI 0.96 / CV −575) พร้อมตาราง Procurement และ Contingency

## หมายเหตุการย้อนกลับ

หากพบตัวขัดขวางหลังติดแท็ก: ลบแท็กในเครื่องด้วย `git tag -d v2.0.0-evolution`,
ลบแท็กระยะไกลด้วย `git push origin :refs/tags/v2.0.0-evolution` หากพุชไปแล้ว,
แก้ไขบน `phase2` รันทั้ง 3 ด่านใหม่ แล้วติดแท็กใหม่เป็น `v2.0.1-evolution`
ห้าม force-push ประวัติ `phase2` ที่ใช้ร่วมกับทีม
