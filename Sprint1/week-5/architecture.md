# สถาปัตยกรรมระบบ (System Architecture)

เอกสารนี้แสดงการเปรียบเทียบสถาปัตยกรรมของระบบคลังสินค้าเดิม (As-is) และระบบคลังสินค้าใหม่ (To-be) ตามที่ได้วางแผนไว้

---

## 1. ผังงานระบบเดิม (As-is Architecture Flowchart)
ผังงาน (Flowchart) แสดงกระบวนการทำงานของระบบแบบ Monolithic Script ที่ใช้ JSON เป็นฐานข้อมูลชั่วคราว ขาดการดักจับข้อผิดพลาดและโครงสร้างแบบ OOP

```mermaid
flowchart TD
    Start([เริ่มโปรแกรม]) --> LoadDB[/"โหลดข้อมูลจากไฟล์ data.json"/]
    LoadDB --> Menu{"แสดงเมนูหลัก"}
    
    Menu -->|เลือก 1| Show["วนลูปแสดงรายการสินค้าทั้งหมด"]
    Menu -->|เลือก 2| Add[/"รับค่า 'ชื่อสินค้า' และ 'จำนวนเพิ่ม'"/]
    Menu -->|เลือก 3| Withdraw[/"รับค่า 'ชื่อสินค้า' และ 'จำนวนเบิก'"/]
    Menu -->|เลือก 4| Exit(["จบการทำงาน"])
    
    Add --> ProcessAdd["อัปเดต Dictionary ของสินค้าในหน่วยความจำ"]
    Withdraw --> ProcessWithdraw["ลดจำนวนสินค้าใน Dictionary"]
    
    ProcessAdd --> SaveDB["เขียนข้อมูลทับไฟล์ data.json (Overwrite)"]
    ProcessWithdraw --> SaveDB
    
    Show --> Menu
    SaveDB --> Menu

    classDef hotspot fill:##ff0000,stroke:#ff0000,stroke-width:2px;
    class SaveDB,LoadDB hotspot
```

---

## 2. โครงสร้างคลาสระบบใหม่ (To-be Architecture UML Class Diagram)
แผนภาพคลาส (UML Class Diagram) สำหรับระบบใหม่ที่ถูกจัดโครงสร้างใหม่เป็นแบบเชิงวัตถุ (OOP) นำ SQLite มาใช้เพื่อให้รองรับ Transaction และเพิ่มระบบสมาชิกลดราคา (Membership System)

```mermaid
classDiagram
    class SystemCLI {
        <<Facade>>
        -db_manager: DatabaseManager
        +start()
        +display_menu()
        +handle_input()
    }
    
    class DatabaseManager {
        <<Singleton>>
        -db_connection: sqlite3.Connection
        +connect()
        +commit_transaction()
        +rollback_transaction()
        +close()
    }
    
    class ProductManager {
        <<Service>>
        +fetch_all_products()
        +update_stock(product_id: int, qty: int)
        -validate_input(qty: int)
    }
    
    class MemberSystem {
        <<Strategy Context>>
        +get_member_tier(member_id: int): String
        +get_discount_rate(tier: String): float
    }
    
    class CheckoutProcess {
        <<Controller>>
        +calculate_net_price(subtotal: float, discount_rate: float): float
        +generate_receipt()
    }
    
    SystemCLI --> DatabaseManager : Initialize DB
    SystemCLI --> ProductManager : delegates Product tasks
    SystemCLI --> MemberSystem : identifies Member
    ProductManager --> DatabaseManager : executes SQL Queries
    MemberSystem --> DatabaseManager : executes SQL Queries
    SystemCLI --> CheckoutProcess : orchestrates checkout
```
