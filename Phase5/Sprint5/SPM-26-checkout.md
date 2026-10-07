# SPM-26 — Member Discount into Checkout Flow

- Jira: `SPM-26` (3 SP) → Done, comment ผูกโค้ดแล้ว
- เรื่องเล่า: ในฐานะแคชเชียร์ ฉันต้องการให้ตอน checkout
  คิดส่วนลดตาม tier อัตโนมัติพร้อมใบเสร็จแยกบรรทัด

## เกณฑ์ยอมรับ → หลักฐาน

1. สมาชิก Gold ซื้อของ 1,000 บาท checkout แล้วสุทธิต้อง 900
   พร้อมรายละเอียดส่วนลด → เทสต์
   `test_checkout_gold_discount_receipt` (สินค้า 500×2 =
   subtotal 1,000, Gold 10% = −100, total 900, เหลือสต็อก 8)
   ผ่าน; ใบเสร็จมี `subtotal`/`tier`/`discount_rate`/
   `discount_value`/`grand_total`
2. ตัดสต็อกพร้อมกัน alert จุดสั่งซื้อต้องยังทำงาน →
   เทสต์ `test_checkout_guest_full_price_and_stock_cut`
   (guest ราคาเต็ม, ของไม่พอคืนจำนวนคงเหลือ) และ
   `test_checkout_keeps_reorder_alert` (ตัดแล้ว
   `low_stock: True`, `get_low_stock_alerts` เจอ,
   summary ขึ้นชื่อ) ผ่าน

## โค้ดและพฤติกรรม

- `app.py`: `CheckoutService.calculate_total_with_discount`
  (`subtotal/discount/total`), `process_checkout` ตรวจ
  `qty > 0`, สินค้ามี, ของพอ → คำนวณ → `update_stock`
  ใน transaction เดียว (พัง = rollback + message)
- รหัสสมาชิกว่าง/ไม่มีในระบบ = guest `Regular` (Graceful
  Guest-Only ตาม scope เดิม); CLI เมนู 7 พิมพ์ใบเสร็จพร้อม
  คำเตือนเมื่อถึงจุดสั่งซื้อซ้ำ
