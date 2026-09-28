# Guía de datos

La fuente canónica para la síntesis es `extraccion/estudios_incluidos.csv`. Los CSV se leen con UTF-8 o UTF-8 con BOM, delimitador coma y comillas dobles. Algunas celdas contienen saltos de línea o listas JSON; use un lector de CSV, no divida líneas manualmente. Los campos vacíos significan información ausente o no aplicable según el contexto, nunca automáticamente «no» o cero.

| Carpeta | Contenido | Uso |
| --- | --- | --- |
| `seleccion/` | 1.746 decisiones globales y 267 pendientes | Reconstruir el flujo y localizar exclusiones |
| `extraccion/` | 539 estudios incluidos, extracción canónica | Calcular resultados del manuscrito |
| `recursos/` | 106 entradas de inventario y 861 filas estudio–unidad | Construir RQ3 con sus filtros explícitos |
| `auditoria/` | Recuperación de textos, incidencias, cambios e índice de evidencias | Seguir procedencia y comprobar integridad |
| `versiones_previas/` | Tablas recibidas y extracción v6 antes de normalizar columnas | Comparar cambios; no mezclar con la base canónica |

## Estado final de selección

`estado` incorpora la deduplicación y las decisiones posteriores. `decision_final` es un campo heredado de una fase anterior, a pesar de su nombre. Contarlo directamente produce cifras distintas del flujo final.

| `estado` | Registros | Interpretación |
| --- | ---: | --- |
| `INCLUIDO` | 539 | Incluido en uno de los tres flujos |
| `CE5` | 106 | Duplicado o versión redundante |
| `NO_EVALUABLE` | 267 | Información insuficiente, conservado como pendiente |
| `NO-CI1` | 479 | No cumple el criterio de aplicación a requisitos con NLP/aprendizaje automático |
| `CE1` | 145 | Fuera del objeto de requisitos de software |
| `CE2` | 60 | Falta el recurso léxico-semántico requerido |
| `CE3` | 88 | Documento ajeno al tipo primario requerido |
| `CE4` | 9 | Idioma fuera del criterio declarado |
| `CE6` | 53 | Estudio secundario |

Los seis motivos de exclusión por contenido suman 834. `conservado_en_lugar` enlaza cada duplicado con otro identificador existente; conservarlo no significa que el registro de destino resulte finalmente incluido.

## RQ3: inventario frente a usos

El inventario contiene 79 modelos, cuatro productos, siete recursos léxicos, 12 familias sin versión y cuatro algoritmos. Solo los tres primeros tipos integran el denominador de 90 recursos concretos.

Los 318 usos se obtienen filtrando `cuenta_como_uso_rq3 == True`. Son pares únicos de estudio y unidad, pertenecen al flujo principal y cubren 196 estudios. Las restantes filas preservan categorías genéricas, menciones o usos que no pertenecen al denominador. Algunas categorías excluidas del recuento no tienen una entrada propia en el inventario; esto no equivale a un recurso perdido de los 90 contados.

## Normalización de métricas

La extracción v6 recibida conserva dos nombres para los contadores de métricas: el original femenino (`n_metricas_verificadas`) y el añadido masculino (`n_metricas_verificados`). Tras las correcciones de pasajes, el primero quedó desactualizado en tres registros.

`scripts/normalizar_extraccion.py` calcula los contadores desde la lista JSON `metricas`, mantiene los nombres femeninos y retira los dos alias masculinos. Se corrigen seis celdas derivadas en tres registros. La tabla recibida queda intacta en `versiones_previas/`; el registro de diferencias está en `auditoria/normalizacion_repositorio.csv`. No cambian citas, interpretación, elegibilidad ni resultados publicados en el manuscrito v6.

## Evidencia textual

El índice `auditoria/indice_evidencia_textual.csv` contiene un identificador, flujo, base textual, longitud y SHA-256 por registro. Los textos correspondientes se conservan localmente en `evidencia_local/`, excluidos de Git. Las citas breves de los campos de extracción conservan atribución mediante `rid`, título y DOI cuando están disponibles; no se conceden derechos sobre las obras citadas.
