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
