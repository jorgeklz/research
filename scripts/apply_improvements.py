import os
import glob

# Add fade-up CSS
css_path = 'assets/style.css'
with open(css_path, 'a') as f:
    f.write("\n.fade-up { opacity: 0; transform: translateY(20px); transition: opacity 0.6s var(--ease), transform 0.6s var(--ease); }\n")
    f.write(".fade-up.visible { opacity: 1; transform: translateY(0); }\n")
    f.write(".pub-search { padding: 0.4rem 0.8rem; border: 1px solid var(--line); border-radius: 8px; background: var(--bg); color: var(--ink); font-family: inherit; font-size: var(--fs-sm); width: 250px; }\n")
    f.write("@media (max-width: 640px) { .pub-search { width: 100%; margin-bottom: 1rem; } }\n")

# Modify app.js
app_path = 'assets/app.js'
with open(app_path, 'r') as f:
    app_code = f.read()

# 1. PWA & Language preference
pwa_lang_code = """
  const manifestLink = document.createElement("link");
  manifestLink.rel = "manifest";
  manifestLink.href = ROOT + "/manifest.json";
  document.head.appendChild(manifestLink);
  if ('serviceWorker' in navigator) navigator.serviceWorker.register(ROOT + '/sw.js').catch(()=>{});

  if (document.documentElement.lang === "es") localStorage.setItem("lang", "es");
  else if (document.documentElement.lang === "en") localStorage.setItem("lang", "en");
  
  // Very crude redirect to es/ if preference is es and we are on root
  if (localStorage.getItem("lang") === "es" && document.documentElement.lang === "en" && window.location.pathname === "/") {
    window.location.href = "es/index.html";
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); }
    });
  }, { threshold: 0.1 });
"""
app_code = app_code.replace('const ROOT = document.body.dataset.root || ".";', 'const ROOT = document.body.dataset.root || ".";\n' + pwa_lang_code)

# 2. Add observer to cards
app_code = app_code.replace('const el = pubEl(p, byId);', 'const el = pubEl(p, byId); el.classList.add("fade-up"); observer.observe(el);')
app_code = app_code.replace('wrap.appendChild(cardEl(p, pubs))', 'const c = cardEl(p, pubs); c.classList.add("fade-up"); wrap.appendChild(c); observer.observe(c);')

# 3. Search Bar Logic for Publications
search_logic = """
    const searchInput = document.getElementById("pub-search");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        const q = e.target.value.toLowerCase();
        filtered = s.filter(p => (p.title || "").toLowerCase().includes(q) || (p.authors || []).join(" ").toLowerCase().includes(q));
        page = 0; render();
      });
    }
"""
app_code = app_code.replace('if (prev) prev.addEventListener("click"', search_logic + '\n    if (prev) prev.addEventListener("click"')

# 4. Chart.js Injection
chart_old = 'function renderChart(pubs) {'
chart_new = """
  function renderChart(pubs) {
    const cb = $("#metrics-chart-body");
    if (!cb) return;
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/chart.js";
    script.onload = () => buildInteractiveChart(pubs);
    document.head.appendChild(script);
  }
  function buildInteractiveChart(pubs) {
    const cb = $("#metrics-chart-body"); cb.innerHTML = '<canvas id="myChart"></canvas>';
"""
app_code = app_code.replace(chart_old, chart_new)

# Cap the buildInteractiveChart logic roughly by replacing some old chart logic
# The old renderChart parses years. We can keep the parsing. Let's write a python script that does safer replacement.
with open(app_path, 'w') as f:
    f.write(app_code)

