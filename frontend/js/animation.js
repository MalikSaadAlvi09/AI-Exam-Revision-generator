window.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".glass").forEach((el, index) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(12px)";
    setTimeout(() => {
      el.style.transition = "all 500ms ease";
      el.style.opacity = "1";
      el.style.transform = "translateY(0px)";
    }, 100 + index * 50);
  });
});
