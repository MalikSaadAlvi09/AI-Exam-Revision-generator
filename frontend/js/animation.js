document.addEventListener('DOMContentLoaded', () => {
  if (window.gsap) {
    gsap.from('.animate-up', { y: 20, opacity: 0, duration: 0.7, stagger: 0.08, ease: 'power2.out' });
  }
  if (window.AOS) {
    AOS.init({ duration: 700, once: true });
  }
});
