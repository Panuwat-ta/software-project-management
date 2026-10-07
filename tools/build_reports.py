#!/usr/bin/env python3
"""สร้างหน้า HTML จากรายงาน Markdown ของทุก Phase/Sprint

ใช้เพื่อให้เปิดดูรายงานบน GitHub Pages ได้
(Markdown ไม่ถูก render เป็นหน้าเว็บโดยตรง)

ใช้งาน:
    python3 tools/build_reports.py            # สร้าง HTML ทั้งหมด
    python3 tools/build_reports.py --check    # ตรวจว่า HTML ตรงกับ md ไหม
    python3 tools/build_reports.py --pdf      # PDF รายงานปิด Sprint/Phase
"""

import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPORT_GLOBS = (
    "Phase*/phase*-report.md",
    "Phase*/Sprint*/sprint*.md",
    "Phase*/Sprint*/SPM-*.md",
    "Phase*/Sprint*/web-plan.md",
    "Phase*/Sprint*/program-plan.md",
    "Phase*/README.md",
    "Phase*/Sprint*/web/README.md",
)
PHASES = ["Phase1", "Phase2", "Phase3", "Phase4", "Phase5"]
PDF_PATTERNS = ("Phase*/phase*-report.md", "Phase*/Sprint*/sprint*.md")
PDF_SOURCES = {
    p.relative_to(ROOT).as_posix()
    for pattern in PDF_PATTERNS
    for p in ROOT.glob(pattern)
    if p.is_file()
}

CSS = """@page { size: A4; margin: 18mm 16mm; }
body { font-family: "Noto Sans Thai", "Liberation Sans", sans-serif;
  font-size: 11pt; line-height: 1.7; color: #1a1a1a; max-width: 900px;
  margin: 0 auto; padding: 24px 20px 60px; }
h1 { font-size: 22pt; border-bottom: 3px solid #1a56db; padding-bottom: 8px; }
h2 { font-size: 14pt; color: #1a56db; margin-top: 1.6em;
  border-bottom: 1px solid #e5e7eb; padding-bottom: 4px; }
h3 { font-size: 12pt; margin-top: 1.2em; }
table { border-collapse: collapse; width: 100%; margin: 0.9em 0;
  font-size: 9.5pt; }
th, td { border: 1px solid #cbd5e1; padding: 6px 9px; text-align: left;
  vertical-align: top; }
th { background: #eef2ff; }
tr:nth-child(even) td { background: #fafbff; }
code { font-family: "Noto Sans Mono", monospace; font-size: 9pt;
  background: #f3f4f6; padding: 1px 5px; border-radius: 3px; }
pre { background: #f3f4f6; padding: 12px; border-radius: 6px;
  overflow-x: auto; font-size: 8.5pt; line-height: 1.5; }
pre code { background: none; padding: 0; }
blockquote { margin: 1em 0; padding: 8px 14px; border-left: 4px solid #1a56db;
  background: #f5f8ff; }
.nav { background: #1a1a2e; color: #fff; padding: 10px 16px;
  border-radius: 8px; margin-bottom: 20px; font-size: 13px; }
.nav a { color: #c7d6ff; text-decoration: none; margin-right: 14px; }
.nav a:hover { color: #fff; text-decoration: underline; }
.note { color: #5b6472; font-size: 10pt; margin-top: 40px;
  border-top: 1px solid #e5e7eb; padding-top: 10px; }
@media print { .nav { display: none; } }"""


def up_prefix(report: pathlib.Path) -> str:
    """Relative prefix from a report file back to the repo root."""
    depth = len(report.relative_to(ROOT).parts) - 1
    return "../" * depth


def nav_html(report: pathlib.Path, depth: str) -> str:
    """Build the phase navigation bar for a report page."""
    phase = report.relative_to(ROOT).parts[0]
    links = [f'<a href="{depth}index.html">หน้าแรก</a>']
    for name in PHASES:
        current = " (หน้านี้)" if name == phase else ""
        links.append(
            f'<a href="{depth}{name}/README.html">{name}{current}</a>'
        )
    return '<nav class="nav">' + "".join(links) + "</nav>"


def render(md_path: pathlib.Path) -> str:
    """Render one Markdown report into a standalone HTML page."""
    depth = up_prefix(md_path)
    body = markdown.markdown(
        md_path.read_text(encoding="utf-8"),
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    rel = md_path.relative_to(ROOT).as_posix()
    pdf_link = ""
    if rel in PDF_SOURCES:
        pdf_link = (
            f'<p class="note">อ่านเป็น PDF: '
            f'<a href="{md_path.stem}.pdf">{md_path.stem}.pdf</a></p>\n'
        )
    return (
        "<!DOCTYPE html>\n"
        '<html lang="th">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width,\n'
        '      initial-scale=1.0">\n'
        f"<title>{md_path.stem.replace('-', ' ')} | SPM</title>\n"
        f'<link rel="stylesheet" href="{depth}theme.css">\n'
        f"<style>{CSS}</style>\n</head>\n<body>\n"
        f"{nav_html(md_path, depth)}\n{body}\n"
        f"{pdf_link}"
        '<p class="note">รายงานอัตโนมัติจาก '
        f"<code>{rel}</code> — ข้อมูลสมมติเพื่อการเรียน"
        " (สร้างด้วย <code>tools/build_reports.py</code>)</p>\n"
        "</body>\n</html>\n"
    )


def targets() -> list[pathlib.Path]:
    """Collect every report Markdown file in the Phase folders."""
    found: list[pathlib.Path] = []
    for pattern in REPORT_GLOBS:
        found.extend(sorted(ROOT.glob(pattern)))
    return [p for p in found if p.is_file()]


def pdf_targets() -> list[pathlib.Path]:
    """Collect the close-out reports that ship as PDF."""
    return sorted(
        ROOT / rel for rel in PDF_SOURCES
    )


PRINT_CSS = """@page { size: A4; margin: 16mm 14mm 18mm 14mm; }
body { font-family: "Noto Sans Thai", "Liberation Sans", sans-serif;
  font-size: 10.5pt; line-height: 1.65; color: #1a1a1a; }
h1 { font-size: 19pt; border-bottom: 3px solid #1a56db;
  padding-bottom: 7px; }
h2 { font-size: 13pt; color: #1a56db; margin-top: 1.5em;
  border-bottom: 1px solid #e5e7eb; padding-bottom: 3px; }
h3 { font-size: 11.5pt; margin-top: 1.1em; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0;
  font-size: 9pt; }
th, td { border: 1px solid #cbd5e1; padding: 5px 7px; text-align: left;
  vertical-align: top; }
th { background: #eef2ff; }
tr { page-break-inside: avoid; }
code { font-family: "Noto Sans Mono", monospace; font-size: 8.5pt;
  background: #f3f4f6; padding: 1px 4px; border-radius: 3px; }
pre { background: #f3f4f6; padding: 10px; border-radius: 5px;
  font-size: 8.5pt; page-break-inside: avoid; }
h1, h2 { page-break-after: avoid; }"""


def render_print(md_path: pathlib.Path) -> str:
    """Render a Markdown report as a standalone printable HTML page."""
    body = markdown.markdown(
        md_path.read_text(encoding="utf-8"),
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    folder = md_path.relative_to(ROOT).parts[0]
    title = md_path.stem.replace("-", " ")
    return (
        "<!DOCTYPE html>\n"
        '<html lang="th">\n<head>\n<meta charset="UTF-8">\n'
        "<title>" + title + " | SPM</title>\n"
        f"<style>{PRINT_CSS}</style>\n</head>\n<body>\n"
        f'<p style="color:#5b6472;font-size:9pt;margin:0 0 10px">'
        f"Software Project Management (SPM) &middot; {folder} "
        "&middot; ข้อมูลสมมติเพื่อการเรียน</p>\n"
        f"{body}\n</body>\n</html>\n"
    )


def find_chrome() -> str | None:
    """Locate a headless-capable Chrome/Chromium binary."""
    for name in ("google-chrome", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found
    return None


def build_pdfs() -> int:
    """Print every close-out report to PDF next to its Markdown."""
    chrome = find_chrome()
    if chrome is None:
        print("ไม่พบ Chrome/Chromium — สร้าง PDF ไม่ได้", file=sys.stderr)
        print("ติดตั้งอย่างใดอย่างหนึ่ง: "
              "google-chrome หรือ chromium", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = pathlib.Path(tmp)
        for md_path in pdf_targets():
            src = tmp_dir / (md_path.stem + ".html")
            src.write_text(render_print(md_path), encoding="utf-8")
            pdf_path = md_path.with_suffix(".pdf")
            subprocess.run(
                [
                    chrome, "--headless", "--disable-gpu", "--no-sandbox",
                    f"--print-to-pdf={pdf_path}",
                    "--no-pdf-header-footer",
                    src.as_uri(),
                ],
                check=True, capture_output=True, timeout=120,
            )
            size_kb = pdf_path.stat().st_size // 1024
            print(f"pdf   {pdf_path.relative_to(ROOT).as_posix()} "
                  f"({size_kb} KB)")

    print(f"เสร็จ: สร้าง PDF {len(pdf_targets())} ไฟล์")
    return 0


def main() -> int:
    """Build (or check) HTML for every report."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="รายงานไฟล์ที่ยังไม่ได้ build")
    parser.add_argument("--pdf", action="store_true",
                        help="สร้าง PDF ของรายงานปิด Sprint/Phase")
    args = parser.parse_args()

    if args.pdf:
        return build_pdfs()

    built, stale = 0, []
    for md_path in targets():
        html_path = md_path.with_suffix(".html")
        expected = render(md_path)
        if args.check:
            if not html_path.exists() or \
                    html_path.read_text(encoding="utf-8") != expected:
                stale.append(md_path.relative_to(ROOT).as_posix())
            continue
        if html_path.exists() and \
                html_path.read_text(encoding="utf-8") == expected:
            continue
        html_path.write_text(expected, encoding="utf-8")
        built += 1
        print(f"built {html_path.relative_to(ROOT).as_posix()}")

    if args.check:
        if stale:
            print("ต้อง build ใหม่:")
            for item in stale:
                print(f"  - {item}")
            return 1
        print(f"HTML ตรงกับ Markdown ทั้งหมด "
              f"({len(targets())} ไฟล์)")
        return 0

    print(f"เสร็จ: สร้าง {built} หน้า, รวม {len(targets())} รายงาน")
    return 0


if __name__ == "__main__":
    sys.exit(main())
