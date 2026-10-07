/* Inventory Web frontend: hash router + fetch render. No dependencies. */
"use strict";

const $ = (sel) => document.querySelector(sel);

async function api(path, options) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...(options || {}),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error((data && data.detail) || `HTTP ${res.status}`);
  }
  return data;
}

function route() {
  const name = (location.hash || "#/dashboard").replace("#/", "");
  const valid = ["dashboard", "products", "members", "checkout"];
  const page = valid.includes(name) ? name : "dashboard";
  document.querySelectorAll(".page").forEach((el) => {
    el.hidden = el.id !== `page-${page}`;
  });
  document.querySelectorAll(".nav a").forEach((a) => {
    a.classList.toggle("active", a.dataset.route === page);
  });
  $("#mainNav").classList.remove("open");
  if (page === "dashboard") loadDashboard();
  if (page === "products") loadProducts();
  if (page === "members") loadMembers();
}

async function checkHealth() {
  const box = $("#apiStatus");
  try {
    const h = await api("/api/health");
    box.textContent = `API พร้อมใช้งาน (${h.version})`;
    box.classList.add("ok");
  } catch (err) {
    box.textContent = `เชื่อมต่อ API ไม่ได้: ${err.message}`;
    box.classList.add("bad");
  }
}

async function loadDashboard() {
  try {
    const s = await api("/api/summary");
    const cards = $("#summaryCards");
    cards.innerHTML = "";
    const items = [
      [s.total_types, "ประเภทสินค้า"],
      [Number(s.total_value).toLocaleString("th-TH"), "มูลค่ารวม (THB)"],
      [s.low_stock_list.length, "รายการใกล้หมด"],
    ];
    items.forEach(([num, lbl]) => {
      const div = document.createElement("div");
      div.className = "stat-card";
      div.innerHTML = `<div class="num"></div><div class="lbl"></div>`;
      div.querySelector(".num").textContent = num;
      div.querySelector(".lbl").textContent = lbl;
      cards.appendChild(div);
    });
    const rows = await api("/api/products");
    const low = rows.filter((p) => p.low_stock);
    const tb = $("#lowTable tbody");
    tb.innerHTML = low.length
      ? ""
      : `<tr><td colspan="4">ไม่มีสินค้าใกล้หมด</td></tr>`;
    low.forEach((p) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td></td><td></td><td></td><td></td>`;
      const cells = tr.querySelectorAll("td");
      cells[0].textContent = p.product_id;
      cells[1].textContent = p.name;
      cells[2].textContent = p.quantity;
      cells[3].textContent = p.reorder_point;
      tb.appendChild(tr);
    });
  } catch (err) {
    $("#summaryCards").innerHTML = `<div class="error">${err.message}</div>`;
  }
}

let productCache = [];

async function loadProducts() {
  const q = ($("#productSearch").value || "").toLowerCase();
  productCache = await api("/api/products");
  const tb = $("#productTable tbody");
  tb.innerHTML = "";
  productCache
    .filter(
      (p) =>
        !q ||
        p.name.toLowerCase().includes(q) ||
        p.product_id.toLowerCase().includes(q)
    )
    .forEach((p) => {
      const tr = document.createElement("tr");
      const badge = p.low_stock
        ? `<span class="badge low">LOW</span>`
        : `<span class="badge">OK</span>`;
      tr.innerHTML =
        `<td></td><td></td><td></td><td></td><td>${badge}</td><td></td>`;
      const cells = tr.querySelectorAll("td");
      cells[0].textContent = p.product_id;
      cells[1].textContent = p.name;
      cells[2].textContent = p.quantity;
      cells[3].textContent = Number(p.price).toFixed(2);
      const box = document.createElement("div");
      box.className = "actions";
      const edit = document.createElement("button");
      edit.className = "ghost";
      edit.textContent = "แก้ไข";
      edit.onclick = () => fillProductForm(p);
      const cut = document.createElement("button");
      cut.className = "ghost";
      cut.textContent = "-1";
      cut.onclick = () => cutStock(p.product_id, 1);
      const del = document.createElement("button");
      del.className = "danger";
      del.textContent = "ลบ";
      del.onclick = () => deleteProduct(p.product_id);
      box.append(edit, cut, del);
      cells[5].appendChild(box);
      tb.appendChild(tr);
    });
}

function fillProductForm(p) {
  const form = $("#productForm");
  form.product_id.value = p.product_id;
  form.name.value = p.name;
  form.quantity.value = p.quantity;
  form.price.value = p.price;
  form.category.value = p.category;
  form.barcode.value = p.barcode;
  form.reorder_point.value = p.reorder_point;
  form.scrollIntoView({ behavior: "smooth", block: "center" });
  form.name.focus();
}

async function cutStock(pid, qty) {
  try {
    await api(`/api/products/${encodeURIComponent(pid)}/cut`, {
      method: "POST",
      body: JSON.stringify({ qty }),
    });
    await loadProducts();
  } catch (err) {
    alert(err.message);
  }
}

async function deleteProduct(pid) {
  if (!confirm(`ลบสินค้า ${pid}?`)) return;
  try {
    await api(`/api/products/${encodeURIComponent(pid)}`, {
      method: "DELETE",
    });
    await loadProducts();
  } catch (err) {
    alert(err.message);
  }
}

async function loadMembers() {
  const rows = await api("/api/members");
  const tb = $("#memberTable tbody");
  tb.innerHTML = rows.length
    ? ""
    : `<tr><td colspan="5">ยังไม่มีสมาชิก</td></tr>`;
  rows.forEach((m) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td></td><td></td><td></td><td></td><td></td>`;
    const cells = tr.querySelectorAll("td");
    cells[0].textContent = m.member_id;
    cells[1].textContent = m.name;
    cells[2].textContent = m.tier;
    cells[3].textContent = `${Math.round(m.discount_rate * 100)}%`;
    const box = document.createElement("div");
    box.className = "actions";
    const edit = document.createElement("button");
    edit.className = "ghost";
    edit.textContent = "แก้ไข";
    edit.onclick = () => {
      const form = $("#memberForm");
      form.member_id.value = m.member_id;
      form.name.value = m.name;
      form.tier.value = m.tier;
      form.scrollIntoView({ behavior: "smooth", block: "center" });
    };
    const del = document.createElement("button");
    del.className = "danger";
    del.textContent = "ลบ";
    del.onclick = async () => {
      if (!confirm(`ลบสมาชิก ${m.member_id}?`)) return;
      try {
        await api(`/api/members/${encodeURIComponent(m.member_id)}`, {
          method: "DELETE",
        });
        await loadMembers();
      } catch (err) {
        alert(err.message);
      }
    };
    box.append(edit, del);
    cells[4].appendChild(box);
    tb.appendChild(tr);
  });
}

function formData(form) {
  const out = {};
  new FormData(form).forEach((v, k) => {
    out[k] = typeof v === "string" ? v.trim() : v;
  });
  return out;
}

document.addEventListener("DOMContentLoaded", () => {
  $("#navToggle").onclick = () => $("#mainNav").classList.toggle("open");
  window.addEventListener("hashchange", route);

  $("#productSearch").addEventListener("input", () => {
    loadProducts().catch(() => {});
  });
  $("#exportCsv").onclick = () => {
    window.location.href = "/api/export.csv";
  };

  $("#productForm").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const d = formData(ev.target);
    try {
      await api("/api/products", {
        method: "POST",
        body: JSON.stringify({
          product_id: d.product_id,
          name: d.name,
          quantity: Number(d.quantity),
          price: Number(d.price),
          category: d.category || "General",
          barcode: d.barcode || "",
          reorder_point: d.reorder_point === "" ? 5 : Number(d.reorder_point),
        }),
      });
      ev.target.reset();
      await loadProducts();
    } catch (err) {
      alert(err.message);
    }
  });

  $("#memberForm").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const d = formData(ev.target);
    try {
      await api("/api/members", {
        method: "POST",
        body: JSON.stringify({
          member_id: d.member_id,
          name: d.name,
          tier: d.tier,
        }),
      });
      ev.target.reset();
      await loadMembers();
    } catch (err) {
      alert(err.message);
    }
  });

  $("#checkoutForm").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const d = formData(ev.target);
    const box = $("#receipt");
    const errBox = $("#checkoutError");
    box.hidden = true;
    errBox.hidden = true;
    try {
      const r = await api("/api/checkout", {
        method: "POST",
        body: JSON.stringify({
          product_id: d.product_id,
          member_id: d.member_id || null,
          qty: Number(d.qty),
        }),
      });
      box.innerHTML =
        `<div><b>${r.product_name}</b> × ${r.quantity} @ ${r.unit_price}</div>` +
        `<div>Subtotal: ${r.subtotal.toFixed(2)} THB</div>` +
        `<div>Tier ${r.tier} (${Math.round(r.discount_rate * 100)}%): -${r.discount_value.toFixed(2)} THB</div>` +
        `<div class="total">TOTAL: ${r.grand_total.toFixed(2)} THB</div>` +
        `<div>คงเหลือ: ${r.remaining}` +
        (r.low_stock ? " — ใกล้หมดแล้ว!" : "") +
        `</div>`;
      box.hidden = false;
    } catch (err) {
      errBox.textContent = err.message;
      errBox.hidden = false;
    }
  });

  checkHealth().then(route);
});
