# SPM-31 — C. Members + Checkout Desktop UI

- Jira: `SPM-31` (8 SP) → Done
- งาน: หน้า Members และ Checkout พร้อมใบเสร็จในโปรแกรม Desktop

## เกณฑ์ยอมรับ → หลักฐาน

1. เพิ่ม/แก้ไข/ลบสมาชิกได้
2. รองรับ Regular 0% / Silver 5% / Gold 10% / Platinum 15%
3. Checkout ใช้ `CheckoutService` เดิม ไม่คำนวณส่วนลดซ้ำใน UI
4. Guest ได้ราคาเต็ม
5. Gold ซื้อ 2 × 500 = 1,000 → สุทธิ 900
6. ใบเสร็จแสดง subtotal, tier, discount, grand total และ stock คงเหลือ

## โค้ด

- `program.py` — Members / Checkout UI และ `format_receipt`
- `app.py` — `MemberManager`, `MemberTier`, `CheckoutService`
- `test_program.py` — integration checkout ผ่าน domain จริง
