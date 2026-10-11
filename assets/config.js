/*
 * Configuración pública del contador de visitas (ver supabase/visitas.sql).
 * Aquí van la URL del proyecto de Supabase y la clave PÚBLICA (publishable). Esa clave está
 * pensada para el navegador: con ella no se pueden leer ni escribir las tablas, solo llamar a
 * las funciones registrar_visita y resumen_visitas.
 * NUNCA pongas aquí la clave "secret" (sb_secret_...) ni la "service_role".
 * Si url o clave quedan vacías, el contador no se muestra.
 */
window.SITE_CONFIG = {
  visitas: {
    url: "https://syglkptimygybufswhmd.supabase.co",
    clave: "sb_publishable_Y8spfv16sNIBd-bVk6lE6A_wuEITxvP",
    // El proyecto lo comparte con Emergency Radar; cada sitio cuenta aparte.
    sitio: "research"
  }
};
