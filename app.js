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
