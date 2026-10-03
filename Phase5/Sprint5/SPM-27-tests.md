# SPM-27 — Automated Tests for DB Layer and Discount Engine

- Jira: `SPM-27` (3 SP) → Done, comment ผูกโค้ดแล้ว
- เรื่องเล่า: ในฐานะ QA ฉันต้องการชุดทดสอบครอบชั้น DB และ
  เครื่องคำนวณส่วนลด รวมทดสอบกัน SQL injection

## เกณฑ์ยอมรับ → หลักฐาน

1. มี input `' OR '1'='1` ส่งผ่านชั้น DB แล้วต้องไม่หลุดเป็น
   SQL → เทสต์ `test_parameterized_blocks_sql_injection`
   (`find_by_id` คืน None, จำนวนแถว/ยอดเงินเท่าเดิม,
   `DROP TABLE` ปลอมทำอะไรไม่ได้) ผ่าน
2. รันชุดทดสอบเสร็จแล้วต้องเขียว 100% รวม backward
   compatibility JSON เดิม → `pytest test_app.py -q` =
   **14 passed** (5 เดิม + 9 ใหม่), regression
   `Phase4/Sprint4/week-12/test_app.py` = **25 passed**;
   เทสต์ `test_backward_compat_legacy_json_keys` ยืนยันไฟล์
   เก่าไร้ `barcode` โหลดได้ไม่ `KeyError`

## ชุดทดสอบใหม่ 9 เคส (ใน `test_app.py`)

| เคส | ครอบคลุม |
|---|---|
| `test_singleton_same_instance` | SPM-23 Singleton |
| `test_parameterized_blocks_sql_injection` | SPM-23 injection |
| `test_migrate_json_to_sqlite_verifies` | SPM-24 migrate+verify |
| `test_member_crud_four_tiers` | SPM-25 CRUD 4 tiers |
| `test_member_invalid_tier_fallback_regular` | SPM-25 fallback |
| `test_checkout_gold_discount_receipt` | SPM-26 Gold 1000→900 |
| `test_checkout_guest_full_price_and_stock_cut` | SPM-26 guest/stock |
| `test_checkout_keeps_reorder_alert` | SPM-26 alert |
| `test_backward_compat_legacy_json_keys` | BUG-101 regression |

- `flake8 app.py` clean (exit 0, ไร้ `E501`), `bandit` 0 issues
- fixture `sqlite_ctx`/`repo`/`members`/`checkout` แยก DB
  ต่อเทสต์ด้วย `tmp_path` + `reset()` กัน singleton รั่วข้ามเคส
