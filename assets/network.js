// network.js
// Advanced D3.js Network Graph for Co-authors

function initNetworkGraph(pubs, ROOT) {
  const container = document.getElementById("network-chart-body");
  if (!container) return;
  
  // Extract authors and relationships
  const authorCounts = {};
  const linksMap = {};
  
  pubs.forEach(p => {
    if (!p.authors) return;
    const authors = p.authors;
    authors.forEach(a => {
      if (!authorCounts[a]) authorCounts[a] = 0;
      authorCounts[a]++;
    });
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
  
  // Find max co-authorship to set dynamic thresholds
  const maxCount = Math.max(1, ...Object.entries(authorCounts)
      .filter(([id]) => !id.includes("Jorge"))
      .map(([, count]) => count));
      
  const freqThresh = Math.max(3, Math.floor(maxCount * 0.6));
  const medThresh = Math.max(2, Math.floor(maxCount * 0.3));

  // Calculate node properties
  const nodes = Object.keys(authorCounts).map(id => {
    let group = 1; // Ocasional
    if (authorCounts[id] >= medThresh) group = 2; // Medio
    if (authorCounts[id] >= freqThresh) group = 3; // Frecuente
    if (authorCounts[id] > 10) group = 4; // Muy frecuente (> 10)
    if (id.includes("Párraga")) group = 0; // Main author

    return { 
      id, 
      group,
      radius: Math.min(35, 8 + authorCounts[id] * 2.5),
      count: authorCounts[id]
    };
  });
  
  const links = Object.values(linksMap);
  
  // Precompute adjacency for quick hover lookups
  const adj = {};
  nodes.forEach(n => adj[n.id] = new Set([n.id]));
  links.forEach(l => {
    adj[l.source].add(l.target);
    adj[l.target].add(l.source);
  });

  container.innerHTML = ""; // clear skeleton
  container.style.overflow = "hidden"; // ensure zoom doesn't leak
  container.style.position = "relative";
  // Remove padding from the parent chart-body to eliminate margins
  container.style.padding = "0";
  
  const width = container.clientWidth || container.parentElement.clientWidth || 800;
  const height = 400; // slightly taller for better visualization
  if (container.style.height === "300px") container.style.height = "400px";

  // Also remove padding from the parent card to maximize space
  if (container.parentElement && container.parentElement.classList.contains("metrics-chart-card")) {
    container.parentElement.style.padding = "0";
    container.parentElement.style.overflow = "hidden";
    // Adjust header padding to compensate
    const header = container.parentElement.querySelector(".chart-header");
    if (header) {
      header.style.padding = "1.35rem 1.6rem 0.7rem 1.6rem";
      header.style.margin = "0";
    }
  }

  // Color scale matching the site theme + complementary colors
  const color = d3.scaleOrdinal()
      .domain([0, 1, 2, 3, 4])
      .range(["var(--navy)", "var(--mint)", "#4bc0c0", "#36a2eb", "var(--blue-600)"]);
  
  const svg = d3.select(container).append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .style("display", "block"); // Removes bottom whitespace

  // Add zoom and pan
  const zoom = d3.zoom()
      .scaleExtent([0.3, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });
  svg.call(zoom);

  const g = svg.append("g");

  const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(d => 50 - Math.min(30, d.value * 5)))
      .force("charge", d3.forceManyBody().strength(-80))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius(d => d.radius + 8).iterations(2));

  // Apply initial zoom out to ensure everything fits
  svg.call(zoom.transform, d3.zoomIdentity.translate(width/2, height/2).scale(0.8).translate(-width/2, -height/2));
      
  const link = g.append("g")
      .attr("stroke", "var(--line-2)")
      .attr("stroke-opacity", 0.4)
    .selectAll("line")
    .data(links)
    .join("line")
      .attr("stroke-width", d => Math.sqrt(d.value) * 1.5);
      
  const nodeGroup = g.append("g")
    .selectAll("g")
    .data(nodes)
    .join("g")
      .call(drag(simulation));

  const circle = nodeGroup.append("circle")
      .attr("stroke", "#fff")
      .attr("stroke-width", 2)
      .attr("r", d => d.radius)
      .attr("fill", d => color(d.group))
      .style("cursor", "pointer")
      .style("transition", "fill 0.2s, stroke 0.2s");

  // Always show labels for top authors, hide for minor ones unless hovered
  const label = nodeGroup.append("text")
      .text(d => d.id.split(" ")[0] + (d.id.split(" ")[1] ? " " + d.id.split(" ")[1][0] + "." : ""))
      .attr("x", 0)
      .attr("y", d => d.radius + 12)
      .attr("text-anchor", "middle")
      .style("font-size", d => d.count > 5 ? "11px" : "10px")
      .style("font-family", "inherit")
      .style("font-weight", d => d.count > 10 ? "bold" : "normal")
      .style("fill", "var(--ink)")
      .style("opacity", d => d.count > 2 ? 1 : 0) // only show prominent labels by default
      .style("pointer-events", "none");

  // Hover interactions
  nodeGroup.on("mouseover", (event, d) => {
    // Fade unconnected nodes and links
    circle.style("opacity", o => adj[d.id].has(o.id) ? 1 : 0.1);
    link.style("opacity", o => (o.source.id === d.id || o.target.id === d.id) ? 1 : 0.05);
    label.style("opacity", o => adj[d.id].has(o.id) ? 1 : 0);
  }).on("mouseout", () => {
    circle.style("opacity", 1);
    link.style("opacity", 0.4);
    label.style("opacity", d => d.count > 2 ? 1 : 0);
  });
      
  // Interactive Info Box (Click)
  const infoBox = d3.select(container).append("div")
      .style("position", "absolute")
      .style("top", "10px")
      .style("right", "10px")
      .style("background", "var(--bg)")
      .style("padding", "1rem")
      .style("border", "1px solid var(--line)")
      .style("border-radius", "8px")
      .style("font-size", "0.9rem")
      .style("color", "var(--ink)")
      .style("box-shadow", "var(--shadow)")
      .style("opacity", "0")
      .style("pointer-events", "none")
      .style("max-width", "250px")
      .style("transition", "opacity 0.2s ease");

  nodeGroup.on("click", (event, d) => {
    // Find strongest connections for this node
    const connections = links
      .filter(l => l.source.id === d.id || l.target.id === d.id)
      .map(l => ({
        target: l.source.id === d.id ? l.target.id : l.source.id,
        value: l.value
      }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 3); // top 3

    let html = `<strong style="font-size:1.1em;color:var(--navy)">${d.id}</strong><br/>`;
    html += `<span style="color:var(--ink-2); display:block; margin: 0.5rem 0;">Publicaciones conjuntas: <b>${d.count}</b></span>`;
    
    if (connections.length > 0) {
      html += `<div style="font-size:0.8em; margin-top:0.5rem; border-top:1px solid var(--line); padding-top:0.5rem;">`;
      html += `<b>Principales coautores:</b><ul style="margin: 0.2rem 0; padding-left: 1rem;">`;
      connections.forEach(c => {
        html += `<li>${c.target} (${c.value})</li>`;
      });
      html += `</ul></div>`;
    }

    infoBox.html(html).style("opacity", "1");
    event.stopPropagation();
  });

  svg.on("click", () => infoBox.style("opacity", "0"));

  // Zoom controls UI
  const controls = d3.select(container).append("div")
      .style("position", "absolute")
      .style("bottom", "10px")
      .style("right", "10px")
      .style("display", "flex")
      .style("gap", "5px");

  controls.append("button")
      .text("+")
      .style("width", "30px").style("height", "30px")
      .style("border", "1px solid var(--line)").style("border-radius", "4px")
      .style("background", "var(--panel)").style("cursor", "pointer")
      .on("click", () => svg.transition().duration(300).call(zoom.scaleBy, 1.5));
      
  controls.append("button")
      .text("-")
      .style("width", "30px").style("height", "30px")
      .style("border", "1px solid var(--line)").style("border-radius", "4px")
      .style("background", "var(--panel)").style("cursor", "pointer")
      .on("click", () => svg.transition().duration(300).call(zoom.scaleBy, 0.75));

  controls.append("button")
      .text("⟲")
      .style("width", "30px").style("height", "30px")
      .style("border", "1px solid var(--line)").style("border-radius", "4px")
      .style("background", "var(--panel)").style("cursor", "pointer")
      .on("click", () => svg.transition().duration(300).call(zoom.transform, d3.zoomIdentity));

  // Legend UI
  // Check if legend already exists to avoid duplicating on re-renders
  if (!container.parentElement.querySelector(".network-legend")) {
    const legend = d3.select(container.parentElement).append("div")
        .attr("class", "network-legend")
        .style("background", "var(--bg)")
        .style("padding", "0.8rem 1rem")
        .style("border-top", "1px solid var(--line)")
        .style("font-size", "0.85rem")
        .style("color", "var(--ink-2)")
        .html(`
          <div style="display:flex; flex-wrap:wrap; gap:15px; justify-content:center;">
            <div style="display:flex; align-items:center; gap:5px;"><span style="display:inline-block; width:12px; height:12px; border-radius:50%; background:var(--navy);"></span> Autor principal</div>
            <div style="display:flex; align-items:center; gap:5px;"><span style="display:inline-block; width:12px; height:12px; border-radius:50%; background:var(--blue-600);"></span> Muy Frecuente (>10)</div>
            <div style="display:flex; align-items:center; gap:5px;"><span style="display:inline-block; width:12px; height:12px; border-radius:50%; background:#36a2eb;"></span> Frecuente (>=${freqThresh})</div>
            <div style="display:flex; align-items:center; gap:5px;"><span style="display:inline-block; width:12px; height:12px; border-radius:50%; background:#4bc0c0;"></span> Medio (>=${medThresh})</div>
            <div style="display:flex; align-items:center; gap:5px;"><span style="display:inline-block; width:12px; height:12px; border-radius:50%; background:var(--mint);"></span> Ocasional</div>
          </div>
        `);
  }

  simulation.on("tick", () => {
    link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
        
    nodeGroup.attr("transform", d => `translate(${d.x},${d.y})`);
  });
  
  function drag(simulation) {
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x; d.fy = d.y;
    }
    function dragged(event, d) {
      d.fx = event.x; d.fy = event.y;
    }
    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null; d.fy = null;
    }
    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
  }
}
