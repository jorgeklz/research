-- Contador de visitas compartido (Emergency Radar + sitio Research)
-- ------------------------------------------------------------------
-- Ejecuta este archivo en Supabase (SQL Editor → New query → Run). Se puede ejecutar
-- encima de la versión anterior (la de Emergency Radar) sin perder datos: solo agrega
-- lo que falta y reemplaza las funciones.
--
-- Cómo cuenta:
--   * Cada sitio tiene su propio conteo, separado por la columna "sitio". Las filas que
--     ya existían quedan como 'emergency-radar' y ese sitio sigue llamando a las funciones
--     sin p_sitio, así que no hay que tocar su código. Este sitio usa p_sitio = 'research'.
--   * La IP se toma del encabezado x-forwarded-for que pone Supabase, en el servidor,
--     así que el navegador no puede inventarla.
--   * No se guarda la IP: se guarda su huella SHA-256 con una sal secreta. Sirve para
--     reconocer al mismo visitante sin conservar un dato personal.
--   * Una misma IP vuelve a contar como visita nueva en un sitio solo después de 6 horas.
--     Recargar o cambiar de página no suma.
--   * País y ciudad son aproximados: llegan del navegador (servicio de geolocalización)
--     o, si faltan, del encabezado cf-ipcountry.
--
-- Las tablas no tienen políticas de acceso: con la clave pública nadie puede leerlas
-- ni escribirlas directamente. Solo se pueden ejecutar las dos funciones de abajo.

begin;

create extension if not exists pgcrypto;

create table if not exists public.visitas (
  id bigint generated always as identity primary key,
  huella text not null,
  pais_codigo text,
  ciudad text,
  creado timestamptz not null default now(),
  ultima timestamptz not null default now()
);
alter table public.visitas add column if not exists sitio text not null default 'emergency-radar';
create index if not exists visitas_sitio_huella_idx on public.visitas (sitio, huella, ultima desc);
create index if not exists visitas_sitio_creado_idx on public.visitas (sitio, creado desc);
create index if not exists visitas_sitio_ultima_idx on public.visitas (sitio, ultima desc);
alter table public.visitas enable row level security;

create table if not exists public.visitas_config (
  id int primary key default 1 check (id = 1),
  sal text not null default encode(gen_random_bytes(24), 'hex')
);
insert into public.visitas_config (id) values (1) on conflict (id) do nothing;
alter table public.visitas_config enable row level security;

-- Versiones anteriores, sin p_sitio. Se borran para que no queden dos funciones con el
-- mismo nombre y distinta firma.
drop function if exists public.registrar_visita(text, text);
drop function if exists public.resumen_visitas();

-- Resumen público de un sitio: totales y últimas visitas (sin huellas ni IP).
create or replace function public.resumen_visitas(p_sitio text default 'emergency-radar')
returns json
language sql
stable
security definer
set search_path = public, extensions
as $$
  select json_build_object(
    'total', (select count(*) from visitas where sitio = p_sitio),
    'hoy', (select count(*) from visitas where sitio = p_sitio and creado >= now() - interval '24 hours'),
    'paises', (select count(distinct pais_codigo) from visitas where sitio = p_sitio and pais_codigo is not null),
    'top', coalesce((
      select json_agg(t) from (
        select pais_codigo as codigo, count(*) as n
        from visitas where sitio = p_sitio and pais_codigo is not null
        group by pais_codigo order by n desc limit 6
      ) t), '[]'::json),
    'recientes', coalesce((
      select json_agg(r) from (
        select pais_codigo as codigo, ciudad, ultima as fecha
        from visitas where sitio = p_sitio order by ultima desc limit 8
      ) r), '[]'::json)
  );
$$;

-- Registra la visita en un sitio (si corresponde) y devuelve el resumen de ese sitio.
create or replace function public.registrar_visita(
  p_codigo text default null,
  p_ciudad text default null,
  p_sitio text default 'emergency-radar'
)
returns json
language plpgsql
volatile
security definer
-- En Supabase, pgcrypto (digest) vive en el esquema "extensions".
set search_path = public, extensions
as $$
declare
  hdrs json := coalesce(nullif(current_setting('request.headers', true), ''), '{}')::json;
  ip text := trim(split_part(coalesce(hdrs->>'x-forwarded-for', hdrs->>'x-real-ip', ''), ',', 1));
  v_sitio text := lower(trim(coalesce(p_sitio, '')));
  v_codigo text := upper(left(coalesce(nullif(trim(p_codigo), ''), hdrs->>'cf-ipcountry'), 2));
  v_ciudad text := nullif(left(trim(coalesce(p_ciudad, '')), 80), '');
  h text;
  previa record;
  nueva boolean := false;
begin
  -- Nombre de sitio corto y simple, para que nadie llene la tabla con valores raros.
  if v_sitio !~ '^[a-z0-9-]{1,40}$' then
    raise exception 'sitio no válido';
  end if;
  if ip = '' then
    return (json_build_object('nueva', false)::jsonb || resumen_visitas(v_sitio)::jsonb)::json;
  end if;
  if v_codigo !~ '^[A-Z]{2}$' or v_codigo in ('XX', 'T1') then v_codigo := null; end if;
  h := encode(digest(ip || (select sal from visitas_config where id = 1), 'sha256'), 'hex');

  select id, ultima into previa from visitas
  where sitio = v_sitio and huella = h order by ultima desc limit 1;
  if previa.id is null or previa.ultima < now() - interval '6 hours' then
    insert into visitas (sitio, huella, pais_codigo, ciudad) values (v_sitio, h, v_codigo, v_ciudad);
    nueva := true;
  else
    update visitas set ultima = now(),
      pais_codigo = coalesce(visitas.pais_codigo, v_codigo),
      ciudad = coalesce(visitas.ciudad, v_ciudad)
    where id = previa.id;
  end if;

  return (json_build_object('nueva', nueva)::jsonb || resumen_visitas(v_sitio)::jsonb)::json;
end;
$$;

revoke all on function public.registrar_visita(text, text, text) from public;
revoke all on function public.resumen_visitas(text) from public;
grant execute on function public.registrar_visita(text, text, text) to anon, authenticated;
grant execute on function public.resumen_visitas(text) to anon, authenticated;

commit;

-- Que la API de Supabase vea enseguida las firmas nuevas.
notify pgrst, 'reload schema';
