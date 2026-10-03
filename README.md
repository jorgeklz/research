# Sitio web de investigador, Jorge Parraga-Alava, Ph.D.

Sitio estático bilingüe (inglés en la raíz, español en `/es/`) del perfil de investigador. Sin frameworks ni build: HTML, CSS y JavaScript puro. Funciona igual en GitHub Pages, incluso en una subcarpeta como `/research/`, porque todas las rutas son relativas.

Diseño en azules, blancos y celestes, tipografía Nunito Sans con el nombre en Montserrat. Cache busting manual con la constante `VER` en `app.js` y `?v=N` en cada HTML y en `style.css`.

## Ubicación

Carpeta del proyecto, fuente de verdad: `~/Claude/Projects/WebSiteResearch/investigador-web/`. Cualquier cambio debe terminar copiado ahí.

## Páginas y navegación

El menú tiene cuatro secciones, iguales en inglés y español, más el selector de idioma:

```
Profile      index.html            es/index.html
Publications publications.html     es/publicaciones.html
Posts        news.html             es/noticias.html
Portfolio    portfolio.html        es/portafolio.html
Post         post.html             es/entrada.html   (post.html?id=... o ?doi=...)
```

Portfolio hoy muestra solo dos secciones: Toolbox (herramientas y bases de datos que usa) y Datasets. `profile.json` también trae `experience`, `education` y `awards`, pero ninguna de las tres se renderiza todavía en el sitio; quedan como datos preparados para una futura página de CV.

## Estructura de archivos

```
index.html, publications.html, news.html, portfolio.html, post.html    Páginas EN
es/                       Las mismas páginas en español
assets/style.css         Diseño
assets/app.js            Toda la lógica: fetch a ORCID/Crossref/OpenAlex, render, métricas, paginación
data/profile.json        Bio, métricas base, experiencia, educación, premios, proyectos, toolbox, datasets, enlaces
data/publications.json   Publicaciones locales: respaldo, enriquecimiento y citas semilla
data/posts.json          Posts divulgativos curados
admin.html               Panel de administración local (ver abajo)
admin_server.py          Servidor local que permite a admin.html guardar cambios en disco
scripts/update_publications.py               Pipeline automático (ORCID → Crossref → post)
.github/workflows/update-publications.yml    Ejecución semanal del pipeline
```

## Datos en vivo

- **Publicaciones**: se cargan en vivo desde la API pública de ORCID (`0000-0001-8558-9122`), se enriquecen con Crossref (autores, revista o congreso, año) y se mezclan con `publications.json` local, que aporta la versión curada y sirve de respaldo si ORCID no responde. Lista paginada.
- **Métricas del landing**: Publicaciones, Citas, índice h, Citas/pub, i10, g, m, Autores/pub, % primer autor, % con al menos una cita. Se calculan sobre el conjunto exacto que muestra el sitio, con citas por DOI de OpenAlex.
- **Vistas de cada post**: se cuentan del lado del cliente con la API pública de Abacus (`abacus.jasoncameron.dev`), con `counterapi.dev` como respaldo si Abacus falla. No hay servidor de analítica propio.

## Posts divulgativos

Cada post tiene un `type`: `paper`, `journal`, `conference` o `software`. Dos niveles de contenido:

- **Dinámico, al instante**: el enlace *Post* de cualquier publicación abre `post.html?doi=...`, armado desde los metadatos de Crossref al momento. Una publicación nueva en ORCID ya tiene su post, sin espera. Aplica solo a publicaciones de 2024 en adelante.
- **Curado**: guardado en `data/posts.json`, con 3 a 4 párrafos para lector no experto, coautores nombrados, ciudad y país en congresos, bilingüe. Este es el que aparece primero en Noticias y el que puede editarse desde el panel de administración.

## Panel de administración local

`admin.html` es un panel para editar el sitio sin tocar JSON a mano, con pestañas Posts, About, CV y Dashboard de visitas (ranking de posts más vistos, leído también de Abacus). Para que guarde de verdad en disco hace falta correrlo con `admin_server.py`, no con `python3 -m http.server`:

```
cd ~/Claude/Projects/WebSiteResearch/investigador-web
python3 admin_server.py
```

Abre `http://localhost:8000/admin.html` para editar, o `http://localhost:8000/index.html` para ver el sitio. Cada guardado hace antes un respaldo (`data/posts.json.bak`, `data/profile.json.bak`). El sitio publicado en GitHub Pages sigue siendo estático: después de guardar en local hace falta `git add -A && git commit -m "..." && git push` para que el cambio quede en línea.

## Ejecutar en local

Solo hace falta Python 3, ya viene en macOS. Dos formas:

- **Solo ver el sitio**: `python3 -m http.server 8000` desde la carpeta del proyecto.
- **Ver el sitio y poder editar desde admin.html**: `python3 admin_server.py` (ver arriba).

Abre `http://localhost:8000`. Hace falta servidor porque el sitio carga los JSON por fetch, y los navegadores bloquean esa carga con `file://`. Español directo en `http://localhost:8000/es/`.

Tras cambios de estilo o JS, sube la constante `VER` en `app.js` y el `?v=N` en los HTML y en `style.css`, y recarga con Cmd+Shift+R la primera vez.

## Automatización

Cada lunes a las 02:00 (hora de Ecuador) el workflow de GitHub Actions:

1. Consulta ORCID por la API pública.
2. Detecta DOIs que no estén en `data/publications.json`.
3. Trae de Crossref autores, revista o congreso, año y abstract.
4. Genera un post divulgativo bilingüe por publicación nueva y hace commit.

Con el secret `ANTHROPIC_API_KEY` configurado en Settings → Secrets and variables → Actions, el post sale redactado completo en inglés y español. Sin la clave, se crea un borrador estructurado con el abstract original, marcado como automático.

Se puede ejecutar el pipeline desde la pestaña Actions ("Run workflow") o en local:

```
cd ~/Claude/Projects/WebSiteResearch/investigador-web
python3 scripts/update_publications.py
```

Para que los posts salgan redactados completos en local, exporta la clave antes:

```
export ANTHROPIC_API_KEY="tu-clave"
python3 scripts/update_publications.py
```

## Editar contenido

- Bio, métricas, experiencia, educación, premios, proyectos, toolbox, datasets y enlaces: `data/profile.json`, a mano o desde las pestañas About / CV de `admin.html`.
- Publicaciones: `data/publications.json`.
- Posts: `data/posts.json`, a mano o desde la pestaña Posts de `admin.html`. Cada entrada lleva versión `en` y `es`. Para quitar la marca de generado automático, cambia `"auto": true` a `false`.

Guarda y recarga el navegador. No hay que compilar nada.

## Publicar en GitHub Pages

1. Crea un repositorio (por ejemplo `investigador-web` o `tuusuario.github.io`).
2. Sube todo el contenido de esta carpeta.
3. Settings → Pages → Source: rama `main`, carpeta `/ (root)`.
4. En uno o dos minutos el sitio queda en `https://tuusuario.github.io/investigador-web/`.

## Despliegue pendiente

Objetivo: reemplazar la versión actual en `https://jorgeklz.github.io/research/`.

- Si `research` es un repo propio: clonar, borrar el contenido viejo, copiar el contenido de `investigador-web/` a la raíz, commit y push, y en Settings → Pages usar rama main / root.
- Si es una carpeta dentro de `jorgeklz.github.io`: copiar el contenido dentro de esa subcarpeta.
- Funciona en subruta porque todas las rutas son relativas. HTTPS de Pages es compatible con ORCID, Crossref, OpenAlex y Abacus.

## Pendientes

- Decidir si `experience`, `education` y `awards` (ya en `profile.json`) se muestran en una página de CV, o se dejan sin usar.
- Revisar la bio en ambos idiomas.
- Si se quiere foto, agregar `<img>` en la sección "About" de `index.html` y `es/index.html`.
