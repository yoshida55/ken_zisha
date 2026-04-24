window.addEventListener('load', () => {
  document.body.classList.add('loaded');
});

// ヘッダー：スクロールでロゴ非表示＋背景つき小型に
(function () {
  const header = document.querySelector('.header');
  if (!header) return;
  window.addEventListener('scroll', () => {
    if (window.scrollY > 80) {
      header.classList.add('header--scrolled');
    } else {
      header.classList.remove('header--scrolled');
    }
  }, { passive: true });
})();

// FV背景スライドショー（クロスフェード）
const fvSlides = document.querySelectorAll('.fv-bg-slide');
if (fvSlides.length > 0) {
  let current = 0;
  setInterval(() => {
    fvSlides[current].classList.remove('is-active');
    current = (current + 1) % fvSlides.length;
    fvSlides[current].classList.add('is-active');
  }, 3000);
}

// スクロール出現アニメーション
const io = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      io.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.reveal').forEach(el => io.observe(el));

const softRevealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      softRevealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.18 });

document.querySelectorAll('.js-soft-reveal').forEach(el => softRevealObserver.observe(el));

// 自動無限スライダー
const track = document.getElementById('sliderTrack');

if (track) {
  const cards = Array.from(track.querySelectorAll('.slide-card'));
  cards.forEach(card => track.appendChild(card.cloneNode(true)));

  let pos = 0;
  let paused = false;
  const speed = 0.6;
  const totalWidth = cards.length * (420 + 4);

  function autoSlide() {
    if (!paused) {
      pos -= speed;
      if (Math.abs(pos) >= totalWidth) pos = 0;
      track.style.transform = `translateX(${pos}px)`;
    }
    requestAnimationFrame(autoSlide);
  }

  autoSlide();

  track.addEventListener('mouseenter', () => { paused = true; });
  track.addEventListener('mouseleave', () => { paused = false; });
}

function scrollToCard(id) {
  const card = document.getElementById(id);
  card.scrollIntoView({ behavior: 'smooth', block: 'center' });
  card.style.boxShadow = '0 0 0 3px #2563eb, 0 8px 32px rgba(37,99,235,0.2)';
  setTimeout(() => card.style.boxShadow = '', 1500);
}

function closeSection() {
  const section = document.querySelector('.section');
  section.style.opacity = '0';
  section.style.transform = 'translateY(-10px)';
  section.style.transition = 'opacity 0.3s, transform 0.3s';
  setTimeout(() => {
    section.style.opacity = '1';
    section.style.transform = '';
  }, 400);
}
