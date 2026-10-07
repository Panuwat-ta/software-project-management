#!/usr/bin/env python3
from pathlib import Path
from html import escape

ROOT = Path("/home/panuwat/work/software-project-management")

CSS = r"""
:root{--font:"Noto Sans Thai","Leelawadee UI",system-ui,sans-serif;--bg:#e7eeee;--paper:#fff;--ink:#122a38;--muted:#49616b;--accent:#0867a1;--line:#bfd0d4;--soft:#e8f3f8}
*{box-sizing:border-box}
body{margin:0;font-family:var(--font);color:var(--ink);background:var(--bg);min-height:100vh;display:grid;grid-template-rows:auto 1fr auto}
a:focus-visible,button:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
.deck-header,.deck-controls{width:min(1440px,calc(100% - 48px));margin:auto;display:flex;align-items:center;justify-content:space-between;gap:18px;color:var(--muted);font-size:14px}
.deck-header{padding:18px 0}.deck-controls{padding:18px 0}
.back-link{color:var(--accent);font-weight:700;text-decoration:none}
.deck-controls button{min-height:44px;padding:10px 16px;border:1px solid var(--line);background:var(--paper);color:var(--ink);font:700 15px var(--font);cursor:pointer}
.deck-controls button:disabled{opacity:.35;cursor:default}.deck-controls button:hover:not(:disabled){background:var(--accent);border-color:var(--accent);color:#fff}
.deck-frame{width:min(1440px,calc(100vw - 48px),calc((100vh - 132px) * 16 / 9));aspect-ratio:16/9;margin:auto;overflow:hidden;background:var(--paper);box-shadow:0 18px 46px rgb(18 42 56 / 18%)}
.slide{display:none;height:100%;padding:3.5% 4.5%;align-content:center}
.slide.active{display:grid}
.slide h1{margin:0;letter-spacing:-.04em;line-height:1.08;font-size:clamp(36px,5vw,76px)}
.slide h2{margin:0;letter-spacing:-.04em;line-height:1.08;font-size:clamp(24px,2.4vw,34px)}
.slide-label{margin:0 0 20px;color:var(--accent);font-weight:800}
.slide-lead{max-width:50ch;margin:10px 0 0;color:var(--muted);font-size:clamp(17px,1.8vw,26px);line-height:1.45}
.cover-meta{margin:0;padding:14px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);color:var(--muted);line-height:1.7}
.cover-layout,.content-layout{display:grid;grid-template-columns:1.12fr .88fr;gap:7%;align-items:center}
.rule-list{margin:0;padding:0;list-style:none;border-top:1px solid var(--line)}
.rule-list li{display:grid;grid-template-columns:32% 1fr;gap:18px;padding:10px 0;border-bottom:1px solid var(--line)}
.rule-list strong{color:var(--accent)}
table{width:100%;margin-top:16px;border-collapse:collapse;font-size:clamp(14px,1.45vw,21px)}
th{padding:8px 14px;font-size:20px;background:var(--ink);color:#fff;text-align:left}
td{padding:8px 14px;font-size:20px;border-bottom:1px solid var(--line)}
tbody tr:nth-child(even){background:#f3f7f7}
.metrics{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.metrics div{padding:14px 18px;border-right:1px solid var(--line)}
.metrics div:last-child{border:0}
.metrics b{display:block;font-size:clamp(26px,3.2vw,44px);letter-spacing:-.05em}
.metrics span{display:block;margin-top:9px;color:var(--muted)}
.next-steps{margin:0;padding-left:1.2em}
.next-steps li{padding:8px 0;color:var(--muted);font-size:clamp(16px,1.6vw,24px)}
@media (max-width:720px){.deck-header,.deck-controls{width:calc(100% - 32px);flex-wrap:wrap}.deck-frame{width:100%;aspect-ratio:auto;overflow:visible;box-shadow:none}.slide{height:auto;min-height:70vh}.cover-layout,.content-layout{grid-template-columns:1fr;gap:20px}.rule-list li{grid-template-columns:1fr;gap:4px}.metrics{grid-template-columns:1fr}th,td{padding:8px 10px}}
@media print{@page{size:13.333in 7.5in;margin:0}.deck-header,.deck-controls{display:none}.deck-frame{width:13.333in;height:auto;aspect-ratio:auto;overflow:visible;box-shadow:none}.slide{display:grid;break-after:page;width:13.333in;height:7.5in;padding:.42in .60in}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto !important}}
"""

JS = r"""
(function(){
var slides=Array.prototype.slice.call(document.querySelectorAll(".slide"));
var count=document.getElementById("slide-counter");
var storageKey=STORAGE_KEY;
function slideFromHash(){var m=/#slide-(\d+)/.exec(window.location.hash||"");if(!m)return null;var i=parseInt(m[1],10)-1;return(i>=0&&i<slides.length)?i:null;}
function storedSlide(){try{var v=window.localStorage.getItem(storageKey);if(v===null)return null;var i=parseInt(v,10);return(i>=0&&i<slides.length)?i:null;}catch(err){return null;}}
function rememberSlide(i){try{window.localStorage.setItem(storageKey,String(i));}catch(err){}}
var current=slideFromHash();if(current===null)current=storedSlide();if(current===null)current=0;
function show(i){current=Math.min(Math.max(i,0),slides.length-1);slides.forEach(function(s,n){s.classList.toggle("active",n===current);});if(count)count.textContent=(current+1)+" / "+slides.length;previousBtn.disabled=current===0;nextBtn.disabled=current===slides.length-1;rememberSlide(current);try{window.history.replaceState(null,"","#slide-"+(current+1));}catch(err){}}
function showFromHash(){var i=slideFromHash();if(i!==null)show(i);}
var previousBtn=document.getElementById("previous");var nextBtn=document.getElementById("next");
previousBtn.addEventListener("click",function(){show(current-1);});nextBtn.addEventListener("click",function(){show(current+1);});
document.addEventListener("keydown",function(e){if(e.key==="ArrowRight"||e.key==="PageDown"||e.key===" "){e.preventDefault();show(current+1);}else if(e.key==="ArrowLeft"||e.key==="PageUp"){e.preventDefault();show(current-1);}else if(e.key==="Home"){e.preventDefault();show(0);}else if(e.key==="End"){e.preventDefault();show(slides.length-1);}});
window.addEventListener("hashchange",showFromHash);show(current);
})();
"""

def cover(label, title, lead, meta):
    return f'''<div class="cover-layout"><div><p class="slide-label">{label}</p><h1>{title}</h1><p class="slide-lead">{lead}</p></div><p class="cover-meta">{meta}</p></div>'''

def table_slide(title, lead, headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'''<h2>{title}</h2><p class="slide-lead">{lead}</p><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'''

def rules_slide(title, lead, items):
    lis = "".join(f"<li><strong>{a}</strong><span>{b}</span></li>" for a,b in items)
    return f'''<div class="content-layout"><div><h2>{title}</h2><p class="slide-lead">{lead}</p></div><ul class="rule-list">{lis}</ul></div>'''

def metrics_slide(title, lead, metrics):
    blocks = "".join(f"<div><b>{v}</b><span>{l}</span></div>" for v,l in metrics)
    return f'''<h2>{title}</h2><p class="slide-lead">{lead}</p><div class="metrics">{blocks}</div>'''

def end_slide(title, lead, steps):
    li = "".join(f"<li>{s}</li>" for s in steps)
    return f'''<div class="cover-layout"><div><h2>{title}</h2><p class="slide-lead">{lead}</p></div><ol class="next-steps">{li}</ol></div>'''

DECKS = {
1: {
"path":"Phase1/Sprint1/slides.html",
"title":"สไลด์ Sprint 1: เริ่มโครงการและวางฐาน | SPM",
"desc":"สไลด์สรุป Sprint 1 Phase 1 เริ่มโครงการ วิเคราะห์ระบบเดิม refactor และทดสอบ",
"back":"sprint1.html",
"back_text":"← รายงาน Sprint 1",
"aria":"สไลด์สรุป Sprint 1",
"slides":[
cover("Sprint 1 · Phase 1 · W1–W4","เริ่มโครงการ<br>และวางฐาน","จาก Project Charter และการวิเคราะห์ระบบเดิม สู่ OOP, validation, atomic write และ PyTest ที่รันซ้ำได้","15 SP · SPM-6…SPM-10<br>Jira Sprint ID 84 · state: closed<br>ข้อมูลสมมติเพื่อการเรียน"),
table_slide("4 สัปดาห์เปลี่ยนระบบเดิมให้มีฐานที่ตรวจสอบได้","ที่มา: sprint1.md ส่วนงานรายสัปดาห์",["สัปดาห์","งานหลัก","ผลลัพธ์"],[["W1","Charter · Scope · ระบบเดิม 5 เมนู","เห็นความเสี่ยงและขอบเขต"],["W2","DFD · Hotspot · Static Analysis · Blueprint","ได้แบบ refactor"],["W3","OOP 3 คลาส · Validation · Atomic Save","ได้โค้ดรุ่นใหม่ + DoD/RACI"],["W4","PyTest และปรับรอบสุดท้าย","5/5 tests ผ่าน"]]),
rules_slide("Refactor แก้ 4 จุดเสี่ยงหลักของระบบเดิม","จาก Monolithic ที่พึ่ง global state ไปสู่โครงสร้างแยกหน้าที่",[("โครงสร้าง","Product / InventoryManager / InventoryCLI แยก Business Logic ออกจาก UI"),("การบันทึก","เขียนไฟล์ชั่วคราวแล้ว os.replace ลดความเสี่ยงไฟล์เสีย"),("Input","validator ต่อช่อง กันค่าติดลบและ ValueError"),("ข้อมูลเก่า","Product.from_dict รองรับ n/q/p/c และค่า default")]),
table_slide("Baseline ชี้ว่าปัญหาหลักอยู่ที่ maintainability","ที่มา: week-2/Static-Analysis.md — ตัวเลขนี้เป็นค่าก่อนปรับ",["ตัวชี้วัด","ค่า","ความหมาย"],[["Pylint","7.10 / 10","ยังมี convention issue"],["Cyclomatic Complexity main","14 (C)","สูงกว่าเป้า ≤ 8"],["Branches","17","สูงกว่าเกณฑ์ 12"],["Statements","55","ฟังก์ชันเดียวทำมากเกินไป"]]),
metrics_slide("ผลเทคนิคผ่าน แต่ EVM บอกว่าต้องคุม scope ให้ดีขึ้น","Sprint 1 ปิดฟังก์ชันหลักได้ แต่ใช้เวลา/ต้นทุนมากกว่าที่วางไว้",[("5 / 5","PyTest PASS"),("SV −1,000","ช้ากว่าแผน"),("CV −1,200","เกินงบ")]),
rules_slide("Definition of Done ทำให้คำว่า “เสร็จ” มีเกณฑ์เดียวกัน","DoD 5 ข้อถูกใช้เป็น quality gate ของงานส่งมอบ",[("Test","PyTest ผ่าน 100%"),("Code","PEP 8 และแยกชั้น"),("Safety","validation + atomic write + กันค่าติดลบ"),("Docs","docstrings และเอกสารอัปเดต"),("Review","Code Review + Approve")]),
rules_slide("งานที่ยังไม่จบถูกยกยอดอย่างมีหลักฐาน","ไม่ปิดเงียบ และไม่อ้างว่าพัฒนาแล้วถ้ายังเป็นแค่แบบออกแบบ",[("SQLite / Member / Checkout","ออกแบบแล้ว แต่ยังไม่ implement — ยกไป Sprint 5"),("CR-01 / CR-02 / BUG-101","ยกไป Sprint 3 เพื่อทำผ่าน Change Control"),("UAT / Tag","ยกไป Sprint 4"),("E501","เก็บใน snapshot และแก้โค้ดสดภายหลัง")]),
end_slide("Sprint 1 วางฐานให้ระบบพร้อมวิวัฒนาการต่อ","สิ่งสำคัญไม่ใช่แค่โค้ดทำงาน แต่ต้องมี baseline, test และเกณฑ์ส่งมอบ",["ใช้ To-Be architecture ต่อใน Sprint 2","คุมการเปลี่ยนแปลงจริงใน Sprint 3","ปิด UAT/Release ใน Sprint 4","นำ SQLite + Member + Checkout มาทำจริงใน Sprint 5"])
]},

2: {
"path":"Phase2/Sprint2/slides.html",
"title":"สไลด์ Sprint 2: ออกแบบและตั้งต้นทุนฐาน | SPM",
"desc":"สไลด์สรุป Sprint 2 Phase 2 To-Be Architecture ISO quality และ Cost Baseline",
"back":"sprint2.html","back_text":"← รายงาน Sprint 2","aria":"สไลด์สรุป Sprint 2",
"slides":[
cover("Sprint 2 · Phase 2 · W5–W7","ออกแบบระบบ<br>และตั้งต้นทุนฐาน","รอบนี้ยังไม่เร่งเขียนฟีเจอร์ แต่ล็อก To-Be Architecture, Quality Gate และ Cost Baseline ก่อนลงมือจริง","13 SP · SPM-11…SPM-14<br>Jira Sprint ID 82 · state: closed<br>ข้อมูลสมมติเพื่อการเรียน"),
table_slide("W5–W7 เปลี่ยนจากแนวคิดเป็นแผนที่ควบคุมได้","ที่มา: sprint2.md ส่วนงานรายสัปดาห์",["สัปดาห์","งานหลัก","ผลลัพธ์"],[["W5","As-Is vs To-Be · ISO 25010 · Budget worksheet","เห็น gap ด้านคุณภาพและต้นทุน"],["W6","Communication · DoR/DoD · Architecture · Variance","ได้กติกาและแบบสถาปัตยกรรม"],["W7","Cost Baseline · Capacity · ISO 14598","ได้ฐานงบและ quality gate"]]),
rules_slide("To-Be แยก 4 ชั้นเพื่อให้เปลี่ยน persistence ได้","แบบนี้ถูกนำไป implement จริงใน Sprint 5",[("Presentation","CLI / Web รับและแสดงผล ไม่ถือ SQL"),("Service","Checkout / Validation / Export เป็นงานเชิงธุรกิจ"),("Repository","ซ่อน CRUD / Summary และ parameterized SQL"),("Database","SQLite เก็บ products / members พร้อม transaction")]),
table_slide("ISO/IEC 25010 ชี้ 3 มิติที่ต้องแก้เชิงโครงสร้าง","ประเมิน As-Is ก่อนพัฒนา เพื่อให้การปรับมีเป้าหมายวัดได้",["มิติ","สถานะ","แนวทาง"],[["Usability","ต้องปรับ","validator + เมนูชัดขึ้น"],["Reliability","ตก","atomic write → SQLite"],["Security","ตก","parameterized query 100%"],["Maintainability","ตก","แยกชั้น + OOP"]]),
metrics_slide("Cost Baseline ที่อนุมัติคือ 18,823 บาท","ใช้ตัวเลข W7 เป็นฐานควบคุมงบ ไม่ปนกับ worksheet ชุด W5",[("15,000","ค่าแรง"),("1,000","Infrastructure"),("2,823","Reserve")]),
rules_slide("Baseline มี threshold และ capacity ไม่ใช่แค่ยอดเงิน","ทีมต้องรู้ว่าเมื่อไรควรเตือนและเมื่อไรควรตัด scope",[("Budget Threshold","≤5% ปกติ · 5–10% เตือน · >10% วิกฤต"),("Capacity","3 คน × 6 ชม. × 2 สัปดาห์ = 36 man-hours"),("Quality","v(G) ≤ 8 · CBO ≤ 4 · DIT ≤ 2 · Coverage ≥ 85%"),("DoR/DoD","งานเข้า Sprint ต้องพร้อม และงานออกต้องผ่าน review/test/docs")]),
table_slide("ตัวอย่าง Cost Variance เตือนว่าการ migration มีต้นทุนแฝง","กรณี JSON → SQLite ในการวิเคราะห์ W6",["ตัวแปร","ค่า","ผล"],[["PV","2,400 THB","งบตามแผน"],["EV","2,400 THB","งานเสร็จตาม DoD"],["AC","4,000 THB","ใช้จริงสูงกว่าแผน"],["CV","−1,600 THB","ต้องพิจารณา reserve / replan"]]),
end_slide("Sprint 2 ทำให้การพัฒนารอบต่อไปมีกรอบตัดสินใจ","Architecture, quality และ cost ถูกเชื่อมเข้าด้วยกันก่อนรับงานเปลี่ยนแปลงจริง",["รับ CR-01 ด้วย Impact Analysis","ติดตาม Burndown / EVM ด้วย Log Work จริง","วัด quality gate ในช่วง Hardening","รักษาฐานงบ 18,823 THB ให้เป็นแหล่งอ้างอิงเดียว"])
]},

3: {
"path":"Phase3/Sprint3/slides.html",
"title":"สไลด์ Sprint 3: ลงมือและคุมการเปลี่ยนแปลง | SPM",
"desc":"สไลด์สรุป Sprint 3 Change Control CR-01 CR-02 BUG-101 EVM Hardening Scope Freeze",
"back":"sprint3.html","back_text":"← รายงาน Sprint 3","aria":"สไลด์สรุป Sprint 3",
"slides":[
cover("Sprint 3 · Phase 3 · W8–W11","ลงมือจริง<br>และคุมการเปลี่ยนแปลง","Change Request ทุกใบต้องมี Impact Analysis, CCB, ต้นทุน และ test — ไม่เพิ่ม scope แบบเงียบ ๆ","16 SP · SPM-15…SPM-19<br>Jira Sprint ID 85 · state: closed<br>ข้อมูลสมมติเพื่อการเรียน"),
table_slide("W8–W11 เดินงานจาก Change Request ไปสู่ Scope Freeze","ที่มา: sprint3.md ส่วนงานรายสัปดาห์",["สัปดาห์","งานหลัก","หลักฐานสำคัญ"],[["W8","CR-01 · Burndown · Stakeholder · Procurement","Impact Analysis"],["W9","EVM · Retrospective · Transition","EVM / Retro"],["W10","CR-02 · CCB · BUG-101 · Reserve","Decision / Defect Log"],["W11","Hardening · Flow/WIP · Scope Freeze","Hardening Report"]]),
rules_slide("Change Control 4 ขั้นตัดสินใจด้วยผลกระทบ ไม่ใช่ความรู้สึก","ใช้กระบวนการเดียวกันกับคำขอที่เพิ่ม scope",[("1 · Submit","บันทึกคำขอและเหตุผล"),("2 · Impact","ประเมินคน เวลา สถาปัตยกรรม และ test"),("3 · CCB Review","Sponsor / User Rep / PM / Tech Lead อนุมัติหรือปฏิเสธ"),("4 · Baseline","อัปเดต scope / cost / schedule หลังอนุมัติ")]),
table_slide("CR-01 และ CR-02 ถูกอนุมัติด้วยข้อมูลคนละแบบ","ทั้งสองใบมีผลต่อ scope แต่เส้นทางตัดสินใจต่างกัน",["รายการ","CR-01 Barcode + ROP","CR-02 CSV Export"],[["ประเภท","Perfective / Normal","Perfective / Fast-Track"],["Impact","+8 man-hours","4.5 h = 1,350 THB"],["ตำแหน่งแก้","Product + Repository + UI","CsvReportExporter"],["การเงิน","เลื่อนไปรอบถัดไป","เบิก Reserve"]]),
rules_slide("BUG-101 ถูกแก้ที่ root cause และล็อกด้วย regression test","อาการ crash จากข้อมูลรุ่นเก่ากลายเป็น test ถาวร",[("อาการ","KeyError: barcode เมื่ออ่าน data.json รุ่นเก่า"),("5 Whys","schema ใหม่ไม่มี default fallback ใน Repository"),("Fix","dict.get('barcode','') และ reorder_point default 5"),("Prevention","Defect-driven test + backward compatibility test")]),
metrics_slide("ก่อน freeze ระบบไปถึง 27 / 29 points","เหลือ 2 points และกำหนด WIP เพื่อไม่ให้งานค้างสะสม",[("27 / 29","Burnup = 93%"),("WIP 3","Review limit"),("1,350 THB","Reserve ที่ใช้")]),
table_slide("Retrospective เปลี่ยนปัญหาเป็น action ที่วัดได้","Mad / Sad / Glad ไม่จบแค่การเล่า",["ด้าน","สิ่งที่พบ","Action"],[["Mad","Merge conflict จากเปลี่ยนโครงสร้างใหญ่","แจ้ง blocker ทุก daily"],["Sad","ประเมิน refactor ต่ำกว่าจริง","ทบทวน hidden technical debt"],["Glad","PyTest จับบั๊กก่อน demo","คง automated test เป็น gate"],["Action","PR ค้าง review","review ภายใน 12 ชั่วโมง + TDR"]]),
rules_slide("Scope Freeze ป้องกันงานงอกก่อน UAT","หลัง freeze รับเฉพาะสิ่งที่ปกป้องคุณภาพ release",[("ขอบเขตล็อก","29 story points"),("อนุญาต","Critical bug · Security fix · Test"),("ไม่อนุญาต","ฟีเจอร์ใหม่ · เปลี่ยน UI · CR ใหม่"),("เงื่อนไขออก","งาน 27/29 + hardening + lint/deck gate")]),
end_slide("Sprint 3 ทำให้การเปลี่ยนแปลงตรวจสอบย้อนหลังได้","CR, defect, cost และ flow ถูกเชื่อมเป็นหลักฐานชุดเดียว",["ปิด 29/29 ก่อน UAT","รัน SC01–SC03 ใน Sprint 4","ผ่าน Release Checklist และ Final EVM","ยก migration เต็มรูปแบบไป Sprint 5"])
]},

4: {
"path":"Phase4/Sprint4/slides.html",
"title":"สไลด์ Sprint 4: UAT และปล่อย v2.0 | SPM",
"desc":"สไลด์สรุป Sprint 4 UAT Release Checklist Final EVM และ v2.0.0-evolution",
"back":"sprint4.html","back_text":"← รายงาน Sprint 4","aria":"สไลด์สรุป Sprint 4",
"slides":[
cover("Sprint 4 · Phase 4 · W12","UAT และปล่อย<br>v2.0.0-evolution","ปิดวงจร W1–W12 ด้วย acceptance scenario, regression 25 เคส, release gate และ Final EVM","5 SP · SPM-20 / SPM-21<br>Jira Sprint ID 83 · state: closed<br>ข้อมูลสมมติเพื่อการเรียน"),
table_slide("v2.0 เปลี่ยนทั้งโครงสร้าง ฟีเจอร์ และความสามารถทดสอบ","เทียบสิ่งที่ส่งมอบกับ v1.0",["รายการ","v1.0","v2.0.0-evolution"],[["Persistence","JSON เขียนทับตรง","JSON + atomic write"],["Architecture","Monolithic + global x","OOP 3 คลาส"],["Inventory","ไม่มี Barcode/ROP","Barcode + Reorder Point"],["Reporting","ไม่มี CSV","CsvReportExporter"],["Tests","5 เคส","25 เคส"]]),
metrics_slide("Regression 25 เคสผ่านครบก่อนปล่อย","ชุดทดสอบครอบคลุม baseline, CR, defect, CLI และ integration",[("25 / 25","Tests PASS"),("6 กลุ่ม","Test groups"),("0","Regression แตก")]),
table_slide("UAT SC01–SC03 ครอบคลุมวงจรรับสินค้า → ขาย → รายงาน","ผลทางเทคนิคผ่านครบ แต่ formal sign-off ยังรอลายเซ็น",["Scenario","การทดสอบ","ผล"],[["SC01 Inventory Manager","เพิ่ม Milk 10 · ROP 5","PASS"],["SC02 Store Cashier","ตัด 6 เหลือ 4 → low stock","PASS"],["SC03 Purchasing","Export CSV เปิด Excel","PASS"],["Formal Sign-off","ผู้ทดสอบ / Tech Lead","ยังรอลงนาม"]]),
rules_slide("Release Checklist มี 3 ด่านก่อนเรียกว่าส่งมอบ","แต่ละด่านมีหลักฐานต่างกัน",[("Gate 1 · Quality","UAT SC01–03 ผ่าน + แยก defect / scope"),("Gate 2 · Technical","Regression 25/25 · PR develop→main · CI · merge"),("Gate 3 · Release","main · annotated tag · CHANGELOG · Final EVM")]),
table_slide("Final EVM ปิดตรงเวลา แต่เกินงบเล็กน้อย","ใช้ reserve เคลียร์ส่วนเกินโดยยอดคงเหลือไม่ติดลบ",["ตัวแปร","ค่า","ความหมาย"],[["PV / EV","15,525 / 15,525","SPI = 1.00 ตรงเวลา"],["AC","16,100","ต้นทุนจริง"],["CPI","0.96","ประสิทธิภาพต้นทุนต่ำกว่า 1"],["CV","−575 THB","เกินงบ 3.7%"],["Reserve เหลือ","898 THB","หลัง CR-02 และ close-out"]]),
rules_slide("CHANGELOG บอกว่ารุ่นนี้เปลี่ยนอะไรจริง","Release note ต้องสะท้อน code และ test ที่ส่งมอบ",[("Added","Barcode · Reorder Alert · CSV Export"),("Changed","Product schema + หมายเลขเมนู"),("Removed","global x"),("Fixed","BUG-101 รองรับ legacy key + default")]),
rules_slide("ข้อจำกัดที่ยังเหลือถูกส่งต่ออย่างตรงไปตรงมา","การผ่าน UAT ทางเทคนิคไม่ได้แปลว่าทุกงานใน roadmap จบแล้ว",[("UAT sign-off","ยังรอลายเซ็นทางการ"),("Legacy data","fallback ยังไม่ใช่ migration เต็ม"),("E501","ยังค้างใน snapshot รุ่นนี้"),("SQLite / Member","ยังเป็น design — ยกไป Sprint 5")]),
end_slide("Sprint 4 ปิด v2.0 และเปิดทางให้ evolution รอบใหม่","รุ่น v2.0.0-evolution มี tag และผ่าน technical gate แล้ว",["นำ SQLite + Member + Checkout มาทำจริง","แก้ E501 ในโค้ดสด","รักษา 25 regression tests ไม่ให้แตก","ต่อยอด UI เป็นโปรแกรม Desktop โดย reuse domain"])
]},

5: {
"path":"Phase5/Sprint5/slides.html",
"title":"สไลด์ Sprint 5: v3.0 และ Desktop Program | SPM",
"desc":"สไลด์สรุป Sprint 5 SQLite Member Checkout GTK4 Desktop Program และ Quality Gate",
"back":"sprint5.html","back_text":"← รายงาน Sprint 5","aria":"สไลด์สรุป Sprint 5",
"slides":[
cover("Sprint 5 · Phase 5 · v3.0 + Desktop","จาก CLI สู่<br>โปรแกรม Desktop","ปิดงานออกแบบที่ค้างตั้งแต่ Sprint 1: SQLite, member discount, checkout และ Desktop UI โดยไม่ทำ regression","46 SP · 2 Epics · 9 Issues<br>Jira Sprint ID 86 · state: closed<br>ข้อมูลสมมติเพื่อการเรียน"),
table_slide("Sprint 5 แบ่งเป็น 2 Track แต่ใช้ domain เดียวกัน","ส่วน A ทำฐานธุรกิจให้แข็งแรง ส่วน B เพิ่มหน้าตาโปรแกรม Desktop",["Track","Story Points","งาน"],[["A · v3.0","17 SP","SQLite · Migration · Member · Checkout · Tests"],["B · Desktop Program","29 SP","GTK4 · Dashboard · Products · Members · Checkout"],["รวม","46 SP","SPM-23…27 + SPM-29…32"]]),
rules_slide("v3.0 ใช้ 3 pattern ลด coupling ของ data และ policy","CLI และ Desktop Program ใช้ business logic ชุดเดียว",[("Singleton","SQLiteDatabaseContext จัดการ connection / reset"),("Repository","InventoryRepository ซ่อน SQL และ persistence"),("Strategy","MemberTier แยก Regular / Silver / Gold / Platinum"),("Transaction","commit / rollback ทุก write ป้องกันข้อมูลค้างกลางทาง")]),
table_slide("Migration ต้องพิสูจน์ว่า data ไม่หายก่อนสลับระบบ","อ่าน legacy ผ่าน Product.from_dict แล้วตรวจผลก่อน/หลัง",["รายการ","ผล"],[["Legacy key","รองรับ n / q / p / c"],["Default ใหม่","barcode='' · reorder_point=5"],["Verification","เทียบ count + total value 100%"],["ตัวอย่าง","2 records · 600.0 → SQLite 600.0"],["Startup","ย้ายอัตโนมัติเมื่อ DB ยังว่าง"]]),
table_slide("Member Strategy ทำให้ส่วนลดเปลี่ยนได้โดยไม่กระจาย if-else","Checkout ใช้ policy เดียวทั้ง CLI และ Desktop UI",["Tier","ส่วนลด","ซื้อ 1,000 บาท"],[["Regular","0%","1,000"],["Silver","5%","950"],["Gold","10%","900"],["Platinum","15%","850"]]),
rules_slide("Desktop UI เป็น presentation layer ที่บาง","program.py reuse domain เดิมทั้งหมด",[("Toolkit","GTK4 / PyGObject"),("หน้าจอ","Dashboard · Products · Members · Checkout"),("Run","python3 program.py"),("Domain","Repository · MemberManager · CheckoutService · CSV")]),
table_slide("หน้าตาโปรแกรมทำงานผ่าน domain จริง","ไม่ต้องเปิด browser หรือรัน server",["หน้าจอ","ความสามารถ"],[["Dashboard","ประเภทสินค้า · มูลค่ารวม · low-stock"],["Products","ค้นหา · เพิ่ม/แก้ไข · ตัด · ลบ · CSV"],["Members","CRUD + 4 tiers"],["Checkout","ส่วนลด + ใบเสร็จ + stock คงเหลือ"]]),
metrics_slide("Quality Gate ผ่านทั้งชุดใหม่และ regression เดิม","การเพิ่ม Desktop Program ไม่ทำให้ v2.0 เสีย",[("21 / 21","Main tests"),("25 / 25","v2 Regression"),("0 / 0","Flake8 / Bandit")]),
rules_slide("Desktop Program ถูกเปิดรันจริงก่อนส่งมอบ","QA ยืนยัน runtime และ Responsive ไม่ใช่ตรวจ static อย่างเดียว",[("Runtime","เปิด GTK4 window บน GNOME/Wayland"),("Responsive","Desktop ≥980 · Compact 760–979 · Narrow <760"),("Tests","test_program.py 7 integration cases · รวม responsive breakpoints"),("Tables","หน้าต่างแคบใช้ horizontal scroll ไม่บีบข้อมูล")]),
rules_slide("ข้อจำกัดของ Desktop build ถูกระบุไว้ชัด","สิ่งที่อยู่นอก scope ไม่ถูกอ้างว่าเป็น feature",[("Auth","ไม่มี Login / Role-based access"),("Payment","ไม่มี Online Payment"),("Concurrency","SQLite เหมาะ local single-user"),("Packaging","ยังเป็น .py; installer/executable เป็นงานต่อไป")]),
end_slide("Sprint 5 ปิดวงจรจาก CLI สู่โปรแกรม Desktop","Architecture ที่แยกชั้นทำให้เพิ่ม UI ได้โดย reuse Repository และ Strategy",["เพิ่ม Member tier ใหม่ได้ด้วย Strategy","ทำ installer/executable ได้ภายหลัง","ปิด UAT sign-off","คง regression gate 21 + 25 tests ทุก release"])
]}
}

def build(num, d):
    slides = "\n".join(
        f'<section class="slide{" active" if i == 1 else ""}" id="slide-{i}">\n{body}\n</section>'
        for i, body in enumerate(d["slides"], 1)
    )
    js = JS.replace("STORAGE_KEY", repr(f"spm-sprint-{num}-summary-slides"))
    html = f'''<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{escape(d["desc"], quote=True)}">
<title>{d["title"]}</title>
<style>{CSS}</style>
</head>
<body>
<header class="deck-header"><a class="back-link" href="{d["back"]}">{d["back_text"]}</a><span id="slide-counter" aria-live="polite">1 / {len(d["slides"])}</span></header>
<main class="deck-frame" aria-label="{d["aria"]}">
{slides}
</main>
<footer class="deck-controls"><button id="previous" type="button" aria-label="สไลด์ก่อนหน้า">← ก่อนหน้า</button><button id="next" type="button" aria-label="สไลด์ถัดไป">ถัดไป →</button></footer>
<script>{js}</script>
</body>
</html>
'''
    path = ROOT / d["path"]
    path.write_text(html, encoding="utf-8")
    print(f"built {path.relative_to(ROOT)} ({len(d['slides'])} slides)")

for num,d in DECKS.items():
    build(num,d)
