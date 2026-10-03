# รายงาน Phase 4 — UAT ปล่อยรุ่น v2.0 (W12)

ข้อมูลทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. ภาพรวบเฟส

| รายการ | ค่า |
|---|---|
| Sprint ที่ครอบคลุม | Sprint 4 (Jira ID 83, closed) |
| สัปดาห์ | 12 |
| Issues | SPM-20, SPM-21 (5 SP) ปิดครบ |
| รุ่นที่ส่งมอบ | `v2.0.0-evolution` |

เฟสนี้ปิดวงจรสัปดาห์ที่ 1–12 ด้วยการทดสอบการยอมรับผู้ใช้ เตรียมตัวปล่อย
และสรุปสถานะการเงินของทั้งโครงการ

## 2. สิ่งที่ทำในสัปดาห์ที่ 12

| งาน | หลักฐาน |
|---|---|
| โค้ดวิวัฒนาการ (รวม CR-01/CR-02/BUG-101 fix) | `Sprint4/week-12/app.py` |
| ชุดทดสอบเติบโต 5 → 25 เคส | `Sprint4/week-12/test_app.py` |
| UAT SC01–SC03 + sign-off sheet | `Sprint4/week-12/UAT_Sign_Off_Sheet.md` |
| Release checklist 3 ด่าน | `Sprint4/week-12/Release_Checklist.md` |
| CHANGELOG + Final EVM | `Sprint4/week-12/CHANGELOG.md`, `Final_EVM.md` |

## 3. ผลลัพธ์หลัก

| ด้าน | ผลลัพธ์ |
|---|---|
| เทสต์ | 25 passed (baseline 5 + CR-01 4 + CR-02 6 + BUG-101 4 + CLI 3 + integration 3) |
| UAT | SC01–SC03 ผ่านในส่วนผลทางเทคนิค และคัดแยกประเด็นชัดเจน |
| การเงิน | SPI 1.00 (ตรงเวลา) · CPI 0.96 · CV −575 THB (3.7%) |
| เงินสำรอง | 2,823 − 1,350 − 575 = เหลือ 898 THB |
| Velocity | Sprint 1 = 15 · Sprint 2 = 22 · Sprint 3 = 12 |

## 4. สถานะที่ยังไม่ปิด

| รายการ | สถานะ |
|---|---|
| ลายเซ็น UAT ของผู้ทดสอบและ Tech Lead | ยังว่าง — ต้องลงนามก่อนถือว่ารับรองเสร็จสมบูรณ์ |
| Flake8 `E501` | ยังค้างในรุ่นนี้ (แก้ใน Sprint 5) |
| การรองรับข้อมูลเก่าแบบ migration เต็มรูปแบบ | ยังเป็น fallback อย่างเดียว |

## 5. รายงานและหลักฐานฉบับเต็ม

- รายงานปิดสปรินต์: [`Sprint4/sprint4.md`](Sprint4/sprint4.md) · [หน้าเว็บ](Sprint4/sprint4.html) · [PDF](Sprint4/sprint4.pdf)
- สรุปรอบ W1–12: [`Sprint4/sprint-report.html`](Sprint4/sprint-report.html) · [สไลด์](Sprint4/sprint1-slides.html) · [PDF](Sprint4/summary-w1-w12.pdf)
- README ของเฟส: [`README.md`](README.md)