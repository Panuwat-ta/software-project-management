/*
  js/script.js — Presentation engine
  ============================================================
  ขั้นตอนการทำงาน:
    1. fetch("./data/data.json")   ← โหลดข้อมูลทั้งหมด
    2. applyMeta(d)                ← ตั้งค่า <title>, <meta>, wordmark
    3. renderSlides(d)             ← สร้าง HTML ทุก slide แล้วแทรกใน #slidesTrack
    4. initPresentation()          ← เริ่มระบบ navigation (dots, arrows, keyboard, swipe)
  ============================================================
*/

/* ─────────────────────────────────────────
   Theme Toggle Setup
   ───────────────────────────────────────── */
(function initThemeToggle() {
  const savedTheme = localStorage.getItem('pp-theme');
  if (savedTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
  }

  window.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('themeToggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        if (isDark) {
          document.documentElement.removeAttribute('data-theme');
          localStorage.setItem('pp-theme', 'light');
        } else {
          document.documentElement.setAttribute('data-theme', 'dark');
          localStorage.setItem('pp-theme', 'dark');
        }
      });
    }
  });
})();

/* ─────────────────────────────────────────
   Utility: แปลง \n ใน JSON string → <br>
   ───────────────────────────────────────── */
const nl2br = (str) => str.replace(/\n/g, '<br>');

/* ─────────────────────────────────────────
   1. applyMeta — ตั้งค่า <title>, <meta description>, wordmark, lang
   ───────────────────────────────────────── */
function applyMeta(d) {
  const { meta } = d;
  document.documentElement.lang = meta.lang || 'th';
  document.title = meta.pageTitle;
  document.querySelector('meta[name="description"]').setAttribute('content', meta.pageDescription);
  document.getElementById('wordmarkLink').textContent = meta.wordmark;
}

/* ─────────────────────────────────────────
   2. renderSlides — สร้าง HTML ทุก slide
   ───────────────────────────────────────── */
function renderSlides(d) {
  const track = document.getElementById('slidesTrack');
  const slides = [];

  /* — Slide 1: Cover — */
  slides.push(renderCover(d.cover));

  /* — Slide 2: About — */
  slides.push(renderAbout(d.about));

  /* — Slide 3: Skills — */
  slides.push(renderSkills(d.skills));

  /* — Slide 4: Projects — */
  slides.push(renderProjects(d.projects));

  /* — Slide 5: Interests — */
  slides.push(renderInterests(d.interests));

  /* — Slide 6: Contact — */
  slides.push(renderContact(d.contact));

  track.innerHTML = slides.join('');
}

/* ─────────────────────────────────────────
   Slide templates
   ───────────────────────────────────────── */

function renderCover(c) {
  return `
  <section class="slide slide-cover" id="slide-1" aria-label="สไลด์ 1 หน้าปก">
    <div class="slide-inner cover-layout">
      <div class="cover-copy">
        <p class="eyebrow">${c.eyebrow}</p>
        <h1>${nl2br(c.name)}</h1>
        <p class="role">${c.role}</p>
        <p class="intro-copy">${c.introCopy}</p>
      </div>
      <div class="profile-panel" aria-label="ตำแหน่งสำหรับรูปโปรไฟล์">
        ${c.image
      ? `<img class="profile-image" src="${c.image}" alt="รูปโปรไฟล์">`
      : `<div class="profile-placeholder">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="12" cy="8" r="3.25"></circle>
                <path d="M5.5 20c.75-3.25 3.05-5 6.5-5s5.75 1.75 6.5 5"></path>
              </svg>
              <span>วางรูปโปรไฟล์ของคุณ</span>
            </div>`
    }
        <p class="profile-caption">${c.profileCaption}</p>
      </div>
    </div>
  </section>`;
}

function renderAbout(a) {
  const factsHTML = a.facts.map(f => {
    const valueHTML = f.isLink
      ? `<a href="${f.href}">${nl2br(f.value)}</a>`
      : nl2br(f.value);
    return `<div class="fact"><dt>${f.label}</dt><dd>${valueHTML}</dd></div>`;
  }).join('');

  return `
  <section class="slide" id="slide-2" aria-label="สไลด์ 2 ข้อมูลส่วนตัว">
    <div class="slide-inner detail-layout">
      <div class="slide-heading">
        <p class="eyebrow">${a.eyebrow}</p>
        <h2>${nl2br(a.heading)}</h2>
        <p>${a.note}</p>
      </div>
      <dl class="facts-grid">${factsHTML}</dl>
    </div>
  </section>`;
}

function renderSkills(s) {
  const barsHTML = s.items.map(sk => `
    <div class="skill-row">
      <div class="skill-meta">
        <span>${sk.name}</span>
        <span>${sk.label}</span>
      </div>
      <div class="skill-meter" role="progressbar"
           aria-label="${sk.name}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${sk.level}">
        <span style="--skill-level: ${sk.level}%"></span>
      </div>
    </div>`).join('');

  const tagsHTML = s.tools.map(t => `<span>${t}</span>`).join('');

  return `
  <section class="slide" id="slide-3" aria-label="สไลด์ 3 ทักษะความสามารถ">
    <div class="slide-inner skills-layout">
      <div class="slide-heading compact-heading">
        <p class="eyebrow">${s.eyebrow}</p>
        <h2>${nl2br(s.heading)}</h2>
        <p>${s.note}</p>
      </div>
      <div class="skill-list">
        ${barsHTML}
        <div class="skill-tags" aria-label="เครื่องมือที่ใช้">${tagsHTML}</div>
      </div>
    </div>
  </section>`;
}

function renderProjects(p) {
  const cardsHTML = p.items.map((item, i) => {
    const bgStyle = item.image
      ? `style="background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('${item.image}');"`
      : '';
    const extraClass = item.image ? ' has-bg' : '';
    const tag = item.link ? 'a' : 'article';
    const hrefAttr = item.link ? ` href="${item.link}" target="_blank" rel="noopener noreferrer"` : '';

    return `
    <${tag}${hrefAttr} class="project-card${extraClass}" ${bgStyle}>
      <p class="card-index">${String(i + 1).padStart(2, '0')}</p>
      <h3>${item.title}</h3>
      <p>${item.description}</p>
      <span class="card-meta">${item.meta}</span>
    </${tag}>`;
  }).join('');

  return `
  <section class="slide" id="slide-4" aria-label="สไลด์ 4 ผลงานและประสบการณ์">
    <div class="slide-inner project-layout">
      <div class="section-topline">
        <div class="slide-heading compact-heading">
          <p class="eyebrow">${p.eyebrow}</p>
          <h2>${nl2br(p.heading)}</h2>
        </div>
        <p class="section-note">${p.note}</p>
      </div>
      <div class="project-grid">${cardsHTML}</div>
    </div>
  </section>`;
}

function renderInterests(it) {
  const listHTML = it.items.map((item, i) => `
    <article class="interest-item">
      <span class="interest-num">${String(i + 1).padStart(2, '0')}</span>
      <div>
        <h3>${item.title}</h3>
        <p>${item.description}</p>
      </div>
    </article>`).join('');

  return `
  <section class="slide" id="slide-5" aria-label="สไลด์ 5 งานอดิเรกและความสนใจ">
    <div class="slide-inner interests-layout">
      <div class="slide-heading">
        <p class="eyebrow">${it.eyebrow}</p>
        <h2>${nl2br(it.heading)}</h2>
        <p>${it.note}</p>
      </div>
      <div class="interest-list">${listHTML}</div>
    </div>
  </section>`;
}

function renderContact(c) {
  const socialsHTML = c.socials.map(s => `
    <a href="${s.url}" aria-label="${s.label}">
      <span>${s.label}</span><span aria-hidden="true">↗</span>
    </a>`).join('');

  return `
  <section class="slide slide-contact" id="slide-6"
           aria-label="สไลด์ 6 ช่องทางติดต่อ">
    <div class="slide-inner contact-layout">
      <div>
        <p class="eyebrow">${c.eyebrow}</p>
        <h2>${nl2br(c.heading)}</h2>
        <p class="contact-copy">${c.copy}</p>
        <a class="contact-email" href="mailto:${c.email}">
          ${c.email} <span aria-hidden="true">↗</span>
        </a>
      </div>
      <nav class="social-list" aria-label="โซเชียลมีเดีย">
        ${socialsHTML}
      </nav>
    </div>
  </section>`;
}

/* ─────────────────────────────────────────
   3. initPresentation — ระบบ navigation
   ───────────────────────────────────────── */
function initPresentation() {
  const track = document.getElementById('slidesTrack');
  const viewport = document.querySelector('.slides-viewport');
  const slides = Array.from(track.querySelectorAll('.slide'));
  const dotsContainer = document.getElementById('progressDots');
  const prevButton = document.getElementById('prevButton');
  const nextButton = document.getElementById('nextButton');
  const currentLabel = document.getElementById('currentSlide');
  const totalLabel = document.getElementById('totalSlides');
  const presentation = document.querySelector('.presentation');
  const wordmarkLink = document.getElementById('wordmarkLink');
  const eyebrowEl = document.getElementById('slideEyebrow');

  /* เก็บ eyebrow text ของแต่ละสไลด์ไว้ใน array สำหรับอัปเดต header */
  const slideEyebrows = slides.map(sl => sl.querySelector('.eyebrow')?.textContent.trim() || '');

  let currentIndex = 0;
  let touchStartX = 0;
  let touchStartY = 0;

  /* อัปเดตจำนวนสไลด์ทั้งหมด */
  totalLabel.textContent = String(slides.length).padStart(2, '0');

  /* สร้าง progress dots */
  slides.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.type = 'button';
    dot.className = 'progress-dot';
    dot.dataset.goTo = String(i);
    dot.setAttribute('aria-label', `ไปสไลด์ ${i + 1}`);
    dotsContainer.appendChild(dot);
  });

  const dotButtons = Array.from(dotsContainer.querySelectorAll('.progress-dot'));

  /* showSlide — อัปเดต transform, counter, dots, header eyebrow, storage */
  const showSlide = (nextIndex) => {
    currentIndex = (nextIndex + slides.length) % slides.length;
    track.style.transform = `translateX(-${currentIndex * 100}%)`;
    currentLabel.textContent = String(currentIndex + 1).padStart(2, '0');
    slides.forEach((sl, i) => sl.setAttribute('aria-hidden', String(i !== currentIndex)));
    dotButtons.forEach((d, i) => d.setAttribute('aria-current', String(i === currentIndex)));

    /* อัปเดต eyebrow ใน header พร้อม fade เล็กน้อย */
    if (eyebrowEl) {
      eyebrowEl.style.opacity = '0';
      requestAnimationFrame(() => {
        eyebrowEl.textContent = slideEyebrows[currentIndex];
        eyebrowEl.style.opacity = '1';
      });
    }

    try { localStorage.setItem('pp-slide', String(currentIndex)); } catch (_) { }
    viewport.scrollTo({ top: 0, behavior: 'auto' });
  };

  const prevSlide = () => showSlide(currentIndex - 1);
  const nextSlide = () => showSlide(currentIndex + 1);

  /* Event listeners */
  prevButton.addEventListener('click', prevSlide);
  nextButton.addEventListener('click', nextSlide);

  dotsContainer.addEventListener('click', (e) => {
    const dot = e.target.closest('[data-go-to]');
    if (dot) showSlide(Number(dot.dataset.goTo));
  });

  wordmarkLink.addEventListener('click', (e) => { e.preventDefault(); showSlide(0); });

  window.addEventListener('keydown', (e) => {
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) return;
    if (e.key === 'ArrowLeft') prevSlide();
    if (e.key === 'ArrowRight') nextSlide();
  });

  presentation.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
    touchStartY = e.changedTouches[0].screenY;
  }, { passive: true });

  presentation.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].screenX - touchStartX;
    const dy = e.changedTouches[0].screenY - touchStartY;
    if (Math.abs(dx) < 45 || Math.abs(dx) < Math.abs(dy)) return;
    dx > 0 ? prevSlide() : nextSlide();
  }, { passive: true });

  /* Restore ตำแหน่งสไลด์หลัง refresh */
  let saved = 0;
  try { saved = Number(localStorage.getItem('pp-slide')); } catch (_) { }
  const ok = Number.isInteger(saved) && saved >= 0 && saved < slides.length;
  showSlide(ok ? saved : 0);
}

/* ─────────────────────────────────────────
   Entry point: fetch data.json → render → init
   ───────────────────────────────────────── */
fetch('./data/data.json')
  .then(res => {
    if (!res.ok) throw new Error(`ไม่พบไฟล์ data.json (${res.status})`);
    return res.json();
  })
  .then(data => {
    applyMeta(data);
    renderSlides(data);
    initPresentation();
  })
  .catch(err => {
    /* แสดง error ที่หน้าจอถ้าโหลด data ไม่ได้ */
    document.getElementById('slidesTrack').innerHTML = `
      <section class="slide" style="display:grid;place-items:center;">
        <div style="text-align:center;color:#dc2626;font-family:monospace;padding:2rem;">
          <p style="font-size:1.25rem;font-weight:600;margin-bottom:.5rem;">⚠ โหลด data.json ไม่ได้</p>
          <p style="color:#6b6b6b;font-size:.875rem;">${err.message}</p>
          <p style="color:#6b6b6b;font-size:.875rem;margin-top:.5rem;">
            ต้องเปิดผ่าน HTTP server (เช่น <code>python3 -m http.server</code>) ไม่ใช่ file://
          </p>
        </div>
      </section>`;
  });
