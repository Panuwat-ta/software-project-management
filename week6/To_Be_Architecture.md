# แผนภาพสถาปัตยกรรม To-Be (To-Be Architecture Class Diagram)

เอกสารนี้อธิบายสถาปัตยกรรมเป้าหมายของระบบคลังสินค้าที่ถูกปรับปรุง (Refactor) จากสคริปต์ `app_v1.py` แบบดั้งเดิม ไปสู่สถาปัตยกรรมที่รองรับ **SQLite Database** และ **ระบบสมาชิก (Member System)** ตามแผนงาน Evolution ในโปรเจค

## แผนภาพคลาส (Mermaid Class Diagram)

```mermaid
classDiagram
    class Product {
        -String id
        -String name
        -int qty
        -float price
        -String category
        +to_dict() dict
    }

    class MemberTier {
        <<Interface>>
        +getDiscountRate() float
    }

    class RegularMember {
        +getDiscountRate() float : 0.0
    }

    class SilverMember {
        +getDiscountRate() float : 0.05
    }

    class GoldMember {
        +getDiscountRate() float : 0.10
    }

    class PlatinumMember {
        +getDiscountRate() float : 0.15
    }

    MemberTier <|-- RegularMember
    MemberTier <|-- SilverMember
    MemberTier <|-- GoldMember
    MemberTier <|-- PlatinumMember

    class SQLiteDatabaseContext {
        <<Singleton Pattern>>
        -static SQLiteDatabaseContext instance
        -String db_path
        -Connection conn
        -SQLiteDatabaseContext()
        +static getInstance() SQLiteDatabaseContext
        +execute(query, params) Cursor
        +commit() void
    }

    class InventoryRepository {
        <<Repository Pattern>>
        -SQLiteDatabaseContext db
        +save(Product) void
        +findById(String id) Product
        +findAll() List~Product~
        +updateStock(String id, int amount) void
    }

    class CheckoutService {
        -InventoryRepository repo
        +calculateTotalWithDiscount(Product, MemberTier, qty) float
        +processCheckout(String productId, MemberTier, qty) receipt
    }

    class CLI_PresentationLayer {
        -InventoryRepository inventory
        -CheckoutService checkout
        +run() void
        +handleInput() void
    }

    CLI_PresentationLayer --> CheckoutService : เรียกใช้งาน (Checkout)
    CLI_PresentationLayer --> InventoryRepository : เรียกใช้งาน (CRUD)
    CheckoutService --> InventoryRepository : ใช้งานฐานข้อมูล
    CheckoutService --> MemberTier : คำนวณส่วนลด
    InventoryRepository --> SQLiteDatabaseContext : จัดการ Transaction
    InventoryRepository --> Product : จัดการ Model
```

## คำอธิบาย Architecture และ Patterns

1. **Repository Pattern (`InventoryRepository`)**: ทำหน้าที่ครอบระบบฐานข้อมูล SQLite เอาไว้ ทำให้ส่วนอื่นๆ ของโปรแกรม เช่น `CheckoutService` และ `CLI_PresentationLayer` ไม่ต้องเขียนคำสั่ง SQL โดยตรง ลดช่องโหว่ SQL Injection ผ่าน Parameterized Query
2. **Singleton Pattern (`SQLiteDatabaseContext`)**: ควบคุมให้มีจุดเชื่อมต่อฐานข้อมูลเพียงจุดเดียว ป้องกันปัญหา Database Locked เมื่อมีการเรียกเขียนไฟล์พร้อมๆ กัน (แก้ปัญหาการใช้ `with open()` ซ้ำซ้อนในโค้ดเก่า)
3. **Strategy Pattern (`MemberTier`)**: ออกแบบระบบสมาชิกให้แต่ละระดับ (Tier) แยกจากกันอย่างชัดเจน ทำให้เราสามารถเพิ่มสมาชิกระดับใหม่ (เช่น Diamond) ในอนาคตได้ทันทีโดยไม่ต้องไปยุ่งกับคำสั่ง `if-else` ที่วุ่นวายในหน้า Checkout
