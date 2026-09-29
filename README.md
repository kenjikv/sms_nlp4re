# SMS_NLP4RE

## Recursos léxico-semánticos en NLP4RE y evidencia para el español

**Publicación 1.1.1 · Manuscrito v10 · 29 de septiembre de 2026**

[![Validación de datos y resultados](https://github.com/kenjikv/sms_nlp4re/actions/workflows/validar.yml/badge.svg)](https://github.com/kenjikv/sms_nlp4re/actions/workflows/validar.yml)

El suplemento reúne los datos y procedimientos del mapeo de recursos léxico-semánticos en ingeniería de requisitos. La publicación 1.1.1 incorpora el manuscrito v10, con una redacción más breve y una discusión centrada en la ambigüedad y la dispersión interpretativa de requisitos en español. Conserva los datos publicados en 1.1.0: 550 estudios incluidos y 544 en el análisis general.

[Artículo v10](manuscrito/Mapeo_Sistematico_NLP4RE_espanol_v10.docx) · [Versión 1.1.1](https://github.com/kenjikv/sms_nlp4re/releases/tag/v1.1.1) · [Cambios editoriales](documentacion/REVISION_EDITORIAL_V10.md) · [Método y procedencia](documentacion/AMPLIACION_V8.md) · [Revisión y validación del autor](documentacion/REVISION_DEL_AUTOR_V8.md)

| Unidad | Recuento | Alcance |
|---|---:|---|
| Estudios incluidos | 550 | 539 anteriores y once nuevos |
| Análisis general | 544 | 533 principales anteriores y once nuevos |
| Estudios complementarios | 6 | Conservados fuera de la distribución general |
| Recursos concretos | 132 | Identificados en 204 estudios del análisis general |
| Pares estudio–recurso | 389 | Usos únicos, sin menciones bibliográficas |
| Estudios con datos españoles explícitos | 8 | Cuatro del análisis general y cuatro complementarios |

El autor revisó y validó la selección de artículos, la extracción de datos, la clasificación de recursos y los resultados del corpus previo. El proceso incluyó validación por pares mediante kappa de Cohen. La ronda conservada documenta 18 pares de decisiones, 17 coincidencias y κ = 0,640; ese coeficiente corresponde a su muestra, sin resumir toda la revisión del autor. La asistencia de modelos y las comprobaciones computacionales apoyaron el proceso. La revisión del autor de las once incorporaciones se registra por separado.

### Alcance de los datos publicados en 1.1.0

La consulta de arXiv recuperó 300 registros y su cribado es parcial: once incorporaciones, 22 ya incluidos, una exclusión anterior conservada, dos exclusiones por dominio, un registro con publicación sin confirmar y 263 pendientes de cribado. Los pendientes no aumentan los estudios incluidos. Tampoco se presenta esta ampliación como búsqueda exhaustiva de IEEE Xplore. Cuatro incorporaciones tienen publicación IEEE confirmada por DOI.

Nueve recursos mantienen pendiente la comprobación de su soporte del español. Parte del aumento de diversidad procede de comparar numerosos codificadores dentro de un mismo estudio, por lo que no representa automáticamente más líneas independientes de investigación.

### Datos y reproducción

- [Extracción canónica](datos/extraccion/estudios_incluidos.csv) e [incorporaciones](datos/extraccion/incorporaciones_v8.csv).
- [Registro completo de descubrimiento](datos/seleccion/descubrimiento_arxiv_v8.csv) y [selección canónica](datos/seleccion/seleccion_global_cribado.csv).
- [Inventario de recursos](datos/recursos/inventario_RQ3_unidades_verificado.csv) y [pares estudio–recurso](datos/recursos/rq3_pares_estudio_unidad.csv).
- [Procedencia editorial y textos abiertos](datos/auditoria/incorporaciones_v8.csv), con identificadores, enlaces y huellas de los textos consultados.

Con Python 3.12, `python scripts/reproducir.py --sin-figuras` verifica y recalcula los resultados usando la biblioteca estándar. Para regenerar también las figuras, instale las dependencias de `requirements.txt` y ejecute `python scripts/reproducir.py`.

La distribución pública ejecuta 23 comprobaciones de consistencia. Otros once controles de integridad textual requieren el archivo privado `evidencia_local/textos_usados_verificacion.csv` y se informan como no ejecutados cuando no está presente. Los 34 controles se ejecutaron en el entorno local que conserva esos textos. Estas comprobaciones complementan la validación del autor; no vuelven a realizar la búsqueda o la extracción semántica.

### Disponibilidad y citación

Kawaida Villegas, K. (2026). *SMS_NLP4RE: datos y materiales del mapeo sistemático de recursos léxico-semánticos en NLP4RE* (versión 1.1.1, manuscrito v10) [Conjunto de datos y programas]. GitHub. https://github.com/kenjikv/sms_nlp4re/releases/tag/v1.1.1

La [versión 1.1.0](https://github.com/kenjikv/sms_nlp4re/releases/tag/v1.1.0) conserva el manuscrito v8 y la ampliación de datos que utiliza la v10. La [versión 1.0.0](https://github.com/kenjikv/sms_nlp4re/releases/tag/v1.0.0) conserva el suplemento asociado al manuscrito v6. La documentación bajo `documentacion/historico_v6` es histórica; las aclaraciones vigentes de revisión humana están en `documentacion/REVISION_DEL_AUTOR_V8.md`. No se ha asignado un DOI al suplemento.

Los textos completos de terceros se conservan en el archivo local de investigación. El repositorio público ofrece sus enlaces y metadatos. Los programas y las aportaciones originales mantienen las condiciones descritas en [LICENSE.md](LICENSE.md). El manuscrito se publica como versión de trabajo del autor.
