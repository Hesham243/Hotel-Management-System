// Mobile navigation toggle
(function(){
  const toggle = document.querySelector('.nav-toggle');
  const menus = document.getElementById('primary-menu');
  if(!toggle || !menus) return;
  toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!expanded));
    menus.classList.toggle('open');
  });
  // Close menu on link click (mobile)
  menus.addEventListener('click', (e) => {
    if(e.target.tagName === 'A') {
      toggle.setAttribute('aria-expanded','false');
      menus.classList.remove('open');
    }
  });
})();
