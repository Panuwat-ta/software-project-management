# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- Primary: the 3-person student team presenting the Software Project Management coursework in class (ENGSE202 / ENGSE225, RMUTL).
- Secondary: outside visitors browsing the project as a portfolio piece over time.
- Not the primary audience: graders doing rubric-only checks without the presentation.

## Product Purpose

A static documentation portal for the software-project-management coursework: project charter, 12 weeks of evidence, the Sprint 1 closure report, and per-week slide decks. It exists so the team can present from it in class and keep it as durable proof of work afterward. Success means a smooth in-room presentation and a site that still reads correctly months later.

## Positioning

The single source of browsable coursework evidence: every claim links back to a repository artifact (markdown docs, test suites, PDFs). A generic project template could not truthfully copy the evidence index.

## Operating Context

- Presented live in a classroom (projector, keyboard-navigated slide decks).
- Evaluated against ENGSE202 (project management: EVM, CCB, UAT, close-out) and ENGSE225 (evolution: refactoring, hardening, release) coursework.
- All figures are fictional coursework simulations; formal UAT sign-off, release tag, and some lint items are honestly recorded as pending.

## Capabilities and Constraints

- Static HTML + CSS only, no build step; slide decks are self-contained files that also open via file://.
- Thai language throughout; Noto Sans Thai with system fallbacks.
- Content moraine: no invented figures, dates, approvals, or signatures; missing evidence is labeled หลักฐานไม่พบ.
- No locked brand assets, colors, fonts, or deployed URLs to preserve (confirmed: none).
- Undecided: long-term hosting location for the portfolio use.

## Evidence on Hand

- Sprint1/sprint1.md (13-section closure report) and Sprint1/sprint1.pdf.
- Sprint1/week-1..12 markdown docs, test suites (root 5 passed, week-12 25 passed), Sprint1/img/test.png and test1.png screenshots.
- Absences future work must not fabricate: UAT signatures, v2.0.0-evolution git tag, Flake8 E501 clearance.

## Product Principles

1. Evidence over decoration: every page earns its place by pointing at a real artifact.
2. Honest gaps beat polished claims: pending items are stated, never implied done.
3. Presentable first: keyboard navigation, readable type at distance, no dependency on network at presentation time.
4. Stable over clever: plain static files the team can commit, move, and open anywhere.

## Accessibility & Inclusion

Classroom projection requires high-contrast body text (WCAG AA 4.5:1); current muted secondary text is a known gap to fix.
