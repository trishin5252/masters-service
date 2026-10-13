"use strict";

document.querySelectorAll("[data-nav-link]").forEach((link) => {
  const href = new URL(link.href).pathname;
  const current = window.location.pathname;
  if (current === href || (href !== "/" && current.startsWith(href))) {
    link.setAttribute("aria-current", "page");
  }
});

document.querySelectorAll("[data-copy-link]").forEach((button) => {
  button.addEventListener("click", async () => {
    const feedback = button.parentElement.querySelector("[data-copy-feedback]");
    try {
      await navigator.clipboard.writeText(window.location.href);
      feedback.textContent = "Ссылка скопирована";
    } catch {
      feedback.textContent = "Не удалось скопировать ссылку";
    }
  });
});
