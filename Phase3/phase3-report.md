# รายงาน Phase 3 — ลงมือและคุมการเปลี่ยนแปลง (W8–W11)

ข้อมูลทั้งหมดเป็นข้อมูลสมมติเพื่อการเรียน ไม่ใช่ข้อมูลลูกค้าจริง

## 1. ภาพรวบเฟส

| รายการ | ค่า |
|---|---|
| Sprint ที่ครอบคลุม | Sprint 3 (Jira ID 85, closed) |
| สัปดาห์ | 8–11 |
| Issues | SPM-15…SPM-19 (16 SP) ปิดครบ |
| ผลลัพธ์หลัก | CR-01, CR-02, BUG-101 + EVM/Retro + Hardening + Scope Freeze |

เฟสนี้เป็นช่วงที่ระบบเริ่ม "ขยับ" ตามคำขอใหม่และตามข้อผิดพลาดที่พบ
โดยทุกการเปลี่ยนแปลงผ่านกระบวนการที่ประเมินผลกระทบและอนุมัติก่อน

## 2. สิ่งที่ทำตามสัปดาห์

| สัปดาห์ | เนื้อหา | ไฟล์หลักฐาน |
|---|---|---|
| W8 | CR-01 Impact Analysis (+8 man-hours) · Sprint Tracking/Burndown · Blocker Flag · Stakeholder & Procurement | `Sprint3/week-8/` |
| W9 | EVM Sprint 1 (PV 4,000 / EV 3,000 / AC 4,200) · Retrospective · Sprint Transition | `Sprint3/week-9/` |
| W10 | CR-02 ผ่าน CCB (4.5h × 300 = 1,350 THB) · BUG-101 5 Whys + fix · เบิกเงินสำรอง | `Sprint3/week-10/` |
| W11 | Hardening (code smell, atomic, Bandit) · WIP limit 3 · Burnup 27/29 (93%) · Scope Freeze | `Sprint3/week-11/` |

## 3. ผลลัพธ์หลัก

| ด้าน | ผลลัพธ์ |
|---|---|
| ฟีเจอร์ใหม่ | Barcode + Reorder Point + แจ้งเตือน `quantity <= reorder_point` (CR-01) |
| ฟีเจอร์รายงาน | `CsvReportExporter` ส่งออก CSV หัวตาราง 6 คอลัมน์ (CR-02) |
| ความทนทาน | แก้ `KeyError: barcode` ด้วย `dict.get` + เพิ่ม defect-driven test (BUG-101) |
| การเงิน | เบิกเงินสำรอง 1,350 THB อย่างเป็นทางการผ่าน CCB |
| การควบคุม | Scope Freeze 29 points · burnup 27/29 · WIP limit ช่อง Review 3 ใบ |

## 4. ผลติดตามและบทเรียน

| ตัวชี้วัด | ค่า |
|---|---|
| EVM Sprint 1 | SV −1,000 THB · CV −1,200 THB |
| Burnup | 27/29 points (93%) |
| Reserve หลังเบิก CR-02 | 1,473 THB |
| บทเรียนหลัก | merge conflict จากตัดโครงสร้างใหญ่รวดเดียว · ประเมินงานต่ำกว่าจริง |

Action ที่ตั้งใจทำต่อ: แจ้ง blocker ทุกวัน · PR ต้องรีวิวภายใน 12 ชั่วโมง · ใช้ TDR

## 5. ปัญหาที่พบและการจัดการ

| ปัญหา | การจัดการ |
|---|---|
| `KeyError: barcode` จากข้อมูลเก่า | fallback ในชั้น Repository + เทสต์ backward compatibility |
| Flake8 `E501` ยังค้าง | บันทึกเป็นหนี้ แก้ใน Sprint 5 (โค้ดสด E501 = 0) |
| งานค้าง 2 points ของ burnup | ยกยอดไปปิดใน Sprint 4 |

## 6. รายงานและหลักฐานฉบับเต็ม

- รายงานปิดสปรินต์: [`Sprint3/sprint3.md`](Sprint3/sprint3.md) · [หน้าเว็บ](Sprint3/sprint3.html) · [PDF](Sprint3/sprint3.pdf)
- README ของเฟส: [`README.md`](README.md)