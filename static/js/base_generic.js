window.addEventListener('scroll', function () {
    let header = document.querySelector('header');
    let windowlPosition = window.scrollY > 0;
    header.classList.toggle('scrolling-active', windowlPosition);
});