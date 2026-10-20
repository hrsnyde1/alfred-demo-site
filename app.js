const themeKey = "harbor-pine-theme";
const darkPreference = window.matchMedia("(prefers-color-scheme: dark)");

try {
  const savedTheme = localStorage.getItem(themeKey);
  if (savedTheme === "light" || savedTheme === "dark") {
    document.documentElement.dataset.theme = savedTheme;
  }
} catch {
  // The OS preference still applies when storage is unavailable.
}

function isDarkTheme() {
  const selectedTheme = document.documentElement.dataset.theme;
  return selectedTheme ? selectedTheme === "dark" : darkPreference.matches;
}

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    const updateToggle = () => {
      toggle.setAttribute("aria-pressed", String(isDarkTheme()));
    };

    updateToggle();
    if (darkPreference.addEventListener) {
      darkPreference.addEventListener("change", updateToggle);
    } else {
      darkPreference.addListener(updateToggle);
    }

    toggle.addEventListener("click", () => {
      const theme = isDarkTheme() ? "light" : "dark";
      document.documentElement.dataset.theme = theme;
      try {
        localStorage.setItem(themeKey, theme);
      } catch {
        // Keep the selected theme for this page when storage is unavailable.
      }
      updateToggle();
    });
  }

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let anchorScrollTimeout;
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (event) => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || reducedMotion.matches) return;
      if (!link.hash || !document.getElementById(link.hash.slice(1))) return;

      // Let the browser perform the anchor navigation and manage its history.
      document.documentElement.classList.add("anchor-scroll");
      clearTimeout(anchorScrollTimeout);
      anchorScrollTimeout = setTimeout(() => {
        document.documentElement.classList.remove("anchor-scroll");
      }, 1200);
    });
  });

  if ("IntersectionObserver" in window && !reducedMotion.matches) {
    const sections = document.querySelectorAll("main > section:not(.hero)");
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });

    sections.forEach((section) => {
      section.classList.add("reveal");
      observer.observe(section);
    });

    const showAllForReducedMotion = () => {
      if (!reducedMotion.matches) return;
      document.documentElement.classList.remove("anchor-scroll");
      clearTimeout(anchorScrollTimeout);
      observer.disconnect();
      sections.forEach((section) => section.classList.remove("reveal"));
    };
    if (reducedMotion.addEventListener) {
      reducedMotion.addEventListener("change", showAllForReducedMotion);
    } else {
      reducedMotion.addListener(showAllForReducedMotion);
    }
  }

  // Loads the tip of the day from the site's own API (api/tip.py on Vercel).
  (async function showTip() {
    const target = document.getElementById("tip");
    if (!target) return;
    try {
      const response = await fetch("/api/tip");
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      target.textContent = data.tip;
    } catch {
      target.textContent = "Small, steady improvements beat big rewrites.";
    }
  })();
});
