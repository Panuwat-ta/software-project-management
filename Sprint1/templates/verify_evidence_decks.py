"""Verifier v2: template-1 visual contract + doc-grounded content coverage."""
import os, re, sys
from html.parser import HTMLParser

DECKS = ([f"Sprint1/week-{n}/slides.html" for n in range(1, 13)]
         + ["Sprint1/Phase1/slides.html", "Sprint1/sprint1-slides.html"])
FORBIDDEN = ["restart", "เริ่มใหม่", "?template=", "http://", "https://"]
MIN_SLIDES = 3
MAX_SLIDES = 12

KEYWORDS = {
  "Sprint1/week-1/slides.html": ["Project Charter", "ขอบเขต", "เมนู", "trello", "global"],
  "Sprint1/week-2/slides.html": ["DFD", "P1", "hotspot", "7.10", "SQLite", "Platinum"],
  "Sprint1/week-3/slides.html": ["DoD", "RACI", "atomic", "Product", "pytest"],
  "Sprint1/week-4/slides.html": ["v2.0", "5 passed", "test.json", "CI", "pytest.yml"],
  "Sprint1/week-5/slides.html": ["As-Is", "To-Be", "18,823", "25010", "31,000"],
  "Sprint1/week-6/slides.html": ["Singleton", "Repository", "Strategy", "DoR", "1,600"],
  "Sprint1/week-7/slides.html": ["18,823", "2,823", "14598", "36", "15%"],
  "Sprint1/week-8/slides.html": ["CR-01", "barcode", "burndown", "stakeholder", "8 man-hours"],
  "Sprint1/week-9/slides.html": ["4,000", "3,000", "4,200", "1,000", "1,200", "Retro", "15"],
  "Sprint1/week-10/slides.html": ["BUG-101", "KeyError", ".get(", "CCB", "CR-02", "1,473"],
  "Sprint1/week-11/slides.html": ["hardening", "27/29", "93", "0.96", "0.97", "E501", "freeze"],
  "Sprint1/week-12/slides.html": ["SC01", "SC02", "SC03", "25", "898", "1.00", "CHANGELOG"],
  "Sprint1/Phase1/slides.html": ["WBS", "risk", "Trello", "proposal"],
  "Sprint1/sprint1-slides.html": ["UAT", "E501", "Sprint 2", "25"],
}

DOC_COVERAGE = {
  "Sprint1/week-1/slides.html": ["doc.md", "project-charter.md", "scope.md", "trello.md"],
  "Sprint1/week-2/slides.html": ["blueprint.md", "dfd.md", "hotspot.md", "member-discount.md", "static-analysis.md", "trello.md"],
  "Sprint1/week-3/slides.html": ["dod.md", "raci.md"],
  "Sprint1/week-4/slides.html": ["app.md", "test.md"],
  "Sprint1/week-5/slides.html": ["architecture.md", "budget_worksheet.md", "iso25010_evaluation.md", "work.md"],
  "Sprint1/week-6/slides.html": ["communication_matrix_and_dod.md", "cost_variance_analysis.md", "to_be_architecture.md"],
  "Sprint1/week-7/slides.html": ["cost_baseline_and_sprint_plan.md", "iso_14598_quality_report.md"],
  "Sprint1/week-8/slides.html": ["cr-01_impact_analysis.md", "procurement_log.md", "sprint1_tracking.md", "stakeholder_matrix.md"],
  "Sprint1/week-9/slides.html": ["evm_sprint1.md", "retrospective_sprint1.md", "sprint_transition.md"],
  "Sprint1/week-10/slides.html": ["ccb_meeting_minutes.md", "contingency_reserve_log.md", "cr-02_impact_decision_form.md", "defect_log_bug-101.md"],
  "Sprint1/week-11/slides.html": ["flow_metrics.md", "hardening_report.md", "scope_freeze_agreement.md"],
  "Sprint1/week-12/slides.html": ["changelog.md", "final_evm.md", "release_checklist.md", "uat_sign_off_sheet.md"],
  "Sprint1/Phase1/slides.html": ["integrated_planning_proposal.md"],
  "Sprint1/sprint1-slides.html": ["sprint1.md", "readme.md"],
}

class V(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.slides, self.has_counter = [], 0, False
        self.has_prev, self.has_next, self.externals = False, False, []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id", "").startswith("slide-") and a.get("id", "")[6:].isdigit():
            self.slides += 1
        if a.get("id"):
            self.ids.append(a["id"])
        if a.get("id") == "slide-counter":
            self.has_counter = True
        if a.get("id") == "previous":
            self.has_prev = True
        if a.get("id") == "next":
            self.has_next = True
        for k in ("href", "src"):
            v = a.get(k, "") or ""
            if v.startswith(("http://", "https://")):
                self.externals.append(v)

def visible_text(raw):
    body = re.sub(r"<style>.*?</style>", "", raw, flags=re.S)
    body = re.sub(r"<script>.*?</script>", "", body, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", body)
    return text.replace("\u2212", "-").casefold()

failures = []
for deck in DECKS:
    errs = []
    if not os.path.exists(deck):
        failures.append(f"{deck}: MISSING FILE"); continue
    raw = open(deck, encoding="utf-8").read()
    p = V(); p.feed(raw)
    num_ids = sorted((i for i in p.ids if i.startswith("slide-") and i[6:].isdigit()), key=lambda x: int(x[6:]))
    want = [f"slide-{i}" for i in range(1, len(num_ids) + 1)]
    if not (MIN_SLIDES <= p.slides <= MAX_SLIDES) or num_ids != want:
        errs.append(f"need consecutive ids slide-1..N ({MIN_SLIDES}-{MAX_SLIDES} slides), got slides={p.slides}")
    if len(p.ids) != len(set(p.ids)):
        errs.append("duplicate ids")
    if not (p.has_counter and p.has_prev and p.has_next):
        errs.append("missing counter/previous/next")
    if p.externals:
        errs.append(f"external refs: {p.externals[:3]}")
    low = raw.lower()
    hit = [w for w in FORBIDDEN if w.lower() in low]
    if hit:
        errs.append(f"forbidden strings: {hit}")
    if "data-template" in raw and 'data-template="evidence"' not in raw:
        errs.append("data-template must be evidence or absent")
    if deck in KEYWORDS:
        text = visible_text(raw)
        missing = [k for k in KEYWORDS[deck] if k.replace("\u2212", "-").casefold() not in text]
        if missing:
            errs.append(f"missing keywords: {missing}")
    if deck in DOC_COVERAGE:
        vtext = visible_text(raw)
        missing_docs = [d for d in DOC_COVERAGE[deck] if d.casefold() not in vtext]
        if missing_docs:
            errs.append(f"missing docs: {missing_docs}")
    if errs:
        failures.append(f"{deck}: " + "; ".join(errs))
    else:
        print(f"PASS {deck}")
if failures:
    print(f"\nFAIL {len(failures)}/{len(DECKS)}")
    print("\n".join(failures)); sys.exit(1)
print(f"\nALL {len(DECKS)} DECKS PASS")
