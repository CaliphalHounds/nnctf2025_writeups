(function () {
  const THEME_KEY = "navajacoin-theme";
  const root = document.documentElement;

  // Apply saved theme ASAP (prevents flash)
  try {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === "dark" || saved === "light") {
      root.setAttribute("data-theme", saved);
    }
  } catch (_) {}

  window.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("themeToggle");
    const current = root.getAttribute("data-theme") || "light";
    btn.setAttribute("aria-pressed", current === "dark");

    btn.addEventListener("click", () => {
      const now = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", now);
      btn.setAttribute("aria-pressed", now === "dark");
      try { localStorage.setItem(THEME_KEY, now); } catch (_) {}
    });
  });
})();
