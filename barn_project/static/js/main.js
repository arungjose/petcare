// BARN — Main JavaScript

document.addEventListener('DOMContentLoaded', function () {

  // ── Navbar scroll effect ──
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    navbar && navbar.classList.toggle('scrolled', window.scrollY > 20);
  });

  // ── Hamburger / Mobile menu ──
  const hamburger = document.getElementById('hamburger');
  let mobileMenu = document.getElementById('mobileMenu');

  if (hamburger) {
    hamburger.addEventListener('click', () => {
      if (!mobileMenu) {
        mobileMenu = buildMobileMenu();
        document.body.appendChild(mobileMenu);
      }
      mobileMenu.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  }

  function buildMobileMenu() {
    const menu = document.createElement('div');
    menu.className = 'mobile-menu';
    menu.id = 'mobileMenu';
    menu.innerHTML = `
      <button class="mobile-close" id="mobileClose">✕</button>
      <a href="/">Home</a>
      <a href="/pets/">Browse Pets</a>
      <a href="/pets/adopt/">❤️ Adopt</a>
      <a href="/services/">Services</a>
      <a href="/store/">Products</a>
      <a href="/store/accessories/">Accessories</a>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a href="/store/cart/">🛒 Cart</a>
      <hr style="border:none;border-top:1px solid var(--border);margin:12px 0">
      <a href="/accounts/login/">Login</a>
      <a href="/accounts/register/">Sign Up</a>
    `;
    menu.querySelector('#mobileClose').addEventListener('click', closeMobileMenu);
    menu.addEventListener('click', e => { if (e.target === menu) closeMobileMenu(); });
    return menu;
  }

  function closeMobileMenu() {
    if (mobileMenu) mobileMenu.classList.remove('open');
    document.body.style.overflow = '';
  }

  // ── Auto-dismiss alerts after 5s ──
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s, transform 0.5s';
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(20px)';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  // ── Pet image gallery ──
  const mainImg = document.getElementById('petMainImg');
  document.querySelectorAll('.pet-thumb').forEach(thumb => {
    thumb.addEventListener('click', () => {
      if (mainImg) mainImg.src = thumb.src;
      document.querySelectorAll('.pet-thumb').forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');
    });
  });

  // ── Quantity buttons in cart ──
  document.querySelectorAll('.qty-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const form = this.closest('form');
      const input = form ? form.querySelector('.qty-input') : null;
      if (!input) return;
      let val = parseInt(input.value) || 1;
      if (this.dataset.action === 'inc') val++;
      else if (this.dataset.action === 'dec') val = Math.max(1, val - 1);
      input.value = val;
      form.submit();
    });
  });

  // ── Smooth count-up for hero stats ──
  const stats = document.querySelectorAll('[data-countup]');
  if (stats.length) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.countup);
          let current = 0;
          const step = Math.ceil(target / 60);
          const timer = setInterval(() => {
            current = Math.min(current + step, target);
            el.textContent = current.toLocaleString() + (el.dataset.suffix || '');
            if (current >= target) clearInterval(timer);
          }, 20);
          observer.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    stats.forEach(el => observer.observe(el));
  }

  // ── Fade-in on scroll ──
  const fadeEls = document.querySelectorAll('.fade-in');
  if (fadeEls.length) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.1 });
    fadeEls.forEach(el => io.observe(el));
  }

  // ── Search form enhancement ──
  const searchInput = document.querySelector('.search-input');
  if (searchInput) {
    searchInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') e.target.closest('form').submit();
    });
  }

  // ── Sticky sidebar active link ──
  const dashLinks = document.querySelectorAll('.dash-nav a');
  dashLinks.forEach(link => {
    if (link.href === window.location.href) link.classList.add('active');
  });

  // ── Image preview for file inputs ──
  document.querySelectorAll('input[type="file"][data-preview]').forEach(input => {
    input.addEventListener('change', function () {
      const previewId = this.dataset.preview;
      const preview = document.getElementById(previewId);
      if (!preview) return;
      const files = Array.from(this.files).slice(0, 5);
      preview.innerHTML = '';
      files.forEach(file => {
        if (!file.type.startsWith('image/')) return;
        const reader = new FileReader();
        reader.onload = e => {
          const img = document.createElement('img');
          img.src = e.target.result;
          img.style.cssText = 'width:80px;height:60px;object-fit:cover;border-radius:8px;border:2px solid var(--teal)';
          preview.appendChild(img);
        };
        reader.readAsDataURL(file);
      });
    });
  });

});
