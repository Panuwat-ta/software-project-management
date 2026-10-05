#!/usr/bin/env python3
"""Inventory Management Desktop Program (GTK4).

Run:
    python3 program.py

This desktop UI reuses the v3.0 domain layer from app.py:
SQLiteDatabaseContext, InventoryRepository, MemberManager,
CheckoutService, CSV export, migration and member-tier strategies.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

GTK_AVAILABLE = True
GTK_IMPORT_ERROR = None
try:
    import gi
    gi.require_version("Gtk", "4.0")
    from gi.repository import GLib, Gtk
except (ImportError, ValueError) as exc:
    GTK_AVAILABLE = False
    GTK_IMPORT_ERROR = exc

    class _MissingGtk:
        Application = object

    Gtk = _MissingGtk()

from app import (  # noqa: E402
    CheckoutService,
    CsvReportExporter,
    InventoryRepository,
    Member,
    MemberManager,
    Product,
    SQLiteDatabaseContext,
    TIER_CLASSES,
    migrate_json_to_sqlite,
    seed_default_products,
)

APP_ID = "th.ac.rmutl.spm.InventoryDesktop"
ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "inventory.db"
LEGACY_JSON = ROOT / "data.json"
REPORT_CSV = ROOT / "report.csv"

CSS = """
* {
  font-family: "Noto Sans", "Noto Sans Thai";
  font-size: 17px;
}
window {
  background: #f3f6f8;
  color: #182b36;
}
.header {
  background: #ffffff;
  border-bottom: 1px solid #dbe4e9;
  padding: 12px 20px;
}
.brand {
  font-size: 20px;
  font-weight: 800;
  color: #142b39;
}
.brand-subtitle {
  font-size: 12px;
  color: #6a7d87;
}
.header-status {
  background: #eef8f2;
  color: #1f7048;
  border: 1px solid #cfe7d8;
  border-radius: 999px;
  padding: 6px 11px;
  font-size: 12px;
  font-weight: 700;
}
.status-banner {
  background: #edf6fb;
  color: #155f88;
  border-bottom: 1px solid #cfe4ef;
  padding: 8px 20px;
}
.status-banner.success {
  background: #eef8f2;
  color: #1f7048;
  border-bottom-color: #cfe7d8;
}
.status-banner.error {
  background: #fff0f0;
  color: #a62f2f;
  border-bottom-color: #f0cece;
}
.sidebar {
  background: #102a3a;
  padding: 12px 6px;
}
.sidebar-title {
  color: #9fb4c0;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.06em;
}
.nav-button {
  min-height: 44px;
  border-radius: 10px;
  border: 0;
  background: transparent;
  color: #d9e5eb;
  padding: 0 12px;
}
.nav-button:hover {
  background: #19394b;
  color: #ffffff;
}
.nav-button.active {
  background: #e8f3f9;
  color: #0a5f8f;
  font-weight: 800;
}
.nav-icon {
  font-size: 15px;
  min-width: 22px;
}
.nav-label {
  font-size: 14px;
}
.sidebar-note {
  color: #9fb4c0;
  font-size: 11px;
}
.page {
  padding: 26px 28px 32px 28px;
}
.page-title {
  font-size: 27px;
  font-weight: 800;
  color: #142b39;
}
.page-lead {
  font-size: 14px;
  color: #667b86;
}
.section-title {
  font-size: 18px;
  font-weight: 800;
  color: #173746;
}
.section-caption {
  font-size: 12px;
  color: #768b95;
}
.card {
  background: #ffffff;
  border: 1px solid #dbe4e9;
  border-radius: 14px;
  padding: 16px;
}
.form-card {
  background: #ffffff;
  border: 1px solid #dbe4e9;
  border-radius: 14px;
  padding: 18px;
}
.table-card {
  background: #ffffff;
  border: 1px solid #dbe4e9;
  border-radius: 14px;
  padding: 0;
}
.metric-card {
  background: #ffffff;
  border: 1px solid #dbe4e9;
  border-radius: 14px;
  padding: 15px 16px;
}
.metric-title {
  font-size: 12px;
  color: #6f838d;
  font-weight: 700;
}
.metric {
  font-size: 29px;
  font-weight: 800;
  color: #0a6d9f;
}
.metric-hint {
  font-size: 11px;
  color: #8a9aa3;
}
.primary {
  background: #0a6d9f;
  color: #ffffff;
  font-weight: 800;
  border-radius: 9px;
  padding: 8px 14px;
}
.primary:hover {
  background: #085c87;
}
.secondary {
  background: #ffffff;
  color: #173746;
  border: 1px solid #cfdbe2;
  border-radius: 9px;
  padding: 8px 13px;
}
.secondary:hover {
  background: #f4f8fa;
}
.ghost {
  background: transparent;
  color: #315464;
  border: 0;
  border-radius: 8px;
  padding: 7px 10px;
}
.ghost:hover {
  background: #eef4f7;
}
.danger {
  background: #fff5f5;
  color: #a23333;
  border: 1px solid #efcece;
  border-radius: 8px;
}
.danger:hover {
  background: #ffeaea;
}
.compact-button {
  min-height: 32px;
  padding: 5px 9px;
}
.table-head {
  background: #eef3f6;
  border-bottom: 1px solid #dbe4e9;
  padding: 10px 12px;
  color: #516872;
  font-weight: 800;
}
.table-row {
  background: #ffffff;
  border-bottom: 1px solid #edf1f4;
  padding: 9px 12px;
}
.table-row:hover {
  background: #fafcfd;
}
.low {
  color: #b65319;
  font-weight: 800;
}
.ok {
  color: #237149;
  font-weight: 800;
}
.success {
  color: #237149;
  font-weight: 800;
}
.error {
  color: #b12f2f;
  font-weight: 800;
}
.badge-low {
  background: #fff3e8;
  color: #a74a12;
  border: 1px solid #f3d7c0;
  border-radius: 999px;
  padding: 3px 8px;
  font-weight: 800;
}
.badge-ok {
  background: #eef8f2;
  color: #217248;
  border: 1px solid #cfe7d8;
  border-radius: 999px;
  padding: 3px 8px;
  font-weight: 800;
}
.receipt {
  background: #ffffff;
  border: 1px solid #dbe4e9;
  border-radius: 14px;
  padding: 18px;
}
.receipt-total {
  font-size: 28px;
  font-weight: 800;
  color: #0a6d9f;
}
.receipt-body {
  font-family: "Noto Sans", "Noto Sans Thai";
  font-size: 19px;
  font-weight: 500;
}
.empty-state {
  background: #fafcfd;
  border: 1px dashed #cfdae0;
  border-radius: 12px;
  padding: 20px;
  color: #6f838d;
}
.empty-title {
  font-size: 15px;
  font-weight: 800;
  color: #435b67;
}
.field-label {
  font-size: 12px;
  color: #526a75;
  font-weight: 700;
}
.helper {
  font-size: 11px;
  color: #84969f;
}
.count-label {
  font-size: 12px;
  color: #607580;
  font-weight: 700;
}
.editing-pill {
  background: #fff5e8;
  color: #9a591b;
  border: 1px solid #f1dcc2;
  border-radius: 999px;
  padding: 4px 9px;
  font-size: 11px;
  font-weight: 800;
}
entry,
spinbutton,
dropdown {
  min-height: 40px;
  border-radius: 8px;
}
entry:focus,
spinbutton:focus,
dropdown:focus {
  border-color: #4b9cc4;
}
separator {
  background: #e3eaee;
}
"""


def build_backend(db_path: str | Path = DB_PATH,
                  legacy_json: str | Path | None = LEGACY_JSON,
                  seed: bool = True,
                  ) -> Tuple[SQLiteDatabaseContext,
                             InventoryRepository,
                             MemberManager,
                             CheckoutService]:
    """Create the shared domain services for the desktop program."""
    SQLiteDatabaseContext.reset()
    db = SQLiteDatabaseContext.getInstance(str(db_path))
    repo = InventoryRepository(db)
    members = MemberManager(db)
    checkout = CheckoutService(repo, members)
    if repo.count_products() == 0 and legacy_json:
        path = Path(legacy_json)
        if path.exists():
            migrate_json_to_sqlite(str(path), repo)
    if seed:
        seed_default_products(repo)
    return db, repo, members, checkout


def summary_metrics(repo: InventoryRepository) -> dict:
    """Return metrics shown on the dashboard."""
    data = repo.get_inventory_summary()
    return {
        "total_types": int(data["total_types"]),
        "total_value": float(data["total_value"]),
        "low_stock_count": len(repo.get_low_stock_alerts()),
    }


def format_receipt(receipt: dict) -> str:
    """Format a checkout receipt for the desktop UI."""
    return (
        f"สินค้า: {receipt['product_name']} ({receipt['product_id']})\n"
        f"จำนวน: {receipt['quantity']} × {receipt['unit_price']:,.2f} บาท\n"
        f"ยอดก่อนลด: {receipt['subtotal']:,.2f} บาท\n"
        f"สมาชิก: {receipt['tier']} ({receipt['discount_rate']:.0%})\n"
        f"ส่วนลด: -{receipt['discount_value']:,.2f} บาท\n"
        f"ยอดสุทธิ: {receipt['grand_total']:,.2f} บาท\n"
        f"คงเหลือ: {receipt['remaining']}"
    )


def product_status(product: Product) -> str:
    """Human-readable stock state used by the product table."""
    return "LOW" if product.is_low_stock else "OK"


def responsive_layout_mode(width: int) -> str:
    """Return the adaptive UI mode for the current window width."""
    if width < 760:
        return "narrow"
    if width < 980:
        return "compact"
    return "desktop"


def sidebar_width_for_window(width: int) -> int:
    """Keep the main menu close to one third of the window width."""
    return max(180, width // 3)


def _clear(container: Gtk.Widget) -> None:
    child = container.get_first_child()
    while child is not None:
        nxt = child.get_next_sibling()
        container.remove(child)
        child = nxt


def _label(
        text: str,
        css: Optional[str] = None,
        xalign: float = 0.0) -> Gtk.Label:
    label = Gtk.Label(label=text, xalign=xalign)
    label.set_wrap(True)
    if css:
        label.add_css_class(css)
    return label


def _field(
        title: str,
        widget: Gtk.Widget,
        helper: str | None = None) -> Gtk.Box:
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
    box.set_size_request(205, -1)
    box.set_hexpand(True)
    box.append(_label(title, "field-label"))
    box.append(widget)
    if helper:
        box.append(_label(helper, "helper"))
    return box


def _action_button(
        text: str,
        css: str = "secondary",
        tooltip: str | None = None) -> Gtk.Button:
    button = Gtk.Button(label=text)
    button.add_css_class(css)
    if tooltip:
        button.set_tooltip_text(tooltip)
    return button


def _empty_state(title: str, detail: str) -> Gtk.Box:
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
    box.add_css_class("empty-state")
    box.append(_label(title, "empty-title"))
    box.append(_label(detail, "helper"))
    return box


def _table_shell() -> Gtk.Box:
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    box.add_css_class("table-card")
    box.set_size_request(720, -1)
    return box


def _horizontal_scroll(child: Gtk.Widget) -> Gtk.ScrolledWindow:
    scroll = Gtk.ScrolledWindow()
    scroll.set_policy(
        Gtk.PolicyType.AUTOMATIC,
        Gtk.PolicyType.NEVER,
    )
    scroll.set_propagate_natural_height(True)
    scroll.set_child(child)
    return scroll


class InventoryDesktop(Gtk.Application):
    """GTK4 application shell."""

    def __init__(self) -> None:
        super().__init__(application_id=APP_ID)
        self.db = None
        self.repo = None
        self.members = None
        self.checkout = None
        self.window = None
        self.stack = None
        self.nav_buttons = {}
        self.nav_labels = {}
        self.sidebar = None
        self.sidebar_title = None
        self.sidebar_db_title = None
        self.sidebar_note = None
        self.header_subtitle = None
        self.header_db_status = None
        self.header_refresh = None
        self.current_layout_mode = None
        self.layout_watch_id = None
        self.metrics_box = None
        self.product_toolbar = None
        self.product_actions = None
        self.product_form_flow = None
        self.member_actions = None
        self.member_form_flow = None
        self.checkout_content = None

        self.status_revealer = None
        self.status_label = None
        self.status_timeout = None

        self.product_rows = None
        self.member_rows = None
        self.low_rows = None

        self.metric_types = None
        self.metric_value = None
        self.metric_low = None
        self.dashboard_updated = None

        self.product_search = None
        self.product_count_label = None
        self.product_form_title = None
        self.product_editing_pill = None
        self.p_id = self.p_name = None
        self.p_category = self.p_barcode = None
        self.p_qty = self.p_price = self.p_reorder = None

        self.member_count_label = None
        self.member_form_title = None
        self.member_editing_pill = None
        self.m_id = self.m_name = self.m_tier = None

        self.c_product = self.c_member = None
        self.c_qty = None
        self.receipt = None
        self.receipt_total = None
        self.checkout_msg = None

    def do_activate(self) -> None:
        if self.window is not None:
            self.window.present()
            return

        self.db, self.repo, self.members, self.checkout = build_backend()

        self.window = Gtk.ApplicationWindow(application=self)
        self.window.set_title("Inventory Management Program")
        self.window.set_default_size(1180, 760)
        self.window.set_size_request(640, 560)

        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode())
        Gtk.StyleContext.add_provider_for_display(
            self.window.get_display(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        outer.append(self._build_header())
        outer.append(self._build_status_banner())

        body = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        body.set_vexpand(True)
        body.append(self._build_sidebar())

        self.stack = Gtk.Stack()
        self.stack.set_hexpand(True)
        self.stack.set_vexpand(True)
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_transition_duration(160)
        self.stack.add_named(
            self._scroll(self._build_dashboard()),
            "dashboard",
        )
        self.stack.add_named(
            self._scroll(self._build_products()),
            "products",
        )
        self.stack.add_named(
            self._scroll(self._build_members()),
            "members",
        )
        self.stack.add_named(
            self._scroll(self._build_checkout()),
            "checkout",
        )

        body.append(self.stack)
        outer.append(body)
        self.window.set_child(outer)

        self.navigate("dashboard")
        self.refresh_all()
        self.window.present()
        GLib.idle_add(self._start_responsive_layout)

    def _build_header(self) -> Gtk.Widget:
        bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        bar.add_css_class("header")

        brand = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        brand.set_hexpand(True)
        brand.append(_label("Inventory Management Program", "brand"))
        self.header_subtitle = _label(
            "CLI → โปรแกรม Desktop · SQLite + Member + Checkout",
            "brand-subtitle",
        )
        brand.append(self.header_subtitle)
        bar.append(brand)

        self.header_db_status = _label(
            "● SQLite พร้อมใช้งาน",
            "header-status",
        )
        self.header_db_status.set_tooltip_text(
            "โปรแกรมใช้ฐานข้อมูล inventory.db บนเครื่องนี้"
        )
        bar.append(self.header_db_status)

        self.header_refresh = _action_button(
            "รีเฟรช",
            "secondary",
            "โหลดข้อมูลล่าสุดจากฐานข้อมูล",
        )
        self.header_refresh.connect(
            "clicked",
            lambda *_: self.refresh_with_feedback(),
        )
        bar.append(self.header_refresh)
        return bar

    def _build_status_banner(self) -> Gtk.Widget:
        self.status_revealer = Gtk.Revealer()
        self.status_revealer.set_transition_type(
            Gtk.RevealerTransitionType.SLIDE_DOWN
        )
        self.status_revealer.set_transition_duration(160)

        self.status_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
        )
        self.status_box.add_css_class("status-banner")
        self.status_label = _label("")
        self.status_label.set_hexpand(True)
        self.status_box.append(self.status_label)

        close = Gtk.Button(label="×")
        close.add_css_class("ghost")
        close.set_tooltip_text("ปิดข้อความแจ้งเตือน")
        close.connect(
            "clicked",
            lambda *_: self.status_revealer.set_reveal_child(False),
        )
        self.status_box.append(close)

        self.status_revealer.set_child(self.status_box)
        return self.status_revealer

    def _build_sidebar(self) -> Gtk.Widget:
        self.sidebar = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=5,
        )
        self.sidebar.add_css_class("sidebar")
        self.sidebar.set_hexpand(False)
        self.sidebar.set_halign(Gtk.Align.START)
        self.sidebar.set_size_request(220, -1)

        self.sidebar_title = _label(
            "เมนูหลัก",
            "sidebar-title",
        )
        self.sidebar_title.set_visible(True)
        self.sidebar.append(self.sidebar_title)

        items = [
            ("dashboard", "ภาพรวม", "view-grid-symbolic"),
            ("products", "สินค้า", "folder-symbolic"),
            ("members", "สมาชิก", "avatar-default-symbolic"),
            ("checkout", "Checkout", "emblem-ok-symbolic"),
        ]
        for key, text, icon_name in items:
            button = Gtk.Button()
            button.add_css_class("nav-button")
            button.set_hexpand(True)
            button.set_tooltip_text(text)

            row = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=0,
            )
            row.set_hexpand(True)
            row.set_halign(Gtk.Align.FILL)
            image = Gtk.Image.new_from_icon_name(icon_name)
            image.add_css_class("nav-icon")
            row.append(image)

            label = _label(text, "nav-label")
            label.set_hexpand(True)
            label.set_xalign(0.0)
            label.set_visible(True)
            row.append(label)
            button.set_child(row)

            button.connect(
                "clicked",
                lambda _b, name=key: self.navigate(name),
            )
            self.nav_buttons[key] = button
            self.nav_labels[key] = label
            self.sidebar.append(button)

        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        self.sidebar.append(spacer)

        self.sidebar_db_title = _label(
            "ฐานข้อมูล",
            "sidebar-title",
        )
        self.sidebar_db_title.set_visible(True)
        self.sidebar.append(self.sidebar_db_title)

        self.sidebar_note = _label(
            "SQLite local\ninventory.db",
            "sidebar-note",
        )
        self.sidebar_note.set_visible(True)
        self.sidebar.append(self.sidebar_note)
        return self.sidebar

    def _scroll(self, child: Gtk.Widget) -> Gtk.Widget:
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC,
        )
        scroll.set_child(child)
        return scroll

    def _page(self, title: str, lead: str) -> Gtk.Box:
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        page.add_css_class("page")
        page.set_size_request(520, -1)

        heading = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=3,
        )
        heading.append(_label(title, "page-title"))
        heading.append(_label(lead, "page-lead"))
        page.append(heading)
        return page

    def _metric_card(
            self,
            title: str,
            hint: str) -> tuple[Gtk.Widget, Gtk.Label]:
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        card.add_css_class("metric-card")
        card.set_hexpand(True)
        card.append(_label(title, "metric-title"))
        value = _label("0", "metric")
        card.append(value)
        card.append(_label(hint, "metric-hint"))
        return card, value

    def _section_header(
            self,
            title: str,
            caption: str | None = None) -> Gtk.Box:
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        text = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        text.set_hexpand(True)
        text.append(_label(title, "section-title"))
        if caption:
            text.append(_label(caption, "section-caption"))
        row.append(text)
        return row

    def _build_dashboard(self) -> Gtk.Widget:
        page = self._page(
            "ภาพรวมคลังสินค้า",
            "ดูสถานะคลังแบบรวดเร็วและเห็นรายการที่ต้องจัดการก่อน",
        )

        self.metrics_box = Gtk.FlowBox()
        self.metrics_box.set_selection_mode(
            Gtk.SelectionMode.NONE
        )
        self.metrics_box.set_homogeneous(True)
        self.metrics_box.set_column_spacing(12)
        self.metrics_box.set_row_spacing(12)
        self.metrics_box.set_min_children_per_line(1)
        self.metrics_box.set_max_children_per_line(3)

        c1, self.metric_types = self._metric_card(
            "ประเภทสินค้า",
            "จำนวนรายการสินค้าในระบบ",
        )
        c2, self.metric_value = self._metric_card(
            "มูลค่าคงคลัง",
            "มูลค่ารวมตามจำนวนคงเหลือ",
        )
        c3, self.metric_low = self._metric_card(
            "สินค้าใกล้หมด",
            "ถึงหรือต่ำกว่าจุดสั่งซื้อ",
        )
        for card in (c1, c2, c3):
            card.set_size_request(190, -1)
            self.metrics_box.append(card)
        page.append(self.metrics_box)

        title_row = self._section_header(
            "รายการที่ควรจัดการ",
            "สินค้าเหลือน้อยกว่าหรือเท่ากับ Reorder Point",
        )
        self.dashboard_updated = _label("", "section-caption")
        title_row.append(self.dashboard_updated)

        page.append(title_row)

        low_card = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0,
        )
        low_card.add_css_class("table-card")
        self.low_rows = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0,
        )
        low_card.append(self.low_rows)
        page.append(low_card)
        return page

    def _build_products(self) -> Gtk.Widget:
        page = self._page(
            "สินค้า",
            "เพิ่มและแก้ไขข้อมูลสินค้า พร้อมค้นหาและจัดการสต็อก",
        )

        form = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=14,
        )
        form.add_css_class("form-card")

        form_head = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
        )
        self.product_form_title = _label(
            "เพิ่มสินค้า",
            "section-title",
        )
        self.product_form_title.set_hexpand(True)
        form_head.append(self.product_form_title)

        self.product_editing_pill = _label(
            "กำลังแก้ไข",
            "editing-pill",
        )
        self.product_editing_pill.set_visible(False)
        form_head.append(self.product_editing_pill)
        form.append(form_head)

        self.product_form_flow = Gtk.FlowBox()
        self.product_form_flow.set_selection_mode(
            Gtk.SelectionMode.NONE
        )
        self.product_form_flow.set_homogeneous(True)
        self.product_form_flow.set_column_spacing(12)
        self.product_form_flow.set_row_spacing(12)
        self.product_form_flow.set_min_children_per_line(1)
        self.product_form_flow.set_max_children_per_line(3)

        self.p_id = Gtk.Entry(placeholder_text="เช่น P001")
        self.p_name = Gtk.Entry(placeholder_text="ชื่อสินค้า")
        self.p_qty = Gtk.SpinButton.new_with_range(
            0,
            1_000_000,
            1,
        )
        self.p_price = Gtk.SpinButton.new_with_range(
            0,
            10_000_000,
            1,
        )
        self.p_price.set_digits(2)
        self.p_category = Gtk.Entry(placeholder_text="General")
        self.p_barcode = Gtk.Entry(
            placeholder_text="Barcode (ถ้ามี)"
        )
        self.p_reorder = Gtk.SpinButton.new_with_range(
            0,
            1_000_000,
            1,
        )
        self.p_reorder.set_value(5)

        fields = [
            _field(
                "รหัสสินค้า *",
                self.p_id,
                "ใช้เป็นรหัสอ้างอิงหลัก",
            ),
            _field("ชื่อสินค้า *", self.p_name),
            _field("จำนวน", self.p_qty),
            _field("ราคา / หน่วย", self.p_price),
            _field("หมวดหมู่", self.p_category),
            _field("Barcode", self.p_barcode),
            _field(
                "Reorder Point",
                self.p_reorder,
                "ระบบจะแจ้งเตือนเมื่อสต็อกถึงค่านี้",
            ),
        ]
        for field in fields:
            self.product_form_flow.append(field)
        form.append(self.product_form_flow)

        self.product_actions = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
        )
        self.product_actions.set_halign(Gtk.Align.END)

        clear = _action_button(
            "ล้างฟอร์ม",
            "secondary",
            "ยกเลิกการแก้ไขและล้างข้อมูล",
        )
        clear.connect(
            "clicked",
            lambda *_: self.clear_product_form(),
        )
        save = _action_button(
            "บันทึกสินค้า",
            "primary",
            "บันทึกข้อมูลสินค้าลง SQLite",
        )
        save.connect("clicked", self.on_save_product)

        self.product_actions.append(clear)
        self.product_actions.append(save)
        form.append(self.product_actions)
        page.append(form)

        self.product_toolbar = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10,
        )
        self.product_search = Gtk.SearchEntry(
            placeholder_text="ค้นหารหัส ชื่อ หรือหมวดหมู่"
        )
        self.product_search.set_hexpand(True)
        self.product_search.connect(
            "search-changed",
            lambda *_: self.refresh_products(),
        )
        self.product_toolbar.append(self.product_search)

        self.product_count_label = _label(
            "0 รายการ",
            "count-label",
        )
        self.product_toolbar.append(self.product_count_label)

        export = _action_button(
            "Export CSV",
            "secondary",
            "ส่งออกรายการสินค้าเป็น report.csv",
        )
        export.connect("clicked", self.on_export_csv)
        self.product_toolbar.append(export)
        page.append(self.product_toolbar)

        table = _table_shell()
        header = Gtk.Grid(column_homogeneous=True)
        header.add_css_class("table-head")
        headers = [
            "รหัส",
            "สินค้า",
            "จำนวน",
            "ราคา",
            "สถานะ",
            "จัดการ",
        ]
        for i, text in enumerate(headers):
            header.attach(_label(text), i, 0, 1, 1)
        table.append(header)

        self.product_rows = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0,
        )
        table.append(self.product_rows)
        page.append(_horizontal_scroll(table))
        return page

    def _build_members(self) -> Gtk.Widget:
        page = self._page(
            "สมาชิก",
            "จัดการข้อมูลสมาชิกและระดับส่วนลดที่ใช้ใน Checkout",
        )

        form = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=14,
        )
        form.add_css_class("form-card")

        form_head = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
        )
        self.member_form_title = _label(
            "เพิ่มสมาชิก",
            "section-title",
        )
        self.member_form_title.set_hexpand(True)
        form_head.append(self.member_form_title)

        self.member_editing_pill = _label(
            "กำลังแก้ไข",
            "editing-pill",
        )
        self.member_editing_pill.set_visible(False)
        form_head.append(self.member_editing_pill)
        form.append(form_head)

        self.member_form_flow = Gtk.FlowBox()
        self.member_form_flow.set_selection_mode(
            Gtk.SelectionMode.NONE
        )
        self.member_form_flow.set_homogeneous(True)
        self.member_form_flow.set_column_spacing(12)
        self.member_form_flow.set_row_spacing(12)
        self.member_form_flow.set_min_children_per_line(1)
        self.member_form_flow.set_max_children_per_line(3)

        self.m_id = Gtk.Entry(placeholder_text="เช่น M001")
        self.m_name = Gtk.Entry(placeholder_text="ชื่อสมาชิก")
        self.m_tier = Gtk.DropDown.new_from_strings(
            list(TIER_CLASSES.keys())
        )

        fields = [
            _field(
                "รหัสสมาชิก *",
                self.m_id,
                "ใช้ค้นหาสมาชิกตอน Checkout",
            ),
            _field("ชื่อสมาชิก *", self.m_name),
            _field(
                "ระดับสมาชิก",
                self.m_tier,
                "Regular 0% · Silver 5% · Gold 10% · Platinum 15%",
            ),
        ]
        for field in fields:
            self.member_form_flow.append(field)
        form.append(self.member_form_flow)

        self.member_actions = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
        )
        self.member_actions.set_halign(Gtk.Align.END)

        clear = _action_button(
            "ล้างฟอร์ม",
            "secondary",
            "ยกเลิกการแก้ไขสมาชิก",
        )
        clear.connect(
            "clicked",
            lambda *_: self.clear_member_form(),
        )
        save = _action_button(
            "บันทึกสมาชิก",
            "primary",
            "บันทึกสมาชิกลง SQLite",
        )
        save.connect("clicked", self.on_save_member)

        self.member_actions.append(clear)
        self.member_actions.append(save)
        form.append(self.member_actions)
        page.append(form)

        list_head = self._section_header(
            "รายชื่อสมาชิก",
            "ส่วนลดจะถูกนำไปใช้โดย CheckoutService",
        )
        self.member_count_label = _label(
            "0 รายการ",
            "count-label",
        )
        list_head.append(self.member_count_label)
        page.append(list_head)

        table = _table_shell()
        header = Gtk.Grid(column_homogeneous=True)
        header.add_css_class("table-head")
        headers = ["รหัส", "ชื่อ", "Tier", "ส่วนลด", "จัดการ"]
        for i, text in enumerate(headers):
            header.attach(_label(text), i, 0, 1, 1)
        table.append(header)

        self.member_rows = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0,
        )
        table.append(self.member_rows)
        page.append(_horizontal_scroll(table))
        return page

    def _build_checkout(self) -> Gtk.Widget:
        page = self._page(
            "Checkout",
            "ตัดสต็อกและคิดส่วนลดสมาชิกด้วย CheckoutService เดิม",
        )

        self.checkout_content = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=16,
        )

        form = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
        )
        form.add_css_class("form-card")
        form.set_hexpand(True)
        form.append(_label("ข้อมูลการขาย", "section-title"))
        form.append(
            _label(
                "กรอกรหัสสินค้าและจำนวน "
                "รหัสสมาชิกเว้นว่างได้สำหรับ Guest",
                "section-caption",
            )
        )

        self.c_product = Gtk.Entry(
            placeholder_text="เช่น P001"
        )
        self.c_qty = Gtk.SpinButton.new_with_range(
            1,
            1_000_000,
            1,
        )
        self.c_member = Gtk.Entry(
            placeholder_text="เช่น M001 หรือเว้นว่าง"
        )

        form.append(
            _field(
                "รหัสสินค้า *",
                self.c_product,
                "ตรวจสอบจากหน้าสินค้าได้",
            )
        )
        form.append(_field("จำนวน *", self.c_qty))
        form.append(
            _field(
                "รหัสสมาชิก",
                self.c_member,
                "Guest จะคิดราคาเต็มโดยอัตโนมัติ",
            )
        )

        checkout_btn = _action_button(
            "ยืนยัน Checkout และตัดสต็อก",
            "primary",
            "คำนวณส่วนลดและบันทึกสต็อก",
        )
        checkout_btn.set_hexpand(True)
        checkout_btn.connect("clicked", self.on_checkout)
        form.append(checkout_btn)

        self.checkout_msg = _label("", "helper")
        form.append(self.checkout_msg)
        self.checkout_content.append(form)

        receipt_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
        )
        receipt_box.add_css_class("receipt")
        receipt_box.set_hexpand(True)

        receipt_box.append(_label("สรุปใบเสร็จ", "section-title"))
        receipt_box.append(
            _label(
                "ผลลัพธ์ล่าสุดจะค้างไว้เพื่อให้ตรวจสอบก่อนทำรายการถัดไป",
                "section-caption",
            )
        )

        self.receipt_total = _label("0.00 ฿", "receipt-total")
        receipt_box.append(self.receipt_total)

        receipt_box.append(Gtk.Separator())

        self.receipt = _label(
            "ยังไม่มีรายการ Checkout\n"
            "เมื่อชำระสำเร็จ รายละเอียดจะแสดงที่นี่",
            "receipt-body",
        )
        self.receipt.set_selectable(True)
        receipt_box.append(self.receipt)

        self.checkout_content.append(receipt_box)
        page.append(self.checkout_content)
        return page

    def show_status(
            self,
            text: str,
            error: bool = False) -> None:
        if not self.status_revealer or not self.status_label:
            return

        self.status_label.set_text(text)
        self.status_box.remove_css_class("success")
        self.status_box.remove_css_class("error")
        self.status_box.add_css_class(
            "error" if error else "success"
        )
        self.status_revealer.set_reveal_child(True)

        if self.status_timeout:
            GLib.source_remove(self.status_timeout)
        self.status_timeout = GLib.timeout_add_seconds(
            4,
            self._hide_status,
        )

    def _hide_status(self) -> bool:
        if self.status_revealer:
            self.status_revealer.set_reveal_child(False)
        self.status_timeout = None
        return False

    def _confirm(
            self,
            title: str,
            detail: str,
            on_confirm) -> None:
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            modal=True,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text=title,
        )
        dialog.set_secondary_text(detail)

        def handle_response(widget, response) -> None:
            if response == Gtk.ResponseType.YES:
                on_confirm()
            widget.destroy()

        dialog.connect("response", handle_response)
        dialog.present()

    def _start_responsive_layout(self) -> bool:
        self._apply_responsive_layout(
            self.window.get_width()
        )
        if self.layout_watch_id is None:
            self.layout_watch_id = GLib.timeout_add(
                250,
                self._watch_responsive_layout,
            )
        return False

    def _watch_responsive_layout(self) -> bool:
        if not self.window:
            self.layout_watch_id = None
            return False
        self._apply_responsive_layout(
            self.window.get_width()
        )
        return True

    def _apply_responsive_layout(
            self,
            width: int) -> None:
        if width <= 1:
            return

        mode = responsive_layout_mode(width)
        if mode == self.current_layout_mode:
            return
        self.current_layout_mode = mode

        narrow = mode == "narrow"

        if self.sidebar:
            self.sidebar.set_size_request(
                sidebar_width_for_window(width),
                -1,
            )
            self.sidebar.set_hexpand(False)
        if self.sidebar_title:
            self.sidebar_title.set_visible(True)
        if self.sidebar_db_title:
            self.sidebar_db_title.set_visible(True)
        if self.sidebar_note:
            self.sidebar_note.set_visible(True)
        for label in self.nav_labels.values():
            label.set_visible(True)

        if self.header_subtitle:
            self.header_subtitle.set_visible(
                mode == "desktop"
            )
        if self.header_db_status:
            self.header_db_status.set_visible(
                not narrow
            )
        if self.header_refresh:
            self.header_refresh.set_visible(
                not narrow
            )

        if self.metrics_box:
            self.metrics_box.set_max_children_per_line(
                3 if mode == "desktop"
                else 2 if mode == "compact"
                else 1
            )

        form_columns = (
            3 if mode == "desktop"
            else 2 if mode == "compact"
            else 1
        )
        if self.product_form_flow:
            self.product_form_flow.set_max_children_per_line(
                form_columns
            )
        if self.member_form_flow:
            self.member_form_flow.set_max_children_per_line(
                form_columns
            )

        if self.product_toolbar:
            self.product_toolbar.set_orientation(
                Gtk.Orientation.VERTICAL
                if narrow
                else Gtk.Orientation.HORIZONTAL
            )

        if self.checkout_content:
            self.checkout_content.set_orientation(
                Gtk.Orientation.HORIZONTAL
                if mode == "desktop"
                else Gtk.Orientation.VERTICAL
            )

    def navigate(self, page: str) -> None:
        self.stack.set_visible_child_name(page)
        for key, button in self.nav_buttons.items():
            if key == page:
                button.add_css_class("active")
            else:
                button.remove_css_class("active")

        if page == "dashboard":
            self.refresh_dashboard()
        elif page == "products":
            self.refresh_products()
        elif page == "members":
            self.refresh_members()

    def refresh_all(self) -> None:
        self.refresh_dashboard()
        self.refresh_products()
        self.refresh_members()

    def refresh_with_feedback(self) -> None:
        self.refresh_all()
        self.show_status("รีเฟรชข้อมูลล่าสุดแล้ว")

    def refresh_dashboard(self) -> None:
        if not self.repo or not self.metric_types:
            return

        metrics = summary_metrics(self.repo)
        self.metric_types.set_text(str(metrics["total_types"]))
        self.metric_value.set_text(
            f"{metrics['total_value']:,.2f} ฿"
        )
        self.metric_low.set_text(
            str(metrics["low_stock_count"])
        )

        if self.dashboard_updated:
            now = datetime.now().strftime("%H:%M:%S")
            self.dashboard_updated.set_text(
                f"อัปเดต {now}"
            )

        _clear(self.low_rows)
        low = self.repo.get_low_stock_alerts()

        if not low:
            self.low_rows.append(
                _empty_state(
                    "สต็อกอยู่ในระดับปกติ",
                    "ยังไม่มีสินค้าที่ถึงหรือต่ำกว่า "
                    "Reorder Point",
                )
            )
            return

        for product in low:
            row = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=12,
            )
            row.add_css_class("table-row")

            product_text = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                spacing=2,
            )
            product_text.set_hexpand(True)
            product_text.append(
                _label(
                    f"{product.product_id} · {product.name}"
                )
            )
            product_text.append(
                _label(
                    product.category,
                    "section-caption",
                )
            )
            row.append(product_text)

            stock_text = (
                f"คงเหลือ {product.quantity} · "
                f"ROP {product.reorder_point}"
            )
            badge = _label(stock_text, "badge-low")
            row.append(badge)
            self.low_rows.append(row)

    def refresh_products(self) -> None:
        if not self.repo or not self.product_rows:
            return

        query = (
            self.product_search.get_text().strip().lower()
            if self.product_search
            else ""
        )
        _clear(self.product_rows)

        matched = []
        for product in self.repo.find_all():
            haystack = (
                f"{product.product_id} "
                f"{product.name} "
                f"{product.category}"
            ).lower()
            if query and query not in haystack:
                continue
            matched.append(product)

        if self.product_count_label:
            self.product_count_label.set_text(
                f"{len(matched)} รายการ"
            )

        if not matched:
            detail = (
                "ลองเปลี่ยนคำค้นหา"
                if query
                else "เพิ่มสินค้าใหม่จากฟอร์มด้านบน"
            )
            self.product_rows.append(
                _empty_state(
                    "ไม่พบสินค้า",
                    detail,
                )
            )
            return

        for product in matched:
            grid = Gtk.Grid(column_homogeneous=True)
            grid.add_css_class("table-row")

            grid.attach(
                _label(product.product_id),
                0,
                0,
                1,
                1,
            )

            info = Gtk.Box(
                orientation=Gtk.Orientation.VERTICAL,
                spacing=1,
            )
            info.append(_label(product.name))
            info.append(
                _label(
                    product.category,
                    "section-caption",
                )
            )
            grid.attach(info, 1, 0, 1, 1)

            grid.attach(
                _label(str(product.quantity)),
                2,
                0,
                1,
                1,
            )
            grid.attach(
                _label(f"{product.price:,.2f} ฿"),
                3,
                0,
                1,
                1,
            )

            status = _label(
                product_status(product),
                "badge-low"
                if product.is_low_stock
                else "badge-ok",
            )
            grid.attach(status, 4, 0, 1, 1)

            actions = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=4,
            )

            edit = _action_button(
                "แก้ไข",
                "ghost",
                f"แก้ไข {product.product_id}",
            )
            edit.add_css_class("compact-button")
            edit.connect(
                "clicked",
                lambda _b, p=product:
                self.fill_product_form(p),
            )

            cut = _action_button(
                "ตัด 1",
                "secondary",
                f"ตัดสต็อก {product.product_id} 1 ชิ้น",
            )
            cut.add_css_class("compact-button")
            cut.connect(
                "clicked",
                lambda _b, p=product:
                self.quick_cut(p),
            )

            delete = _action_button(
                "ลบ",
                "danger",
                f"ลบ {product.product_id}",
            )
            delete.add_css_class("compact-button")
            delete.connect(
                "clicked",
                lambda _b, p=product:
                self.request_delete_product(p),
            )

            actions.append(edit)
            actions.append(cut)
            actions.append(delete)
            grid.attach(actions, 5, 0, 1, 1)
            self.product_rows.append(grid)

    def refresh_members(self) -> None:
        if not self.members or not self.member_rows:
            return

        _clear(self.member_rows)
        members = self.members.find_all()

        if self.member_count_label:
            self.member_count_label.set_text(
                f"{len(members)} รายการ"
            )

        if not members:
            self.member_rows.append(
                _empty_state(
                    "ยังไม่มีสมาชิก",
                    "เพิ่มสมาชิกจากฟอร์มด้านบน "
                    "หรือ Checkout แบบ Guest ได้ทันที",
                )
            )
            return

        for member in members:
            grid = Gtk.Grid(column_homogeneous=True)
            grid.add_css_class("table-row")

            grid.attach(
                _label(member.member_id),
                0,
                0,
                1,
                1,
            )
            grid.attach(
                _label(member.name),
                1,
                0,
                1,
                1,
            )
            grid.attach(
                _label(member.tier),
                2,
                0,
                1,
                1,
            )
            grid.attach(
                _label(
                    f"{member.discount_rate:.0%}",
                    "badge-ok",
                ),
                3,
                0,
                1,
                1,
            )

            actions = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=4,
            )

            edit = _action_button(
                "แก้ไข",
                "ghost",
                f"แก้ไข {member.member_id}",
            )
            edit.add_css_class("compact-button")
            edit.connect(
                "clicked",
                lambda _b, m=member:
                self.fill_member_form(m),
            )

            delete = _action_button(
                "ลบ",
                "danger",
                f"ลบ {member.member_id}",
            )
            delete.add_css_class("compact-button")
            delete.connect(
                "clicked",
                lambda _b, m=member:
                self.request_delete_member(m),
            )

            actions.append(edit)
            actions.append(delete)
            grid.attach(actions, 4, 0, 1, 1)
            self.member_rows.append(grid)

    def clear_product_form(self) -> None:
        self.p_id.set_text("")
        self.p_name.set_text("")
        self.p_qty.set_value(0)
        self.p_price.set_value(0)
        self.p_category.set_text("")
        self.p_barcode.set_text("")
        self.p_reorder.set_value(5)
        self.p_id.set_editable(True)

        if self.product_form_title:
            self.product_form_title.set_text(
                "เพิ่มสินค้า"
            )
        if self.product_editing_pill:
            self.product_editing_pill.set_visible(False)

    def fill_product_form(self, product: Product) -> None:
        self.p_id.set_text(product.product_id)
        self.p_id.set_editable(False)
        self.p_name.set_text(product.name)
        self.p_qty.set_value(product.quantity)
        self.p_price.set_value(product.price)
        self.p_category.set_text(product.category)
        self.p_barcode.set_text(product.barcode)
        self.p_reorder.set_value(
            product.reorder_point
        )

        if self.product_form_title:
            self.product_form_title.set_text(
                f"แก้ไขสินค้า {product.product_id}"
            )
        if self.product_editing_pill:
            self.product_editing_pill.set_visible(True)

        self.p_name.grab_focus()

    def on_save_product(self, *_args) -> None:
        pid = self.p_id.get_text().strip()
        name = self.p_name.get_text().strip()

        if not pid or not name:
            self.message(
                "ข้อมูลไม่ครบ",
                "กรุณากรอกรหัสสินค้าและชื่อสินค้า",
                error=True,
            )
            if not pid:
                self.p_id.grab_focus()
            else:
                self.p_name.grab_focus()
            return

        product = Product(
            pid,
            name,
            int(self.p_qty.get_value()),
            float(self.p_price.get_value()),
            self.p_category.get_text().strip()
            or "General",
            self.p_barcode.get_text().strip(),
            int(self.p_reorder.get_value()),
        )
        self.repo.save(product)
        self.clear_product_form()
        self.refresh_all()
        self.message(
            "บันทึกแล้ว",
            f"สินค้า {pid} ถูกบันทึกเรียบร้อย",
        )

    def quick_cut(self, product: Product) -> None:
        if product.quantity <= 0:
            self.message(
                "ตัดสต็อกไม่ได้",
                "สินค้าเหลือ 0 แล้ว",
                error=True,
            )
            return

        remaining = product.quantity - 1
        self.repo.update_stock(
            product.product_id,
            remaining,
        )
        self.refresh_all()
        self.message(
            "ตัดสต็อกแล้ว",
            f"{product.product_id} เหลือ {remaining} ชิ้น",
        )

    def request_delete_product(
            self,
            product: Product) -> None:
        self._confirm(
            "ลบสินค้านี้?",
            (
                f"{product.product_id} · {product.name}\n"
                "การลบไม่สามารถย้อนกลับได้"
            ),
            lambda: self.delete_product(product),
        )

    def delete_product(self, product: Product) -> None:
        self.repo.delete(product.product_id)
        self.clear_product_form()
        self.refresh_all()
        self.message(
            "ลบสินค้าแล้ว",
            f"{product.product_id} ถูกนำออกจากระบบ",
        )

    def on_export_csv(self, *_args) -> None:
        CsvReportExporter.export_repo(
            self.repo,
            str(REPORT_CSV),
        )
        self.message(
            "Export สำเร็จ",
            f"บันทึก report.csv ที่ {REPORT_CSV}",
        )

    def clear_member_form(self) -> None:
        self.m_id.set_text("")
        self.m_id.set_editable(True)
        self.m_name.set_text("")
        self.m_tier.set_selected(0)

        if self.member_form_title:
            self.member_form_title.set_text(
                "เพิ่มสมาชิก"
            )
        if self.member_editing_pill:
            self.member_editing_pill.set_visible(False)

    def fill_member_form(self, member: Member) -> None:
        self.m_id.set_text(member.member_id)
        self.m_id.set_editable(False)
        self.m_name.set_text(member.name)
        self.m_tier.set_selected(
            list(TIER_CLASSES.keys()).index(
                member.tier
            )
        )

        if self.member_form_title:
            self.member_form_title.set_text(
                f"แก้ไขสมาชิก {member.member_id}"
            )
        if self.member_editing_pill:
            self.member_editing_pill.set_visible(True)

        self.m_name.grab_focus()

    def on_save_member(self, *_args) -> None:
        mid = self.m_id.get_text().strip()
        name = self.m_name.get_text().strip()

        if not mid or not name:
            self.message(
                "ข้อมูลไม่ครบ",
                "กรุณากรอกรหัสและชื่อสมาชิก",
                error=True,
            )
            if not mid:
                self.m_id.grab_focus()
            else:
                self.m_name.grab_focus()
            return

        tier = list(TIER_CLASSES.keys())[
            self.m_tier.get_selected()
        ]
        self.members.save_member(
            Member(mid, name, tier)
        )
        self.clear_member_form()
        self.refresh_members()
        self.message(
            "บันทึกสมาชิกแล้ว",
            f"{mid} · {tier}",
        )

    def request_delete_member(
            self,
            member: Member) -> None:
        self._confirm(
            "ลบสมาชิกนี้?",
            (
                f"{member.member_id} · {member.name}\n"
                "ข้อมูลสมาชิกจะถูกลบออกจากระบบ"
            ),
            lambda: self.delete_member(member),
        )

    def delete_member(self, member: Member) -> None:
        self.members.delete_member(member.member_id)
        self.clear_member_form()
        self.refresh_members()
        self.message(
            "ลบสมาชิกแล้ว",
            f"{member.member_id} ถูกนำออกจากระบบ",
        )

    def on_checkout(self, *_args) -> None:
        pid = self.c_product.get_text().strip()
        qty = int(self.c_qty.get_value())
        member_id = (
            self.c_member.get_text().strip()
            or None
        )

        if not pid:
            self.checkout_msg.set_text(
                "กรุณากรอกรหัสสินค้า"
            )
            self.checkout_msg.remove_css_class(
                "success"
            )
            self.checkout_msg.add_css_class("error")
            self.show_status(
                "Checkout ไม่สำเร็จ: "
                "กรุณากรอกรหัสสินค้า",
                error=True,
            )
            self.c_product.grab_focus()
            return

        ok, payload, _remaining = (
            self.checkout.process_checkout(
                pid,
                member_id,
                qty,
            )
        )

        if not ok:
            self.checkout_msg.set_text(str(payload))
            self.checkout_msg.remove_css_class(
                "success"
            )
            self.checkout_msg.add_css_class("error")
            self.show_status(
                f"Checkout ไม่สำเร็จ: {payload}",
                error=True,
            )
            return

        self.checkout_msg.set_text(
            "Checkout สำเร็จ · "
            "สต็อกและยอดถูกอัปเดตแล้ว"
        )
        self.checkout_msg.remove_css_class("error")
        self.checkout_msg.add_css_class("success")

        self.receipt_total.set_text(
            f"{payload['grand_total']:,.2f} ฿"
        )
        self.receipt.set_text(
            format_receipt(payload)
        )

        self.c_product.set_text("")
        self.c_member.set_text("")
        self.c_qty.set_value(1)

        self.refresh_all()
        self.show_status(
            "Checkout สำเร็จ · "
            f"ยอดสุทธิ {payload['grand_total']:,.2f} บาท"
        )
        self.c_product.grab_focus()

    def message(
            self,
            title: str,
            text: str,
            error: bool = False) -> None:
        self.show_status(
            f"{title}: {text}",
            error=error,
        )


def main() -> int:
    if not GTK_AVAILABLE:
        raise SystemExit(
            "GTK4/PyGObject is required to open the UI. "
            "On Fedora: sudo dnf install python3-gobject gtk4"
        ) from GTK_IMPORT_ERROR
    app = InventoryDesktop()
    return app.run(sys.argv)


if __name__ == "__main__":
    raise SystemExit(main())
