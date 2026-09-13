---
target: slide decks week-1..12 + Phase1
total_score: 21
max_score: 24
na_heuristics: 9,10
p0_count: 1
p1_count: 2
target_identity: "file:/home/panuwat/work/software-project-management/Sprint1/week-12/slides.html"
target_fingerprint: "sha256:ac7ceff542a678125b5efaddc80f75b4be987c83071a471aaa639a0780ccae54"
target_path: /home/panuwat/work/software-project-management/Sprint1/week-12/slides.html
timestamp: 2026-09-13T18-15-50Z
slug: sprint1-week-12-slides-html
---
# Critique — slide decks week-1..12 + Phase1 (13 files, 52 slides)

⚠️ DEGRADED: single-context (dual subagents failed twice with upstream server_error; review + evidence done inline with detector CLI, DOM metrics and headless screenshots instead)

## Design Health Score (decks)

| # | Heuristic | Score | Key Issue |
|---|---|---|---|
| 1 | Visibility of System Status | 3 | counter+hash+restart ครบ; restore เงียบแต่มีปุ่มเริ่มใหม่แก้ |
| 2 | Match System / Real World | 3 | ภาษาไทยโดเมนดี มีศัพท์ดิบปนเล็กน้อย |
| 3 | User Control and Freedom | 3 | prev/next/restart/keyboard/hash/fresh ครบ; ไม่มี overview grid |
| 4 | Consistency and Standards | 2 | สองทรง A/B markup controls ต่างกัน; tokens สไลด์ drift จาก theme.css |
| 5 | Error Prevention | 3 | storage guarded, hash parse guarded, file:// ได้จริง |
| 6 | Recognition Rather Than Recall | 3 | counter+ปุ่มกลับเนื้อหาชัด; 13 ชุดแพทเทิร์นเดียว |
| 7 | Flexibility and Efficiency | 2 | คีย์บอร์ด+hash jump มี; ข้ามไกล/ดูภาพรวมไม่ได้ |
| 8 | Aesthetic and Minimalist Design | 2 | สไลด์แน่นล้น viewport (เห็นจริง week-12 slide 2) |
| 9 | Error Recovery | n/a | สไลด์ static ไม่มี error state |
| 10 | Help and Documentation | n/a | deck คือเอกสารเอง |
| **Total** | | **21/24 (87.5%, Good)** | |

## Design Specificity Verdict

**LLM**: fit-for-purpose ไม่โดดเด่น — เหมาะกับ internal coursework decks (marker pills รหัสสัปดาห์, footer อ้างแหล่ง .md, ปุ่มกลับเนื้อหา) แต่ 13 ชุดใช้ template เดียวกันจึงไม่มีเอกลักษณ์รายชุด ซึ่งถูกต้องแล้วสำหรับงานนี้
**Scan**: 50 findings (low-contrast 26, tight-leading 23, em-dash 1) — ส่วนใหญ่คือ tokens ยุคก่อน polish (ส้ม #d9730d 2.8:1, เทา 4.48:1) กับ leading ของ pill/counter; DOM assertions ผ่าน (lang/title×13, slide≥3, counter+keyboard+hash+restart+guarded storage, id ไม่ซ้ำ, external 0)
**Overlay**: fallback (headless-only) — ทดแทนด้วยสกรีนช็อตตรวจตา + วัดตัวอักษร/บูลเล็ตทุกสไลด์

## Overall Impression

โครง deck แข็งแรง (nav ครบ file:// ได้) แต่สไลด์แน่นเกิน 8 หน้าเนื้อหาล้นจอจริง — ปัญหาเดียวที่ผู้ชมเห็นบนเวที

## What's Working

1. **Deep-link + restart + fresh**: ส่งลิงก์ `#slide-3` เปิดตรงหน้าได้จริง (verify ทั้งสองทรง)
2. **Self-contained**: 13/13 ไฟล์ไร้ external เปิด file:// ได้ตาม PRODUCT.md
3. **Honesty pills**: ป้ายสมมติ + อ้างแหล่ง .md ท้ายสไลด์สม่ำเสมอ

## Priority Issues

- **[P0] สไลด์แน่นล้น viewport (เห็นจริง)**: week-12 slide 2 ป้ายอังกฤษขาดบน บูลเล็ตขาดล่าง; วัดทั้ง 52 สไลด์พบ 8 หน้าเสี่ยง (week-8/s4 940 ตัวอักษร, week-7/s2, week-10/s2+s3 9 บูลเล็ต, week-5/s3, week-6/s4, week-7/s4, week-12/s3) — **Fix**: จำกัด ≤5 บูลเล็ต/≤600 ตัวอักษรต่อสไลด์ แยกหน้าที่เกิน + safety `overflow-y:auto` ใน slide-body — Suggested: /impeccable layout
- **[P1] Tokens สไลด์ตกยุคก่อน polish**: ส้ม #d9730d (2.8:1) เทา #787774 (4.48:1) — **Fix**: sync กับ theme.css (#9c4400/#6f6a63) — Suggested: /impeccable polish
- **[P1] สองทรง A/B markup controls ไม่เหมือนกัน** — **Fix**: รวม controls pattern เดียว — Suggested: /impeccable polish
- **[P2] ไม่มี overview grid กระโดดข้ามสไลด์** — **Fix**: เพิ่ม grid ภาพย่อ — Suggested: /impeccable shape

## Persona Red Flags

- **Presenter**: สไลด์ล้นบน projector (P0 ข้างบน); ลำดับคีย์บอร์ด/restart/deep-link ครบแล้ว (เขียว)
- **Jordan**: สไลด์ 9 บูลเล็ตศัพท์ EVM/CCB แน่น อ่านตามไม่ทัน
- **Sam**: aria-live แก้แล้ว (ประกาศแค่ "สไลด์ N จาก M"); counter เป็น span แต่ live region คุมให้แล้ว

## Content Accuracy (spot-check)

ตรวจลึก 3 ชุด (week-12 ตรง Final_EVM ทุกตัวเลข, week-9 ตรง EVM_Sprint1, week-1 ตรง charter) ที่เหลืออีก 10 ชุดตรวจแค่โครงสร้าง — ยังไม่พบแต่งตัวเลข แต่ยังไม่ได้รับรองครบ

## Minor Observations

- em-dash ในสไลด์ไทยเป็น false positive (ตัวคั่นปกติ)
- tight-leading ส่วนใหญ่คือ pill/counter ไม่กระทบอ่าน

## Questions to Consider

- สไลด์แน่น 8 หน้า: แยกสไลด์ (ได้ ~60 สไลด์) หรือย่อความ (เสี่ยงเสียเนื้อหา)?
- overview grid คุ้มความซับซ้อนที่เพิ่มในไฟล์ self-contained ไหม?
- จะล็อกความยาวสไลด์ใน DoD ของงานเว็บเลยไหม (กันกลับมาแน่นอีก)?
