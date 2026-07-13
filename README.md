# Sitio web de investigador — Jorge Párraga Álava, Ph.D.

Sitio estático bilingüe (inglés por defecto, español en `/es/`) con diseño minimalista en azules, blancos y celestes, tipografía Avenir (con respaldo Nunito Sans) y menú superior a la derecha. Cada ítem del menú es una página independiente. Sin frameworks, sin proceso de compilación: HTML, CSS y JavaScript puro. Funciona tal cual en GitHub Pages.

El menú tiene cinco páginas: Perfil, Publicaciones, Noticias y posts, Sobre mí y CV. La página CV reúne experiencia, educación y premios, todo alimentado desde `data/profile.json`. Cada red social (Google Scholar, Scopus, Web of Science, ORCID, DBLP, GitHub) y cada acción de publicación (DOI, Cite, Open access, Post) usa un ícono lineal minimalista.

## Publicaciones en vivo y posts dinámicos

La página de Publicaciones carga tus trabajos **en vivo desde la API pública de ORCID** (igual que tu sitio actual), con paginación Prev/Sig. Para cada trabajo pide a Crossref los autores, la revista o congreso y el año, y los completa sobre la marcha. Si un DOI ya está en `data/publications.json`, usa esa versión curada (más rica); si es nuevo, lo muestra igual. Si ORCID no responde, cae a la lista local.

El post divulgativo se genera en **dos niveles**:

- **Dinámico, al instante:** el enlace *Post* de cualquier publicación abre `post.html?doi=...`, que arma un resumen bilingüe desde los metadatos de Crossref en el momento. Apenas aparece una publicación nueva en ORCID, su post ya existe, sin esperar nada.
- **Curado, semanal:** el workflow de GitHub Actions redacta y guarda el post completo en `data/posts.json` (ver más abajo), que es el que sale en Noticias.

## Estructura

```
├── index.html              Perfil / inicio (EN)
├── publications.html       Publicaciones (EN)
├── news.html               Noticias y posts (EN)
├── about.html              Sobre mí (EN)
├── cv.html                 Experiencia, educación y premios (EN)
├── post.html               Entrada individual (EN)  →  post.html?id=...
├── es/                     Las mismas páginas en español
│     index.html · publicaciones.html · noticias.html · sobre-mi.html · cv.html · entrada.html
├── assets/style.css        Diseño (paleta azul, Avenir, íconos)
├── assets/app.js           Renderizado de datos y filtros
├── data/profile.json       Tu perfil, bio, métricas y enlaces
├── data/publications.json  Publicaciones (se actualiza solo)
├── data/posts.json         Posts divulgativos y noticias (se actualiza solo)
├── scripts/update_publications.py   Pipeline automático
└── .github/workflows/update-publications.yml   Ejecución semanal
```

Todo el contenido vive en los tres JSON de `data/`. Las páginas HTML casi nunca se tocan.

## Publicar en GitHub Pages

1. Crea un repositorio en GitHub (por ejemplo `investigador-web` o `tuusuario.github.io`).
2. Sube todo el contenido de esta carpeta.
3. En el repositorio: Settings → Pages → Source: rama `main`, carpeta `/ (root)`.
4. En uno o dos minutos el sitio queda en `https://tuusuario.github.io/investigador-web/`.

## La automatización

Cada lunes a las 02:00 (hora de Ecuador) el workflow de GitHub Actions:

1. Consulta tu ORCID (`0000-0001-8558-9122`) por la API pública.
2. Detecta DOIs que no estén en `data/publications.json`.
3. Trae de Crossref los autores, la revista o congreso, el año y el abstract.
4. Genera un post divulgativo bilingüe por cada publicación nueva y hace commit.

Sobre la redacción de posts hay dos modos:

- **Con clave de Anthropic** (recomendado): agrega un secret llamado `ANTHROPIC_API_KEY` en Settings → Secrets and variables → Actions. El post se redacta completo en inglés y español, en lenguaje llano, a partir del título y el abstract. Cuesta centavos por publicación.
- **Sin clave**: se crea un borrador estructurado con el abstract original, marcado como automático, para que lo pulas a mano.

Puedes ejecutar el pipeline cuando quieras desde la pestaña Actions (botón "Run workflow") o localmente con `python3 scripts/update_publications.py`. La primera ejecución importará todo tu historial de ORCID que aún no esté en el JSON, incluidas las publicaciones anteriores a 2021.

## Editar contenido manualmente

- **Noticia de congreso o evento**: agrega un objeto en `data/posts.json` con `"type": "conference"` (o `"software"` para lanzamientos, `"news"` para lo demás). Usa la entrada de ejemplo como plantilla. Título, resumen y cuerpo siempre con versión `en` y `es`.
- **Bio, métricas, enlaces**: edita `data/profile.json`. El índice h está vacío (`null`); si agregas el valor de Scholar, aparecerá en el inicio.
- **Corregir un post automático**: edítalo en `posts.json` y cambia `"auto": true` a `false` para quitar la nota de generación automática.

## Cosas por verificar

- El enlace de ResearchGate en `profile.json` apunta a la búsqueda; reemplázalo con la URL exacta de tu perfil.
- El enlace de GitHub (`jorgeklz`) es una suposición; corrígelo si tu usuario es otro.
- Revisa la bio en ambos idiomas y ajusta lo que quieras.
- Si quieres foto, agrega `<img>` en la sección "About" de `index.html` y `es/index.html`.

## Ver el sitio localmente

Por seguridad los navegadores no cargan JSON desde `file://`. Desde esta carpeta:

```
python3 -m http.server 8000
```

y abre `http://localhost:8000`.
