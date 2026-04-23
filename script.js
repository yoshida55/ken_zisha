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
