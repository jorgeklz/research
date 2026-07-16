/* Jorge Parraga-Alava — researcher profile
   Minimalist, blue/white, Avenir. Top-right menu. Separate pages.
   Publications live from ORCID (+ local enrichment) with pagination.
   Dynamic plain-language post generation from Crossref. */

(function () {
  "use strict";

  const LANG = document.documentElement.lang === "es" ? "es" : "en";
  const ROOT = document.body.dataset.root || ".";
  const PAGE = document.body.dataset.page;
  const POST_PAGE = LANG === "es" ? "entrada.html" : "post.html";
  const ORCID_ID = "0000-0001-8558-9122";
  const PAGE_SIZE = 5;
  // works hidden from the site (and therefore from the metrics)
  const EXCLUDE_DOIS = new Set(["10.1063/5.0187487"]);
  const isExcluded = (p) => p && EXCLUDE_DOIS.has((p.doi || "").toLowerCase());

  const T = {
    en: {
      journal: "Journal", conference: "Conference", software: "Software", book: "Book chapter",
      paper: "New paper", news: "Posts",
      readMore: "Read the post", cite: "Cite", copied: "BibTeX copied", doi: "DOI",
      openAccess: "Open access", all: "All", post: "Post", aboutPaper: "About the paper", readPaper: "Read the paper",
      readOriginalPaper: "Read the original paper",
      postLink: "Explanatory post", article: "Article", minRead: "min read", cvEdu: "Education", cvExp: "Academic experience", cvAwards: "Awards & recognition",
      views: "views", viewsOne: "view", shareWa: "Share on WhatsApp",
      empty: "Nothing here yet.", notFound: "Post not found.", loadingOrcid: "Loading publications from ORCID…",
      syncedOrcid: "Live from ORCID", worksTotal: "publications",
      prev: "← Prev", next: "Next →", pageOf: (a, b) => `Page ${a} of ${b}`, goTo: "Go to",
      backNews: "← All posts", generating: "Preparing a plain-language summary…",
      autoNote: "Summary generated automatically from the publication metadata.",
      autoSummary: "Read a plain-language summary of this paper, generated from its abstract.",
      loadFail: "Could not load data. Serve the site with a local server (python3 -m http.server) instead of opening the file directly.",
      orcidFail: "Could not reach ORCID. Showing the curated list instead."
    },
    es: {
      journal: "Revista", conference: "Congreso", software: "Software", book: "Capítulo de libro",
      paper: "Nuevo artículo", news: "Posts",
      readMore: "Leer el post", cite: "Citar", copied: "BibTeX copiado", doi: "DOI",
      openAccess: "Acceso abierto", all: "Todas", post: "Post", aboutPaper: "Sobre el artículo", readPaper: "Leer el paper",
      readOriginalPaper: "Leer el paper original",
      postLink: "Post explicativo de la publicación", article: "Artículo", minRead: "min de lectura", cvEdu: "Educación", cvExp: "Experiencia académica", cvAwards: "Premios y reconocimientos",
      views: "vistas", viewsOne: "vista", shareWa: "Compartir en WhatsApp",
      empty: "Aún no hay contenido.", notFound: "Entrada no encontrada.", loadingOrcid: "Cargando publicaciones desde ORCID…",
      syncedOrcid: "En vivo desde ORCID", worksTotal: "publicaciones",
      prev: "← Ant.", next: "Sig. →", pageOf: (a, b) => `Página ${a} de ${b}`, goTo: "Ir a",
      backNews: "← Todos los posts", generating: "Preparando un resumen divulgativo…",
      autoNote: "Resumen generado automáticamente a partir de los metadatos de la publicación.",
      autoSummary: "Lee un resumen en lenguaje simple de este artículo, generado a partir de su abstract.",
      loadFail: "No se pudieron cargar los datos. Sirve el sitio con un servidor local (python3 -m http.server).",
      orcidFail: "No se pudo conectar con ORCID. Se muestra la lista curada."
    }
  }[LANG];

  const $ = (s, el) => (el || document).querySelector(s);
  const $$ = (s, el) => Array.from((el || document).querySelectorAll(s));
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const pick = (v) => (v && typeof v === "object" && (v.en || v.es) ? (v[LANG] || v.en || v.es) : v);
  const normDoi = (d) => (d || "").toLowerCase().trim();

  const VER = "17";
  const fetchJSON = (name) => fetch(`${ROOT}/data/${name}.json?v=${VER}`).then((r) => {
    if (!r.ok) throw new Error(name + ": " + r.status); return r.json();
  });

  /* ---------- line icons (stroke = currentColor) ---------- */
  const svg = (inner, w) => `<svg width="${w || 15}" height="${w || 15}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${inner}</svg>`;
  const ICON = {
    scholar: svg('<path d="M12 3 2 8l10 5 10-5-10-5Z"/><path d="M5 10v5c0 1.5 3.1 3 7 3s7-1.5 7-3v-5"/><path d="M22 8v5"/>'),
    scopus: svg('<circle cx="12" cy="12" r="9"/><path d="M15 9.2a4 4 0 1 0 0 5.6"/>'),
    wos: svg('<circle cx="12" cy="12" r="2.2"/><circle cx="5" cy="6" r="1.6"/><circle cx="19" cy="6" r="1.6"/><circle cx="5" cy="18" r="1.6"/><circle cx="19" cy="18" r="1.6"/><path d="M10.3 10.6 6.2 7M13.7 10.6 17.8 7M10.3 13.4 6.2 17M13.7 13.4 17.8 17"/>'),
    orcid: svg('<circle cx="12" cy="12" r="9"/><line x1="9.2" y1="9" x2="9.2" y2="16.5"/><circle cx="9.2" cy="6.6" r=".2"/><path d="M12.4 9v7.5h2.2a3.75 3.75 0 0 0 0-7.5h-2.2Z"/>'),
    dblp: svg('<line x1="8" y1="6" x2="20" y2="6"/><line x1="8" y1="12" x2="20" y2="12"/><line x1="8" y1="18" x2="20" y2="18"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/>'),
    github: svg('<path d="M9 19c-4 1.5-4-2-6-2.5m12 4.5v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1-.3-3.4 1.3a11.6 11.6 0 0 0-6 0C6.9 3.5 5.9 3.8 5.9 3.8a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4.5 10.2c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/>'),
    link: svg('<path d="M10 13a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1.5 1.5"/><path d="M14 11a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1.5-1.5"/>', 13),
    external: svg('<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>', 13),
    cite: svg('<path d="M7 8H5a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v3l3-3a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2Z"/><path d="M18 8h-2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v3l3-3a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2Z"/>', 13),
    oa: svg('<rect x="4" y="11" width="16" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 7.5-2"/><circle cx="12" cy="15.5" r="1.3"/>', 13),
    doc: svg('<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9Z"/><polyline points="14 3 14 9 20 9"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="13" y2="17"/>', 13),
    mail: svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>', 14),
    arrow: svg('<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>', 12),
    read: svg('<path d="M12 6.5C9 3.5 4.5 4 3 4v13c1.5 0 6-.5 9 2.5M12 6.5C15 3.5 19.5 4 21 4v13c-1.5 0-6-.5-9 2.5M12 6.5V19"/>', 16),
    cal: svg('<rect x="3" y="4.5" width="18" height="16" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="8" y1="2.5" x2="8" y2="6"/><line x1="16" y1="2.5" x2="16" y2="6"/>', 13),
    clock: svg('<circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15.5 14"/>', 13),
    eye: svg('<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>', 13),
    pin: svg('<path d="M12 21s7-6.4 7-11.5A7 7 0 1 0 5 9.5C5 14.6 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.3"/>', 13),
    whatsapp: svg('<path d="M3 21l1.4-4.4A8 8 0 1 1 8.6 19.6 8 8 0 0 1 3 21Z"/><path d="M8.7 8.4c.3 0 .5.35.6.6l.5 1.35c.05.15.05.3-.05.45l-.45.6c-.1.15-.1.3 0 .45.35.6.85 1.2 1.4 1.65.55.45 1.15.8 1.75 1.05.15.05.3.05.4-.05l.55-.55c.15-.15.3-.15.45-.1l1.3.55c.25.1.55.3.55.6 0 .6-.4 1.2-.95 1.4-.6.25-1.3.3-2.15 0a7.2 7.2 0 0 1-2.9-1.85 7.2 7.2 0 0 1-1.85-2.9c-.3-.85-.25-1.55 0-2.15.2-.55.8-.95 1.4-.95Z"/>', 13),
    tJournal: svg('<path d="M4 5a2 2 0 0 1 2-2h5v16H6a2 2 0 0 0-2 2V5Z"/><path d="M20 5a2 2 0 0 0-2-2h-5v16h5a2 2 0 0 1 2 2V5Z"/>', 13),
    tConf: svg('<rect x="3" y="4" width="18" height="12" rx="2"/><line x1="12" y1="16" x2="12" y2="20"/><line x1="8" y1="20" x2="16" y2="20"/><polyline points="8.5 11 11 8.5 13 10.5 16 7"/>', 13),
    tSoft: svg('<polyline points="9 8 5 12 9 16"/><polyline points="15 8 19 12 15 16"/>', 13),
    // metric icons
    mPub: svg('<path d="M4 4h9l3 3v13H4z"/><path d="M13 4v3h3"/><line x1="7" y1="12" x2="13" y2="12"/><line x1="7" y1="16" x2="12" y2="16"/>'),
    mCite: svg('<path d="M7 7H4v5h3v5l3-3V7zM17 7h-3v5h3v5l3-3V7z"/>'),
    mH: svg('<line x1="4" y1="20" x2="20" y2="20"/><rect x="5" y="12" width="3.5" height="8"/><rect x="10.5" y="7" width="3.5" height="13"/><rect x="16" y="14" width="3.5" height="6"/>'),
    mCpp: svg('<line x1="7" y1="18" x2="17" y2="6"/><circle cx="7.5" cy="7.5" r="1.6"/><circle cx="16.5" cy="16.5" r="1.6"/>'),
    mI10: svg('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.4"/><circle cx="12" cy="12" r="0.6" fill="currentColor"/>'),
    mG: svg('<circle cx="12" cy="12" r="8"/><path d="M15.5 9.5A4 4 0 1 0 16 14h-3"/>'),
    mM: svg('<polyline points="4 16 10 10 13 13 20 6"/><polyline points="15 6 20 6 20 11"/>'),
    mAuth: svg('<circle cx="9" cy="8" r="3"/><path d="M3.5 20a5.5 5.5 0 0 1 11 0"/><path d="M16 6a3 3 0 0 1 0 6"/><path d="M17 14.5a5.5 5.5 0 0 1 3.5 5.5"/>'),
    mFirst: svg('<polygon points="12 3 14.5 9 21 9.5 16 13.7 17.6 20 12 16.5 6.4 20 8 13.7 3 9.5 9.5 9"/>'),
    mCited: svg('<circle cx="12" cy="12" r="9"/><polyline points="8 12.5 11 15.5 16 9"/>')
  };
  function socialIcon(label) {
    const k = label.toLowerCase();
    if (k.includes("scholar")) return ICON.scholar;
    if (k.includes("scopus")) return ICON.scopus;
    if (k.includes("science") || k.includes("wos")) return ICON.wos;
    if (k.includes("orcid")) return ICON.orcid;
    if (k.includes("dblp")) return ICON.dblp;
    if (k.includes("github")) return ICON.github;
    return ICON.link;
  }

  /* ---------- text utils ---------- */
  function md(text) {
    return String(text || "").split(/\n\s*\n/).map((blk) => {
      let b = esc(blk.trim()); if (!b) return "";
      b = b.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/\*(.+?)\*/g, "<em>$1</em>")
           .replace(/`(.+?)`/g, "<code>$1</code>")
           .replace(/\[(.+?)\]\((https?:[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
      if (b.startsWith("## ")) return `<h2>${b.slice(3)}</h2>`;
      return `<p>${b.replace(/\n/g, "<br>")}</p>`;
    }).join("\n");
  }
  const firstPara = (t) => String(t || "").split(/\n\s*\n/)[0] || "";
  const stripJats = (t) => {
    let s = String(t || "");
    // Crossref/OpenAlex sometimes double-escape JATS markup (e.g. "&amp;lt;jats:italic&amp;gt;");
    // decode entities repeatedly (bounded) so any nested escaping is fully resolved before we strip tags.
    const d = document.createElement("div");
    for (let i = 0; i < 3; i++) {
      d.innerHTML = s;
      const decoded = d.textContent;
      if (decoded === s) break;
      s = decoded;
    }
    // now remove any real/decoded tags (JATS <italic>, <sub>, <mml:...>, etc.)
    d.innerHTML = s.replace(/<[^>]+>/g, " ");
    s = d.textContent;
    // normalize unicode (combining forms -> precomposed) so accents render consistently
    if (s.normalize) s = s.normalize("NFC");
    return s
      .replace(/\s+/g, " ")
      .replace(/\s+([,.;:!?])/g, "$1")   // stray space before punctuation left by tag removal
      .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "") // stray control chars
      .trim();
  };
  const fmtDate = (iso) => { try { return new Date(iso + "T12:00:00").toLocaleDateString(LANG === "es" ? "es-EC" : "en-GB", { year: "numeric", month: "short", day: "numeric" }); } catch (e) { return iso; } };
  const boldSelf = (a) => {
    const marked = a.map((x) => /parraga|párraga/i.test(x) ? `<b>${esc(x)}</b>` : esc(x));
    if (marked.length <= 1) return marked.join("");
    const conj = LANG === "es" ? " y " : " and ";
    return marked.slice(0, -1).join(", ") + conj + marked[marked.length - 1];
  };
  const typeLabel = (t) => T[t] || (t === "journal-article" ? T.journal : /conf|proceed/.test(t || "") ? T.conference : t) || "";

  function bibtex(p) {
    const key = (p.authors && p.authors[0] || "ref").split(/\s+/).pop().toLowerCase().replace(/[^a-z]/g, "") + (p.year || "");
    const kind = p.type === "journal" ? "article" : "inproceedings";
    const field = p.type === "journal" ? "journal" : "booktitle";
    const L = [`@${kind}{${key},`, `  author    = {${(p.authors || []).join(" and ")}},`,
      `  title     = {${p.title}},`, `  ${field} = {${p.venue || ""}},`, `  year      = {${p.year || ""}},`];
    if (p.pages) L.push(`  pages     = {${p.pages}},`);
    if (p.doi) L.push(`  doi       = {${p.doi}},`);
    L.push("}"); return L.join("\n");
  }
  function toast(msg) {
    let t = $("#toast"); if (!t) { t = document.createElement("div"); t.id = "toast"; document.body.appendChild(t); }
    t.textContent = msg; t.classList.add("show"); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove("show"), 1700);
  }
  const indexPosts = (posts) => { const m = {}; (posts.items || []).forEach((p) => m[p.id] = p); return m; };


  function updateGoto(container, pages, current, onGo) {
    if (!container) return;
    let g = container.querySelector(".goto");
    if (!g) {
      g = document.createElement("label");
      g.className = "goto";
      g.innerHTML = `<span>${T.goTo}</span><select aria-label="${T.goTo}"></select>`;
      container.appendChild(g);
      g.querySelector("select").addEventListener("change", (e) => onGo(parseInt(e.target.value, 10)));
    }
    const sel = g.querySelector("select");
    if (sel.options.length !== pages) {
      sel.innerHTML = "";
      for (let i = 0; i < pages; i++) {
        const o = document.createElement("option");
        o.value = String(i); o.textContent = String(i + 1);
        sel.appendChild(o);
      }
    }
    sel.value = String(current);
    g.style.display = pages > 1 ? "inline-flex" : "none";
  }

  /* ---------- Crossref ---------- */
  function crossref(doi) {
    return fetch("https://api.crossref.org/works/" + encodeURIComponent(doi))
      .then((r) => { if (!r.ok) throw new Error("cr " + r.status); return r.json(); })
      .then((j) => {
        const m = j.message || {};
        const authors = (m.author || []).map((a) => [a.given, a.family].filter(Boolean).join(" ")).filter(Boolean);
        let year = null;
        for (const k of ["published-print", "published-online", "issued"]) {
          const dp = (m[k] || {})["date-parts"]; if (dp && dp[0] && dp[0][0]) { year = dp[0][0]; break; }
        }
        const ct = m["container-title"] || [];
        const venueName = stripJats(ct[0] || "");
        const venueLooksLikeConference = /conference|proceedings|symposium|workshop|congress|congreso/i.test(venueName);
        let type = m.type === "journal-article" ? "journal" : /proceed|conf/.test(m.type || "") ? "conference" : "other";
        if (venueLooksLikeConference) type = "conference";
        return {
          title: stripJats((m.title || [""])[0]), authors, venue: venueName, year,
          pages: m.page || null, type, abstract: stripJats(m.abstract || ""),
          openAccess: (m.license || []).some((l) => /creativecommons/.test(l.URL || ""))
        };
      });
  }

  /* ---------- secondary abstract source: OpenAlex (covers many DOIs Crossref lacks) ---------- */
  function openAlexAbstract(doi) {
    return fetch("https://api.openalex.org/works/https://doi.org/" + encodeURIComponent(doi))
      .then((r) => (r.ok ? r.json() : null))
      .then((j) => {
        const idx = j && j.abstract_inverted_index;
        if (!idx) return "";
        const words = [];
        Object.keys(idx).forEach((w) => { idx[w].forEach((pos) => { words[pos] = w; }); });
        return words.join(" ").replace(/\s+/g, " ").trim();
      })
      .catch(() => "");
  }
  function topicLabel(t) { return String(t || "").replace(/-/g, " "); }
  /* crude EN/ES language guess so we never silently pass off an English abstract as a Spanish one */
  function looksEnglish(text) {
    const t = " " + String(text || "").toLowerCase() + " ";
    const en = (t.match(/ (the|and|of|is|with|this|were|from|study|using|based) /g) || []).length;
    const es = (t.match(/ (el|la|los|las|de|que|es|con|este|esta|estudio|para|una|del) /g) || []).length;
    return en > es;
  }

  /* ---------- dynamic bilingual post from metadata (Crossref abstract) ---------- */
  function splitParagraphs(text, n) {
    const clean = String(text || "").replace(/\s+/g, " ").trim();
    // Abbreviations whose trailing "." must not be treated as a sentence end.
    const ABBR = /\b(et al|e\.g|i\.e|vs|cf|approx|fig|figs|eq|eqs|no|pp|p|vol|ref|refs|dr|mr|mrs|ms|prof|st|dept|resp|resp|vol|no)\.$/i;
    const raw = clean.match(/[^.!?]+[.!?]+(?:["')\]]+)?\s*/g) || [clean];
    const sents = [];
    for (const piece of raw) {
      const trimmed = piece.trim();
      if (!trimmed) continue;
      const prev = sents[sents.length - 1];
      // merge with previous fragment if it ended on a known abbreviation, or if this
      // fragment is just a lone number/letter (decimal points, initials, "Fig. 3.")
      if (prev && (ABBR.test(prev) || /\d\.$/.test(prev) && /^\d/.test(trimmed) || /^[a-z0-9]$/i.test(trimmed.replace(/[.)\]]+$/, "")))) {
        sents[sents.length - 1] = (prev + " " + trimmed).trim();
      } else {
        sents.push(trimmed);
      }
    }
    if (sents.length <= 1) return [clean];
    const per = Math.max(1, Math.ceil(sents.length / n)), out = [];
    for (let i = 0; i < sents.length; i += per) out.push(sents.slice(i, i + per).join(" ").trim());
    return out.filter(Boolean);
  }
  function buildPost(meta, doi) {
    const venue = meta.venue || "";
    const abs = meta.abstract || "";
    const oaEn = meta.openAccess ? " It is open access, so anyone can read it in full." : "";
    const oaEs = meta.openAccess ? " Es de acceso abierto, así que cualquiera puede leerlo completo." : "";
    const abstractIsEnglish = abs && looksEnglish(abs);
    const esNote = abstractIsEnglish
      ? `*Nota: aún no hay una versión en español de este resumen; se muestra tal como aparece en la fuente original (inglés).*\n\n`
      : "";

    let en, es;
    if (abs) {
      const parts = splitParagraphs(abs, 3);
      en = parts.join("\n\n") +
        `\n\nYou can read the full paper through the link below.${oaEn}`;
      es = esNote + parts.join("\n\n") +
        `\n\nPuedes leer el artículo completo en el enlace de abajo.${oaEs}`;
    } else {
      const topics = (meta.topics || []).map(topicLabel);
      const topicsEn = topics.length
        ? `Based on its publication record, this work relates to ${topics.slice(0, 3).join(", ")}.\n\n`
        : "";
      const topicsEs = topics.length
        ? `Según su registro de publicación, este trabajo se relaciona con ${topics.slice(0, 3).join(", ")}.\n\n`
        : "";
      en = `The publisher does not provide a public abstract for this work, so this page is limited to what is listed in its metadata; the full details live in the paper itself.\n\n` +
        topicsEn +
        `You can read the full paper through the link below.${oaEn}`;
      es = `La editorial no ofrece un resumen público de este trabajo, así que esta página se limita a lo que indican sus metadatos; los detalles completos están en el propio artículo.\n\n` +
        topicsEs +
        `Puedes leer el artículo completo en el enlace de abajo.${oaEs}`;
    }

    return {
      auto: true, doi,
      date: (meta.year ? meta.year + "-01-01" : new Date().toISOString().slice(0, 10)),
      type: meta.type === "conference" ? "conference" : meta.type === "software" ? "software" : "journal",
      title: { en: meta.title, es: meta.title },
      summary: {
        en: `New publication${venue ? " in " + venue : ""}${meta.year ? " (" + meta.year + ")" : ""}.`,
        es: `Nueva publicación${venue ? " en " + venue : ""}${meta.year ? " (" + meta.year + ")" : ""}.`
      },
      body: { en, es },
      links: doi ? [{ label: "DOI", url: "https://doi.org/" + doi }] : []
    };
  }

  /* ---------- publication card ---------- */
  function pubEl(p, byId) {
    const el = document.createElement("article");
    el.className = "pub";
    const doiURL = p.doi ? "https://doi.org/" + p.doi : null;
    const curated = p.postId && byId[p.postId];
    // only offer an explanatory post for curated ones or 2024+ publications
    const postHref = curated ? `${POST_PAGE}?id=${encodeURIComponent(p.postId)}`
      : (p.doi && (p.year || 0) >= 2024 ? `${POST_PAGE}?doi=${encodeURIComponent(p.doi)}` : null);
    el.innerHTML = `
      <h3>${doiURL ? `<a href="${doiURL}" target="_blank" rel="noopener">` : ""}${esc(p.title)}${doiURL ? "</a>" : ""}</h3>
      ${p.authors && p.authors.length ? `<p class="auth">${boldSelf(p.authors)}</p>` : ""}
      <div class="meta">
        <span class="yrchip">${p.year || "—"} · ${esc(typeLabel(p.type))}</span>
        ${p.venue ? `<span class="ven">${esc(p.venue)}${p.pages ? ", " + esc(p.pages) : ""}</span>` : ""}
      </div>
      <div class="act">
        ${doiURL ? `<a href="${doiURL}" target="_blank" rel="noopener">${ICON.external} ${T.doi}</a>` : ""}
        <button type="button" class="bib">${ICON.cite} ${T.cite}</button>
        ${p.openAccess ? `<a class="oa" href="${doiURL || "#"}" target="_blank" rel="noopener">${ICON.oa} ${T.openAccess}</a>` : ""}
        ${postHref ? `<a href="${postHref}">${ICON.doc} ${T.postLink}</a>` : ""}
      </div>`;
    el.querySelector("button.bib").addEventListener("click", () =>
      navigator.clipboard.writeText(bibtex(p)).then(() => toast(T.copied)).catch(() => toast(T.copied)));
    return el;
  }

  /* ---------- shared: curated list + ORCID live fetch/merge (used by Publications and News pages) ---------- */
  function curatedPubsSorted(pubs) {
    return [...pubs.items].sort((a, b) => (b.year || 0) - (a.year || 0));
  }
  function fetchLivePubs(pubs) {
    const curatedList = curatedPubsSorted(pubs);
    const localByDoi = {}; pubs.items.forEach((p) => { if (p.doi) localByDoi[normDoi(p.doi)] = p; });
    return fetch(`https://pub.orcid.org/v3.0/${ORCID_ID}/works`, { headers: { Accept: "application/json" } })
      .then((r) => { if (!r.ok) throw new Error("orcid " + r.status); return r.json(); })
      .then((data) => {
        const groups = data.group || [];
        const works = groups.map((g) => g["work-summary"] && g["work-summary"][0]).filter(Boolean).map((w) => {
          const title = (w.title && w.title.title && w.title.title.value) || "";
          const year = (w["publication-date"] && w["publication-date"].year && w["publication-date"].year.value) || null;
          const jt = (w["journal-title"] && w["journal-title"].value) || "";
          let doi = null;
          const ids = (w["external-ids"] && w["external-ids"]["external-id"]) || [];
          const d = ids.find((e) => e["external-id-type"] === "doi"); if (d) doi = d["external-id-value"];
          const wtype = (w.type || "").toLowerCase();
          const type = wtype.includes("journal") ? "journal" : (wtype.includes("conference") || wtype.includes("proceed")) ? "conference" : (wtype.includes("book") ? "book" : "other");
          const local = doi && localByDoi[normDoi(doi)];
          if (local) return Object.assign({}, local);
          return { title, year: year ? Number(year) : null, venue: jt, doi, type, authors: [], _needsEnrich: !!doi };
        }).filter((w) => w.title);
        // dedupe by doi/title, keep ORCID order (already year-grouped) then sort by year desc
        const seen = new Set();
        const merged = [];
        works.forEach((w) => { if (isExcluded(w)) return; const k = normDoi(w.doi) || w.title.toLowerCase(); if (!seen.has(k)) { seen.add(k); merged.push(w); } });
        // include any local not present
        curatedList.forEach((p) => { if (isExcluded(p)) return; const k = normDoi(p.doi) || p.title.toLowerCase(); if (!seen.has(k)) { seen.add(k); merged.push(p); } });
        merged.sort((a, b) => (b.year || 0) - (a.year || 0));
        return merged;
      });
  }

  /* ---------- Publications page: ORCID live + local merge + pagination ---------- */
  function fillPublications(profile, pubs, posts) {
    const list = $("#pub-list"), fw = $("#pub-filters"), byId = indexPosts(posts);
    const pag = $("#pub-pagination"), info = $("#pag-info");
    const prev = $("#pag-prev"), next = $("#pag-next"), note = $("#orcid-note");

    let all = [], filtered = [], type = "all", page = 0;

    function apply() {
      filtered = type === "all" ? all : all.filter((p) => p.type === type);
      page = 0; render();
    }
    function render() {
      const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
      page = Math.min(page, pages - 1);
      list.innerHTML = "";
      const slice = filtered.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE);
      if (!slice.length) { list.innerHTML = `<p class="loading">${T.empty}</p>`; }
      slice.forEach((p) => {
        const el = pubEl(p, byId); list.appendChild(el);
        if (p._needsEnrich && p.doi) enrich(p, el);
      });
      if (pag) {
        pag.style.display = filtered.length > PAGE_SIZE ? "flex" : "none";
        info.textContent = T.pageOf(page + 1, pages);
        prev.disabled = page === 0; next.disabled = page >= pages - 1;
        updateGoto(pag, pages, page, (i) => { page = Math.max(0, Math.min(i, pages - 1)); render(); window.scrollTo({ top: 0, behavior: "smooth" }); });
      }
    }
    function enrich(p, el) {
      p._needsEnrich = false;
      crossref(p.doi).then((m) => {
        if (m.authors.length) p.authors = m.authors;
        if (m.venue) p.venue = m.venue;
        if (m.pages) p.pages = m.pages;
        if (m.type !== "other") p.type = m.type;
        if (m.openAccess) p.openAccess = true;
        const fresh = pubEl(p, byId);
        el.replaceWith(fresh);
      }).catch(() => {});
    }

    if (prev) prev.addEventListener("click", () => { if (page > 0) { page--; render(); window.scrollTo({ top: 0, behavior: "smooth" }); } });
    if (next) next.addEventListener("click", () => { page++; render(); window.scrollTo({ top: 0, behavior: "smooth" }); });

    if (fw) {
      const types = ["all", "journal", "conference"];
      fw.innerHTML = types.map((t) => `<button data-t="${t}" class="${t === "all" ? "on" : ""}">${t === "all" ? T.all : T[t]}</button>`).join("");
      fw.addEventListener("click", (e) => {
        const b = e.target.closest("button"); if (!b) return;
        fw.querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b));
        type = b.dataset.t; apply();
      });
    }

    // curated (local) list as immediate fallback
    all = curatedPubsSorted(pubs); apply();

    // live ORCID
    fetchLivePubs(pubs)
      .then((merged) => {
        all = merged;
        if (note) note.querySelector(".txt").textContent = `${merged.length} ${T.worksTotal} · ${T.syncedOrcid}`;
        apply();
        // metrics computed strictly over the publications shown on the site
        if ($("#stat-grid")) {
          renderMetrics(computeMetrics(shownMetricList(merged, null)));
          fetchOpenAlexMap()
            .then((map) => renderMetrics(computeMetrics(shownMetricList(merged, map))))
            .catch(() => {});
        }
      })
      .catch(() => { if (note) note.querySelector(".txt").textContent = T.orcidFail; });
  }

  /* ---------- other pages ---------- */
  function readingMinutes(post) {
    const t = pick(post.body) || "";
    const words = t.replace(/[#*`>_\[\]()]/g, " ").split(/\s+/).filter(Boolean).length;
    return Math.max(1, Math.round(words / 200));
  }
  /* ---------- visit counter (per post, shared across visitors) ---------- */
  const VIEWS_NS = "jorgeparragaalava-site-posts";
  function postViewKey(post) {
    return post.id || (post.doi ? "doi-" + normDoi(post.doi) : "page-" + location.search);
  }
  function loadViewCount(post) {
    const wrap = $("#post-views");
    if (!wrap) return;
    const label = wrap.querySelector(".views-count");
    const key = encodeURIComponent(postViewKey(post));
    const show = (raw) => {
      const n = Number(raw) || 1;
      const fmt = n.toLocaleString(LANG === "es" ? "es-EC" : "en-US");
      label.textContent = `${fmt} ${n === 1 ? T.viewsOne : T.views}`;
    };
    // primary: Abacus (abacus.jasoncameron.dev). countapi.xyz is discontinued, so it is not used here.
    fetch(`https://abacus.jasoncameron.dev/hit/${VIEWS_NS}/${key}`)
      .then((r) => { if (!r.ok) throw new Error("abacus"); return r.json(); })
      .then((d) => show(d.value))
      .catch(() => {
        // fallback: CounterAPI v1 (no auth required)
        fetch(`https://api.counterapi.dev/v1/${VIEWS_NS}/${key}/up`)
          .then((r) => { if (!r.ok) throw new Error("counterapi"); return r.json(); })
          .then((d) => show(d.value))
          .catch(() => { wrap.style.display = "none"; });
      });

  }
  function parseVenueLocation(venue) {
    const parts = String(venue || "").split(",").map((s) => s.trim()).filter(Boolean);
    if (parts.length < 3) return null;
    const city = parts[1];
    const country = parts[2].replace(/\s*\([^)]*\)\s*$/, "").trim();
    if (!city || !country) return null;
    return `${city}, ${country}`;
  }
  function pubKind(post, pubs) {
    const pub = post.doi && (pubs.items || []).find((p) => normDoi(p.doi) === normDoi(post.doi));
    const type = pub ? pub.type : (["conference", "software"].includes(post.type) ? post.type : "journal");
    const venue = (pub && pub.venue) || (post._ref && post._ref.venue) || "";
    if (type === "conference") return { label: T.conference, icon: ICON.tConf, location: parseVenueLocation(venue) };
    if (type === "software") return { label: T.software, icon: ICON.tSoft };
    return { label: T.journal, icon: ICON.tJournal };
  }
  function postMeta(post, pubs, opts) {
    opts = opts || {};
    const k = pubKind(post, pubs);
    const mins = readingMinutes(post);
    const locHtml = k.location ? `<span class="mi">${ICON.pin}${esc(k.location)}</span>` : "";
    const viewsHtml = opts.showViews
      ? `<span class="mi" id="post-views">${ICON.eye}<span class="views-count">···</span></span>`
      : "";
    const shareHtml = opts.shareUrl
      ? `<a class="mi share-wa" href="https://api.whatsapp.com/send?text=${encodeURIComponent(pick(post.title) + " — " + opts.shareUrl)}" target="_blank" rel="noopener">${ICON.whatsapp}<span>${esc(T.shareWa)}</span></a>`
      : "";
    return `<div class="meta">
      <span class="mi">${ICON.cal}<time datetime="${esc(post.date)}">${fmtDate(post.date)}</time></span>
      <span class="mi">${k.icon}${esc(k.label)}</span>
      ${locHtml}
      <span class="mi">${ICON.clock}${mins} ${esc(T.minRead)}</span>
      ${viewsHtml}
      ${shareHtml}
    </div>`;
  }
  function postCardHref(post) {
    return post.id ? `${POST_PAGE}?id=${encodeURIComponent(post.id)}`
      : `${POST_PAGE}?doi=${encodeURIComponent(post.doi)}`;
  }
  function cardEl(post, pubs) {
    const el = document.createElement("article"); el.className = "card";
    const href = postCardHref(post);
    el.innerHTML = `
      ${postMeta(post, pubs)}
      <h3><a href="${href}">${esc(pick(post.title))}</a></h3>
      <p>${esc(pick(post.summary))}</p>
      <a class="more" href="${href}">${T.readMore} ${ICON.arrow}</a>`;
    return el;
  }
  function rowsEl(container, items, kind) {
    container.innerHTML = "";
    items.forEach((it) => {
      const el = document.createElement("div"); el.className = "row";
      const when = (kind === "edu" || kind === "award") ? it.year : it.period;
      const badge = it.note ? `<span class="badge">${esc(pick(it.note))}</span>` : "";
      const org = esc(pick(it.org));
      const orgHtml = it.orgUrl ? `<a href="${esc(it.orgUrl)}" target="_blank" rel="noopener">${org}</a>` : org;
      el.innerHTML = `<div class="when">${esc(when)}</div><div class="what"><div class="t">${esc(pick(it.title || it.role))}${badge}</div><div class="o">${orgHtml}</div></div>`;
      container.appendChild(el);
    });
  }

  function fillChrome(profile) {
    const name = LANG === "es" && profile.nameEs ? profile.nameEs : profile.name;
    $$(".brand .bname").forEach((e) => e.textContent = name);
    $$(".brand .logo").forEach((e) => e.setAttribute("alt", name));
    const soc = $("#socials");
    if (soc && profile.profiles) {
      soc.innerHTML = profile.profiles.map((p) =>
        `<a href="${esc(p.url)}" target="_blank" rel="noopener" title="${esc(p.label)}">${socialIcon(p.label)}<span>${esc(p.label)}</span></a>`).join("");
    }
    const mail = $("#foot-mail");
    if (mail) { mail.innerHTML = `${ICON.mail} <a href="mailto:${esc(profile.email)}">${esc(profile.email)}</a>`; }
    const yr = $("#foot-year"); if (yr) yr.textContent = new Date().getFullYear();
  }

  // ---------- bibliometrics computed from the full ORCID publication set ----------
  const METRIC_ICON = { pubs: ICON.mPub, cites: ICON.mCite, h: ICON.mH, cpp: ICON.mCpp,
    i10: ICON.mI10, g: ICON.mG, m: ICON.mM, app: ICON.mAuth, first: ICON.mFirst, cited: ICON.mCited };
  const METRICS = {
    en: [
      { k: "pubs", label: "Publications", abbr: "P" },
      { k: "cites", label: "Citations", abbr: "C" },
      { k: "h", label: "h-index", abbr: "h" },
      { k: "cpp", label: "Citations per publication", abbr: "C/P" },
      { k: "i10", label: "i10-index", abbr: "i10" },
      { k: "g", label: "g-index", abbr: "g" },
      { k: "m", label: "m-index", abbr: "m" },
      { k: "app", label: "Authors per publication", abbr: "A/P" },
      { k: "first", label: "First-author share", abbr: "1A" },
      { k: "cited", label: "Cited publications", abbr: "≥1 cit" }
    ],
    es: [
      { k: "pubs", label: "Publicaciones", abbr: "P" },
      { k: "cites", label: "Citas", abbr: "C" },
      { k: "h", label: "Índice h", abbr: "h" },
      { k: "cpp", label: "Citas por publicación", abbr: "C/P" },
      { k: "i10", label: "Índice i10", abbr: "i10" },
      { k: "g", label: "Índice g", abbr: "g" },
      { k: "m", label: "Índice m", abbr: "m" },
      { k: "app", label: "Autores por publicación", abbr: "A/P" },
      { k: "first", label: "Como primer autor", abbr: "1A" },
      { k: "cited", label: "Con al menos 1 cita", abbr: "≥1 cit" }
    ]
  }[LANG];

  function computeMetrics(list) {
    const n = list.length;
    if (!n) return null;
    const cs = list.map((x) => x.citations || 0).sort((a, b) => b - a);
    const cites = cs.reduce((a, b) => a + b, 0);
    let h = 0; for (let i = 0; i < cs.length; i++) { if (cs[i] >= i + 1) h = i + 1; else break; }
    const i10 = cs.filter((c) => c >= 10).length;
    let g = 0, sum = 0; for (let i = 0; i < cs.length; i++) { sum += cs[i]; if (sum >= (i + 1) * (i + 1)) g = i + 1; else break; }
    const years = list.map((x) => x.year).filter(Boolean);
    const firstYear = years.length ? Math.min.apply(null, years) : null;
    const age = firstYear ? (new Date().getFullYear() - firstYear + 1) : null;
    const m = age ? h / age : null;
    const cpp = cites / n;
    const auth = list.map((x) => x.nAuthors).filter((v) => v > 0);
    const app = auth.length ? auth.reduce((a, b) => a + b, 0) / auth.length : null;
    const wa = list.filter((x) => x.hasAuthorInfo);
    const first = wa.length ? Math.round(100 * wa.filter((x) => x.first).length / wa.length) : null;
    const cited = Math.round(100 * list.filter((x) => (x.citations || 0) >= 1).length / n);
    return { pubs: n, cites, h, i10, g, m, cpp, app, first, cited };
  }

  function fmtMetric(k, v) {
    if (v == null) return "—";
    if (k === "cpp" || k === "app") return v.toFixed(1);
    if (k === "m") return v.toFixed(2);
    if (k === "first" || k === "cited") return v + "<small>%</small>";
    return String(v);
  }

  const METRIC_DESC = {
    en: {
      pubs: "Total number of publications shown on this site.",
      cites: "Total citations received across those publications.",
      h: "h-index: h publications with at least h citations each.",
      cpp: "Average citations per publication (total citations divided by publications).",
      i10: "i10-index: number of publications with at least 10 citations.",
      g: "g-index: the largest g such that the top g publications together gather at least g² citations.",
      m: "m-index: the h-index divided by the number of years since the first publication.",
      app: "Average number of authors per publication.",
      first: "Share of publications where he appears as the first author.",
      cited: "Share of publications with at least one citation."
    },
    es: {
      pubs: "Número total de publicaciones mostradas en este sitio.",
      cites: "Total de citas recibidas por esas publicaciones.",
      h: "Índice h: h publicaciones con al menos h citas cada una.",
      cpp: "Promedio de citas por publicación (citas totales dividido entre publicaciones).",
      i10: "Índice i10: número de publicaciones con al menos 10 citas.",
      g: "Índice g: el mayor g tal que las g mejores publicaciones reúnen al menos g² citas.",
      m: "Índice m: el índice h dividido entre los años transcurridos desde la primera publicación.",
      app: "Número promedio de autores por publicación.",
      first: "Porcentaje de publicaciones donde figura como primer autor.",
      cited: "Porcentaje de publicaciones con al menos una cita."
    }
  }[LANG];

  function renderMetrics(metrics) {
    const grid = $("#stat-grid"); if (!grid) return;
    grid.innerHTML = METRICS.map((mm) => `
      <div class="stat" tabindex="0">
        <div class="stat-hd">${METRIC_ICON[mm.k] || ""}<span class="l">${esc(mm.label)} <span class="ab">(${esc(mm.abbr)})</span></span></div>
        <div class="n" id="m-${mm.k}">${metrics ? fmtMetric(mm.k, metrics[mm.k]) : "—"}</div>
        <div class="tip">${esc(METRIC_DESC[mm.k] || "")}</div>
      </div>`).join("");
    grid.querySelectorAll(".stat").forEach((s) => {
      s.addEventListener("click", () => s.classList.toggle("open"));
    });
  }

  function localMetricList(pubs) {
    return pubs.items.map((p) => ({
      year: p.year,
      citations: p.citations || 0,
      nAuthors: Array.isArray(p.authors) ? p.authors.length : 0,
      hasAuthorInfo: Array.isArray(p.authors) && p.authors.length > 0,
      first: Array.isArray(p.authors) && /parraga|párraga/i.test(p.authors[0] || "")
    }));
  }

  // OpenAlex citation/author info keyed by DOI, used to enrich the shown publication set
  function fetchOpenAlexMap() {
    const url = "https://api.openalex.org/works?filter=author.orcid:" + ORCID_ID +
      "&per-page=200&select=doi,cited_by_count,authorships&mailto=jorge.parraga@utm.edu.ec";
    return fetch(url).then((r) => { if (!r.ok) throw new Error("openalex " + r.status); return r.json(); })
      .then((data) => {
        const m = new Map();
        (data.results || []).forEach((w) => {
          const doi = (w.doi || "").replace(/^https?:\/\/doi\.org\//i, "").toLowerCase();
          if (!doi) return;
          const a = w.authorships || [];
          const fa = a.find((x) => x.author_position === "first");
          const isSelf = (au) => au && ((au.orcid || "").indexOf(ORCID_ID) >= 0 || /parraga|párraga/i.test(au.display_name || ""));
          m.set(doi, { cites: w.cited_by_count || 0, nAuthors: a.length, first: fa ? isSelf(fa.author) : false });
        });
        return m;
      });
  }

  // metric list computed strictly over the publications shown on the site (the merged ORCID list)
  function shownMetricList(shown, oaMap) {
    return shown.map((p) => {
      const doi = normDoi(p.doi);
      const oa = doi && oaMap && oaMap.get(doi);
      const localAuthors = Array.isArray(p.authors) && p.authors.length ? p.authors : null;
      return {
        year: p.year,
        citations: oa ? oa.cites : (p.citations || 0),
        nAuthors: oa ? oa.nAuthors : (localAuthors ? localAuthors.length : 0),
        hasAuthorInfo: oa ? oa.nAuthors > 0 : !!localAuthors,
        first: oa ? oa.first : (localAuthors ? /parraga|párraga/i.test(localAuthors[0] || "") : false)
      };
    });
  }

  function fillHome(profile, pubs) {
    const say = $("#say"); if (say) say.textContent = pick(profile.tagline);
    // instant fallback from the local (ORCID-seeded) list; fillPublications refines
    // the metrics over the exact set of publications shown on the site.
    renderMetrics(computeMetrics(localMetricList(pubs)));
  }
  function fillAbout(profile) {
    const bio = $("#bio"); if (bio) bio.innerHTML = md(pick(profile.bio));
  }
  function fillCV(profile) {
    const stage = $("#cv-stage"), tabsEl = $("#cv-tabs"); if (!stage || !tabsEl) return;
    // one tab per category, in order: Education, Academic experience, Awards
    const tabs = [
      { title: T.cvEdu, kind: "edu", items: profile.education || [] },
      { title: T.cvExp, kind: "exp", items: profile.experience || [] },
      { title: T.cvAwards, kind: "award", items: profile.awards || [] }
    ].filter((p) => p.items.length);
    let active = 0;
    function render() {
      tabsEl.innerHTML = tabs.map((t, i) =>
        `<button type="button" class="cv-tab${i === active ? " on" : ""}" data-i="${i}">${esc(t.title)}</button>`).join("");
      const tb = tabs[active];
      stage.innerHTML = `<div class="cv-block"><div class="rows" id="cv-rows"></div></div>`;
      rowsEl($("#cv-rows"), tb.items, tb.kind);
    }
    tabsEl.addEventListener("click", (e) => {
      const b = e.target.closest(".cv-tab"); if (!b) return;
      active = parseInt(b.dataset.i, 10); render();
    });
    render();
  }
  // Builds the news feed as one entry per publication, in the exact order the
  // publications themselves are listed (pubList, already sorted newest-first).
  // A publication with a curated post uses it; a 2024+ publication without one
  // gets a lightweight placeholder card that links to the dynamically-generated
  // post (post.html?doi=...), same rule the Publications page already follows.
  function buildNewsList(pubList, posts) {
    const byDoi = {}; (posts.items || []).forEach((p) => { if (p.doi) byDoi[normDoi(p.doi)] = p; });
    const out = [];
    pubList.forEach((p) => {
      if (isExcluded(p)) return;
      const curated = p.doi && byDoi[normDoi(p.doi)];
      if (curated) { out.push(curated); return; }
      if ((p.year || 0) < 2024 || !p.doi) return; // matches the Publications-page rule
      out.push({
        id: null,
        doi: p.doi,
        date: `${p.year}-01-01`,
        type: p.type,
        auto: true,
        topics: p.topics || [],
        title: { en: p.title, es: p.title },
        summary: { en: T.autoSummary, es: T.autoSummary }
      });
    });
    // curated posts not tied to any doi currently in pubList (e.g. software posts) go last, newest first
    const usedIds = new Set(out.map((x) => x.id).filter(Boolean));
    const usedDois = new Set(out.map((x) => x.doi && normDoi(x.doi)).filter(Boolean));
    const leftover = (posts.items || []).filter((p) => {
      const k = p.doi && normDoi(p.doi);
      return !(p.id && usedIds.has(p.id)) && !(k && usedDois.has(k));
    }).sort((a, b) => (a.date < b.date ? 1 : -1));
    return out.concat(leftover);
  }
  function fillNews(profile, pubs, posts) {
    const wrap = $("#news-list");
    const pag = $("#news-pagination"), info = $("#news-info");
    const prev = $("#news-prev"), next = $("#news-next");
    let s = buildNewsList(curatedPubsSorted(pubs), posts);
    let page = 0;
    function render() {
      const pages = Math.max(1, Math.ceil(s.length / PAGE_SIZE));
      page = Math.min(page, pages - 1);
      wrap.innerHTML = "";
      if (!s.length) { wrap.innerHTML = `<p class="loading">${T.empty}</p>`; }
      s.slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE).forEach((p) => wrap.appendChild(cardEl(p, pubs)));
      if (pag) {
        pag.style.display = s.length > PAGE_SIZE ? "flex" : "none";
        info.textContent = T.pageOf(page + 1, pages);
        prev.disabled = page === 0; next.disabled = page >= pages - 1;
        updateGoto(pag, pages, page, (i) => { page = Math.max(0, Math.min(i, pages - 1)); render(); window.scrollTo({ top: 0, behavior: "smooth" }); });
      }
    }
    if (prev) prev.addEventListener("click", () => { if (page > 0) { page--; render(); window.scrollTo({ top: 0, behavior: "smooth" }); } });
    if (next) next.addEventListener("click", () => { page++; render(); window.scrollTo({ top: 0, behavior: "smooth" }); });
    render();
    // refine with the live ORCID-ordered list once it arrives, keeping the same order rule
    fetchLivePubs(pubs).then((merged) => { s = buildNewsList(merged, posts); render(); }).catch(() => {});
  }

  function renderRelated(posts, current) {
    const box = $("#post-related"); if (!box) return;
    const topics = new Set(current.topics || []);
    const scored = posts.items
      .filter((p) => p.id !== current.id)
      .map((p) => ({ p, n: (p.topics || []).filter((t) => topics.has(t)).length }))
      .filter((x) => x.n > 0)
      .sort((a, b) => b.n - a.n || (a.p.date < b.p.date ? 1 : -1))
      .slice(0, 5);
    if (!scored.length) { const wrap = box.closest(".related"); if (wrap) wrap.style.display = "none"; return; }
    box.innerHTML = scored.map(({ p }) => {
      const doiURL = p.doi ? "https://doi.org/" + p.doi : null;
      return `<div class="rel">
        <a class="rel-main" href="${POST_PAGE}?id=${encodeURIComponent(p.id)}">
          <span class="rel-t">${esc(pick(p.title))}</span>
          <span class="rel-m">${fmtDate(p.date)}</span>
        </a>
        ${doiURL ? `<a class="rel-doi" href="${doiURL}" target="_blank" rel="noopener" title="${T.doi}: ${esc(p.doi)}">${ICON.external}<span>${T.readOriginalPaper}</span></a>` : ""}
      </div>`;
    }).join("");
  }

  function renderPost(profile, pubs, post) {
    const hero = $("#post-hero"), body = $("#article"), links = $("#post-links");
    document.title = pick(post.title) + " — " + profile.name;
    hero.innerHTML = `<h1>${esc(pick(post.title))}</h1>${postMeta(post, pubs, { showViews: true, shareUrl: location.href })}`;
    loadViewCount(post);
    let html = md(pick(post.body));
    const pub = post.doi && pubs.items.find((p) => normDoi(p.doi) === normDoi(post.doi));
    const ref = pub || post._ref;
    const doiURL = post.doi ? "https://doi.org/" + post.doi : ((post.links || [])[0] || {}).url;
    const oa = (post.links || []).some((l) => /open access|acceso abierto/i.test(l.label));
    if (ref) {
      html += `<div class="refbox">
        <span class="lab">${T.aboutPaper}</span>
        <div class="ref-cite"><em>${esc(ref.title)}</em>. ${esc(ref.venue || "")}${ref.year ? ", " + ref.year : ""}.${post.doi ? ` <a href="https://doi.org/${esc(post.doi)}" target="_blank" rel="noopener">doi:${esc(post.doi)}</a>` : ""}</div>
        ${doiURL ? `<a class="read-paper" href="${esc(doiURL)}" target="_blank" rel="noopener">${ICON.external}<span>${T.readPaper}</span>${oa ? `<span class="oa-chip">${T.openAccess}</span>` : ""}</a>` : ""}
      </div>`;
    } else if (doiURL) {
      html += `<a class="read-paper" href="${esc(doiURL)}" target="_blank" rel="noopener">${ICON.external}<span>${T.readPaper}</span>${oa ? `<span class="oa-chip">${T.openAccess}</span>` : ""}</a>`;
    }
    if (post.auto) html += `<p style="color:var(--ink-3);font-size:.9em"><em>${T.autoNote}</em></p>`;
    body.innerHTML = html;
    const extra = (post.links || []).filter((l) => l.url !== doiURL);
    if (links) links.innerHTML = extra.map((l) => `<a href="${esc(l.url)}" target="_blank" rel="noopener">${ICON.external} ${esc(l.label)}</a>`).join("");
    if (post._posts) renderRelated(post._posts, post);
    const sw = $(".nav a.lang");
    if (sw) { const base = sw.getAttribute("href").split("?")[0]; sw.href = base + location.search; }
  }

  function fillPost(profile, pubs, posts) {
    const params = new URLSearchParams(location.search);
    const id = params.get("id"), doi = params.get("doi");
    const hero = $("#post-hero"), body = $("#article");
    if (id) {
      const post = posts.items.find((p) => p.id === id);
      if (post) { post._posts = posts; return renderPost(profile, pubs, post); }
    }
    if (doi) {
      // dynamic generation from metadata
      const local = pubs.items.find((p) => normDoi(p.doi) === normDoi(doi));
      hero.innerHTML = `<div class="meta"><span class="chip paper">${T.paper}</span></div><h1>${esc(local ? local.title : "")}</h1>`;
      body.innerHTML = `<p class="loading">${T.generating}</p>`;
      crossref(doi).then((m) => {
        if (local) { m.title = local.title || m.title; if (local.authors && local.authors.length) m.authors = local.authors; if (local.venue) m.venue = local.venue; }
        m.topics = local ? local.topics : [];
        const finish = (meta) => {
          const post = buildPost(meta, doi);
          post._ref = { title: meta.title, authors: meta.authors, venue: meta.venue, year: meta.year };
          renderPost(profile, pubs, post);
        };
        if (m.abstract) { finish(m); }
        else { openAlexAbstract(doi).then((abs) => { m.abstract = abs; finish(m); }); }
      }).catch(() => {
        if (local) { const post = buildPost({ title: local.title, authors: local.authors, venue: local.venue, year: local.year, abstract: "", topics: local.topics }, doi); renderPost(profile, pubs, post); }
        else hero.innerHTML = `<h1>${T.notFound}</h1>`, body.innerHTML = "";
      });
      return;
    }
    hero.innerHTML = `<h1>${T.notFound}</h1>`;
  }

  /* ---------- boot ---------- */
  Promise.all([fetchJSON("profile"), fetchJSON("publications"), fetchJSON("posts")])
    .then(([profile, pubs, posts]) => {
      fillChrome(profile);
      if (PAGE === "home") { fillHome(profile, pubs); fillPublications(profile, pubs, posts); }
      else if (PAGE === "about") fillAbout(profile);
      else if (PAGE === "cv") fillCV(profile);
      else if (PAGE === "publications") fillPublications(profile, pubs, posts);
      else if (PAGE === "news") fillNews(profile, pubs, posts);
      else if (PAGE === "post") fillPost(profile, pubs, posts);
    })
    .catch((err) => {
      console.error(err);
      const c = $(".content");
      if (c) { const p = document.createElement("p"); p.className = "loading"; p.textContent = T.loadFail; c.prepend(p); }
    });
})();
