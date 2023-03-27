  const menuBtn = document.querySelector('.mobile-menu-button');
  const menu = document.querySelector('.mobile-menu');

  menuBtn.addEventListener('click', () => {
    menu.classList.toggle('hidden');
  });
