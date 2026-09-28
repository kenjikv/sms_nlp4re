# Procedencia y cambios del repositorio

El paquete 1.0.0 se construyó a partir de los entregables revisados del manuscrito v6. Los originales del autor y las sucesivas tablas aportadas no se modificaron.

| Material | Procedencia | Tratamiento |
| --- | --- | --- |
| Selección, pendientes e inventario | Última entrega conciliada del autor | Copia conservada |
| Extracción anterior y extracción v6 | Paquete de revisión v6 | Instantáneas conservadas en `datos/versiones_previas/` |
| Extracción canónica | Derivada de la extracción v6 | Seis correcciones de contadores en tres registros y eliminación de dos alias de columna |
| Referencia numérica | `Resultados_v6.json` de la entrega | Copia sellada por huella digital; usada para comparar resultados |
| Figuras | Programas del paquete v6 | Rutas adaptadas, valores del flujo calculados desde CSV y SVG sin fecha variable |
| Manuscrito Word | Artículo v6 | Copia exacta con cinco figuras y 24 fuentes bibliográficas registradas |
| Manuscrito Markdown | Fuente de v6 | Solo se adaptan las rutas de imágenes a la estructura del repositorio |
| Textos de verificación | CSV aportado por el autor | Copia local excluida de Git; índice con longitud y SHA-256 por registro |
| Documentación y controles | Preparación del repositorio | Guía, diccionario, catálogo, esquema, metadatos y verificadores nuevos |

## Historial de correcciones

`datos/auditoria/Cambios_aplicados_v6.csv` documenta 12 ajustes previos del manuscrito: 11 pasajes y una clasificación de evaluación. `normalizacion_repositorio.csv` registra únicamente la consolidación posterior de campos derivados. Son etapas diferentes.

Las tablas `cambios_respecto_version_auditada.csv` e `incidencias_respuesta.csv` mantienen la procedencia de la entrega. Sus columnas de estado histórico no sustituyen a `estado` en la selección final.

Los manifiestos aportados describen el paquete de origen y pueden contener nombres de versiones o archivos que no forman parte de esta estructura. El inventario vigente es `MANIFEST.sha256`, acompañado por `documentacion/CATALOGO_DATOS.csv`.

## Autoría y automatización

La autoría consignada es Kenji Kawaida Villegas, nombre conservado en los metadatos del documento del autor. No se inventan afiliación, ORCID, coautores, DOI ni revista de publicación del conjunto de datos. Si la autoría final incluye otras personas, los metadatos de citación deberán actualizarse antes de publicar.

La organización del repositorio, la normalización, la documentación y las verificaciones se prepararon con asistencia de IA. La extracción recibida contiene además sus propios identificadores de modelo, consigna y pasada. Estas etiquetas se conservan como procedencia declarada, no como prueba de una nueva revisión humana.
