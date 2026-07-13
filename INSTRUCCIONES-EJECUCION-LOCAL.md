# Cómo ejecutar el sitio en tu computadora

## Requisito

Solo necesitas Python 3, que ya viene instalado en macOS. Nada más: el sitio no usa frameworks ni requiere instalar paquetes.

## Pasos

1. Abre la aplicación **Terminal**.

2. Entra a la carpeta del sitio:

```
cd ~/Claude/Projects/WebSiteResearch/investigador-web
```

3. Inicia el servidor local:

```
python3 -m http.server 8000
```

4. Abre en tu navegador:

```
http://localhost:8000
```

Verás la versión en inglés. El botón **Español** (arriba a la derecha) cambia de idioma, o entra directo a `http://localhost:8000/es/`.

5. Para detener el servidor vuelve a la Terminal y presiona `Ctrl + C`.

## ¿Por qué hace falta el servidor?

Si abres `index.html` con doble clic, el navegador bloquea la carga de los archivos JSON con los datos (es una restricción de seguridad de `file://`). Con el servidor local todo funciona igual que en internet.

## Probar la actualización automática de publicaciones

El mismo script que correrá cada semana en GitHub también funciona localmente:

```
cd ~/Claude/Projects/WebSiteResearch/investigador-web
python3 scripts/update_publications.py
```

Consulta tu ORCID, detecta publicaciones que no estén en `data/publications.json`, trae los metadatos de Crossref y crea el borrador del post bilingüe en `data/posts.json`. Al recargar el navegador ya aparecen.

Si quieres que los posts salgan redactados completos (no como borrador), exporta tu clave antes de ejecutarlo:

```
export ANTHROPIC_API_KEY="tu-clave"
python3 scripts/update_publications.py
```

## Editar contenido

- Tu bio, métricas y enlaces: `data/profile.json`
- Publicaciones: `data/publications.json`
- Noticias y posts: `data/posts.json` (cada entrada con versión `en` y `es`)

Guarda el archivo y recarga el navegador. No hay que compilar nada.

## Publicar en internet

Los pasos para GitHub Pages y la configuración de la actualización semanal están en el `README.md` de esta misma carpeta.
