// network.js
// D3.js co-author network: centred layout, bilingual labels and a list of the most frequent co-authors.

function initNetworkGraph(pubs, ROOT) {
  const container = document.getElementById("network-chart-body");
  if (!container) return;

  const ES = document.documentElement.lang === "es";
  const TX = ES ? {
    title: "Red de coautores", top: "Coautores más frecuentes", joint: "Publicaciones conjuntas", topCo: "Principales coautores",
    main: "Autor principal", very: "Muy frecuente", freq: "Frecuente", med: "Medio", occ: "Ocasional", reset: "Restablecer vista"
  } : {
    title: "Co-author network", top: "Most frequent co-authors", joint: "Joint publications", topCo: "Top co-authors",
    main: "Main author", very: "Very frequent", freq: "Frequent", med: "Medium", occ: "Occasional", reset: "Reset view"
  };
  const titleEl = document.querySelector("#network-chart-card .chart-t");
  if (titleEl) titleEl.textContent = TX.title;

  // Same person, different spelling ("Parraga-Alava" / "Párraga-Álava" / "J. Parraga-Alava"):
  // merge by accent-free key, keep the spelling that carries accents, and fold every variant of
  // the site owner into a single node.
  const norm = (s) => String(s).normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\s+/g, " ").trim().toLowerCase();
  const isMain = (id) => norm(id).includes("parraga");
  const MAIN_NAME = "Jorge Párraga-Álava";
  const keyOf = (a) => (isMain(a) ? "__main__" : norm(a));
  const display = {};
  const prefer = (a, b) => {
    const accents = (s) => (s.normalize("NFD").match(/[\u0300-\u036f]/g) || []).length;
    return accents(b) > accents(a) ? b : a;
  };
  pubs.forEach((p) => (p.authors || []).forEach((a) => {
    const k = keyOf(a);
    display[k] = k === "__main__" ? MAIN_NAME : (display[k] ? prefer(display[k], a) : a);
  }));

  const authorCounts = {};
  const linksMap = {};
  pubs.forEach((p) => {
    if (!p.authors) return;
    const authors = [...new Set(p.authors.map((a) => display[keyOf(a)]))];
    authors.forEach((a) => { authorCounts[a] = (authorCounts[a] || 0) + 1; });
    for (let i = 0; i < authors.length; i++) {
      for (let j = i + 1; j < authors.length; j++) {
        const a1 = authors[i] < authors[j] ? authors[i] : authors[j];
        const a2 = authors[i] < authors[j] ? authors[j] : authors[i];
        const key = a1 + "|||" + a2;
        if (!linksMap[key]) linksMap[key] = { source: a1, target: a2, value: 0 };
        linksMap[key].value++;
      }
    }
  });

  const maxCount = Math.max(1, ...Object.entries(authorCounts).filter(([id]) => !isMain(id)).map(([, c]) => c));
  const freqThresh = Math.max(3, Math.floor(maxCount * 0.6));
  const medThresh = Math.max(2, Math.floor(maxCount * 0.3));

  const nodes = Object.keys(authorCounts).map((id) => {
    let group = 1;
    if (authorCounts[id] >= medThresh) group = 2;
    if (authorCounts[id] >= freqThresh) group = 3;
    if (authorCounts[id] > 10) group = 4;
    if (isMain(id)) group = 0;
    return { id, group, radius: Math.min(35, 8 + authorCounts[id] * 2.5), count: authorCounts[id] };
  });
  const links = Object.values(linksMap);

  const adj = {};
  nodes.forEach((n) => { adj[n.id] = new Set([n.id]); });
  links.forEach((l) => { adj[l.source].add(l.target); adj[l.target].add(l.source); });

  const color = d3.scaleOrdinal()
    .domain([0, 1, 2, 3, 4])
    .range(["var(--navy)", "var(--mint)", "#4bc0c0", "#36a2eb", "var(--blue-600)"]);

  // layout: graph on the left, list of top co-authors on the right (stacked on small screens)
  container.innerHTML = "";
  container.style.height = "auto";
  container.style.padding = "0";
  container.style.overflow = "hidden";
  if (container.parentElement && container.parentElement.classList.contains("metrics-chart-card")) {
    container.parentElement.style.padding = "0";
    container.parentElement.style.overflow = "hidden";
    const header = container.parentElement.querySelector(".chart-header");
    if (header) { header.style.padding = "1.35rem 1.6rem 0.7rem 1.6rem"; header.style.margin = "0"; }
  }
  const layout = d3.select(container).append("div").attr("class", "net-layout");
  const host = layout.append("div").attr("class", "net-host").node();
  const aside = layout.append("aside").attr("class", "net-list");

  const width = host.clientWidth || 600;
  const height = host.clientHeight || 380;

  const svg = d3.select(host).append("svg")
    .attr("width", "100%").attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .style("display", "block");
  const g = svg.append("g");
  const zoom = d3.zoom().scaleExtent([0.3, 4]).on("zoom", (event) => g.attr("transform", event.transform));
  svg.call(zoom);

  const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id((d) => d.id).distance((d) => 50 - Math.min(30, d.value * 5)))
    .force("charge", d3.forceManyBody().strength(-80))
    .force("center", d3.forceCenter(width / 2, height / 2))
    // gentle pull to the middle keeps loosely-connected groups inside the view
    .force("x", d3.forceX(width / 2).strength(0.07))
    .force("y", d3.forceY(height / 2).strength(0.07))
    .force("collide", d3.forceCollide().radius((d) => d.radius + 8).iterations(2));
  simulation.stop();
  simulation.tick(300);

  const link = g.append("g").attr("stroke", "var(--line-2)").attr("stroke-opacity", 0.4)
    .selectAll("line").data(links).join("line")
    .attr("stroke-width", (d) => Math.sqrt(d.value) * 1.5);

  const nodeGroup = g.append("g").selectAll("g").data(nodes).join("g").call(drag(simulation));
  const circle = nodeGroup.append("circle")
    .attr("stroke", "#fff").attr("stroke-width", 2)
    .attr("r", (d) => d.radius).attr("fill", (d) => color(d.group))
    .style("cursor", "pointer").style("transition", "fill 0.2s, stroke 0.2s");
  nodeGroup.append("title").text((d) => `${d.id} (${d.count})`);

  const shortName = (id) => id.split(" ")[0] + (id.split(" ")[1] ? " " + id.split(" ")[1][0] + "." : "");
  const label = nodeGroup.append("text")
    .text((d) => shortName(d.id))
    .attr("x", 0).attr("y", (d) => d.radius + 12).attr("text-anchor", "middle")
    .style("font-size", (d) => (d.count > 5 ? "11px" : "10px"))
    .style("font-family", "inherit")
    .style("font-weight", (d) => (d.count > 10 ? "bold" : "normal"))
    .style("fill", "var(--ink)")
    .style("opacity", (d) => (d.count > 2 ? 1 : 0))
    .style("pointer-events", "none");

  function place() {
    link.attr("x1", (d) => d.source.x).attr("y1", (d) => d.source.y).attr("x2", (d) => d.target.x).attr("y2", (d) => d.target.y);
    nodeGroup.attr("transform", (d) => `translate(${d.x},${d.y})`);
  }
  place();
  simulation.on("tick", place);

  // initial view: fit every node inside the frame
  function fitTransform() {
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    nodes.forEach((n) => {
      x0 = Math.min(x0, n.x - n.radius); x1 = Math.max(x1, n.x + n.radius);
      y0 = Math.min(y0, n.y - n.radius); y1 = Math.max(y1, n.y + n.radius + 14);
    });
    const bw = Math.max(1, x1 - x0), bh = Math.max(1, y1 - y0);
    const k = Math.max(0.3, Math.min(1.5, 0.92 * Math.min(width / bw, height / bh)));
    return d3.zoomIdentity.translate(width / 2 - k * (x0 + x1) / 2, height / 2 - k * (y0 + y1) / 2).scale(k);
  }
  const home = fitTransform();
  svg.call(zoom.transform, home);

  // hover: fade unrelated nodes
  nodeGroup.on("mouseover", (event, d) => {
    circle.style("opacity", (o) => (adj[d.id].has(o.id) ? 1 : 0.1));
    link.style("opacity", (o) => (o.source.id === d.id || o.target.id === d.id ? 1 : 0.05));
    label.style("opacity", (o) => (adj[d.id].has(o.id) ? 1 : 0));
  }).on("mouseout", () => {
    circle.style("opacity", 1);
    link.style("opacity", 0.4);
    label.style("opacity", (d) => (d.count > 2 ? 1 : 0));
  });

  // info box
  const infoBox = d3.select(host).append("div")
    .style("position", "absolute").style("top", "10px").style("right", "10px")
    .style("background", "var(--bg)").style("padding", "1rem")
    .style("border", "1px solid var(--line)").style("border-radius", "8px")
    .style("font-size", "0.9rem").style("color", "var(--ink)").style("box-shadow", "var(--shadow)")
    .style("opacity", "0").style("pointer-events", "none").style("max-width", "250px")
    .style("transition", "opacity 0.2s ease");

  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function showInfo(d) {
    const connections = links
      .filter((l) => l.source.id === d.id || l.target.id === d.id)
      .map((l) => ({ target: l.source.id === d.id ? l.target.id : l.source.id, value: l.value }))
      .sort((a, b) => b.value - a.value).slice(0, 3);
    let html = `<strong style="font-size:1.1em;color:var(--navy)">${esc(d.id)}</strong><br/>`;
    html += `<span style="color:var(--ink-2); display:block; margin: 0.5rem 0;">${TX.joint}: <b>${d.count}</b></span>`;
    if (connections.length > 0) {
      html += `<div style="font-size:0.8em; margin-top:0.5rem; border-top:1px solid var(--line); padding-top:0.5rem;">`;
      html += `<b>${TX.topCo}:</b><ul style="margin: 0.2rem 0; padding-left: 1rem;">`;
      connections.forEach((c) => { html += `<li>${esc(c.target)} (${c.value})</li>`; });
      html += `</ul></div>`;
    }
    infoBox.html(html).style("opacity", "1");
  }
  nodeGroup.on("click", (event, d) => { showInfo(d); event.stopPropagation(); });
  svg.on("click", () => infoBox.style("opacity", "0"));

  // zoom controls
  const controls = d3.select(host).append("div")
    .style("position", "absolute").style("bottom", "10px").style("right", "10px")
    .style("display", "flex").style("gap", "5px");
  const btn = (txt, label, fn) => controls.append("button").text(txt).attr("type", "button").attr("aria-label", label).attr("title", label)
    .style("width", "30px").style("height", "30px").style("border", "1px solid var(--line)").style("border-radius", "4px")
    .style("background", "var(--panel)").style("cursor", "pointer").on("click", fn);
  btn("+", "Zoom in", () => svg.transition().duration(300).call(zoom.scaleBy, 1.5));
  btn("-", "Zoom out", () => svg.transition().duration(300).call(zoom.scaleBy, 0.75));
  btn("⟲", TX.reset, () => svg.transition().duration(300).call(zoom.transform, home));

  // list of the most frequent co-authors
  const top = nodes.filter((n) => n.group !== 0).sort((a, b) => b.count - a.count || a.id.localeCompare(b.id)).slice(0, 6);
  aside.append("h3").attr("class", "net-list-t").text(TX.top);
  const ul = aside.append("ul");
  top.forEach((n) => {
    const li = ul.append("li");
    const b = li.append("button").attr("type", "button").attr("class", "net-row")
      .on("click", () => { showInfo(n); });
    b.append("span").attr("class", "net-dot").style("background", color(n.group));
    b.append("span").attr("class", "net-name").text(n.id);
    b.append("span").attr("class", "net-count").text(n.count);
    b.on("mouseenter", () => nodeGroup.filter((d) => d.id === n.id).dispatch("mouseover"))
     .on("mouseleave", () => nodeGroup.filter((d) => d.id === n.id).dispatch("mouseout"));
  });

  // legend
  if (!container.parentElement.querySelector(".network-legend")) {
    const dot = (bg) => `<span style="display:inline-block; width:12px; height:12px; border-radius:50%; background:${bg};"></span>`;
    d3.select(container.parentElement).append("div")
      .attr("class", "network-legend")
      .style("background", "var(--bg)").style("padding", "0.8rem 1rem")
      .style("border-top", "1px solid var(--line)").style("font-size", "0.85rem").style("color", "var(--ink-2)")
      .html(`
        <div style="display:flex; flex-wrap:wrap; gap:15px; justify-content:center;">
          <div style="display:flex; align-items:center; gap:5px;">${dot("var(--navy)")} ${TX.main}</div>
          <div style="display:flex; align-items:center; gap:5px;">${dot("var(--blue-600)")} ${TX.very} (&gt;10)</div>
          <div style="display:flex; align-items:center; gap:5px;">${dot("#36a2eb")} ${TX.freq} (&ge;${freqThresh})</div>
          <div style="display:flex; align-items:center; gap:5px;">${dot("#4bc0c0")} ${TX.med} (&ge;${medThresh})</div>
          <div style="display:flex; align-items:center; gap:5px;">${dot("var(--mint)")} ${TX.occ}</div>
        </div>`);
  }

  function drag(sim) {
    return d3.drag()
      .on("start", (event, d) => { if (!event.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
      .on("drag", (event, d) => { d.fx = event.x; d.fy = event.y; })
      .on("end", (event, d) => { if (!event.active) sim.alphaTarget(0); d.fx = null; d.fy = null; });
  }
}
