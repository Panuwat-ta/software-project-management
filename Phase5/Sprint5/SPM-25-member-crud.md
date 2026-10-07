# SPM-25 — Member CRUD Module with 4 Tiers

- Jira: `SPM-25` (3 SP) → Done, comment ผูกโค้ดแล้ว
- เรื่องเล่า: ในฐานะพนักงานร้าน ฉันต้องการจัดการข้อมูลสมาชิก
  (เพิ่ม/ค้นหา/แก้ไข) พร้อมระดับ Regular 0%, Silver 5%,
  Gold 10%, Platinum 15%

## เกณฑ์ยอมรับ → หลักฐาน

1. มีรหัสสมาชิก ค้นหาแล้วต้องเจอพร้อม tier ถูกต้อง →
   `MemberManager.save_member`/`find_by_id`/`find_all`/
   `delete_member` (parameterized); เทสต์
   `test_member_crud_four_tiers` สร้างครบ 4 tiers ตรวจอัตรา
   0.0/0.05/0.10/0.15, แก้ไข tier, ลบแล้วหาย ผ่าน
2. tier ผิด/ว่างบันทึกแล้วต้อง fallback Regular (0%) โดยไม่
   error → `normalize_tier`/`discount_rate_for` คืน Regular/0.0
   เสมอเมื่อ input ผิด; เทสต์ `test_member_invalid_tier_fallback_regular`
   (รวม `"Diamond"`, `""`, `None`) ผ่าน

## โค้ด

- `app.py`: Strategy `MemberTier` + 4 คลาสย่อย
  (`RegularMember`/`SilverMember`/`GoldMember`/`PlatinumMember`,
  เพิ่ม tier ใหม่ไม่ต้องแตะ `if-else` ตาม OCP),
  `Member` (`discount_rate` property), `MemberManager`
  (ตาราง `members`, เก็บ `discount_rate` จาก tier ที่ normalize แล้ว)
- CLI เมนู 6: ดูรายชื่อ / เพิ่ม-อัปเดต / ค้นหา (พิมพ์เตือนและ
  fallback เมื่อ tier ไม่รู้จัก)
