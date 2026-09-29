# Guía de datos de la v8

La fuente canónica es `extraccion/estudios_incluidos.csv`, con 550 estudios. Los CSV usan UTF-8 y algunas celdas contienen listas JSON o saltos de línea. Las celdas vacías indican información ausente o no aplicable, sin equivaler automáticamente a «no» o cero.

| Carpeta | Contenido | Uso |
|---|---|---|
| `seleccion/` | 1757 registros canónicos y descubrimiento arXiv separado | Reconstruir selección y pendientes |
| `extraccion/` | 550 incluidos y once incorporaciones identificadas | Calcular resultados |
| `recursos/` | 149 unidades de inventario, incluidas categorías excluidas del denominador | Relacionar recursos y usos |
| `auditoria/` | Procedencia, identificadores, cambios y evidencias | Rastrear decisiones |
| `versiones_previas/` | Instantáneas históricas | Comparar sin mezclarlas con los datos vigentes |

## Denominadores

La selección canónica conserva 106 duplicados, 834 exclusiones y 267 registros sin información suficiente. Incluye 550 estudios. Para las distribuciones generales se seleccionan los flujos `principal` y `ampliacion_v8`, que reúnen 544 estudios. Los seis complementarios mantienen su alcance dirigido.

Los 300 registros de `descubrimiento_arxiv_v8.csv` forman un registro separado: once incorporados, 22 ya incluidos, una exclusión previa conservada, dos exclusiones por dominio, un registro con publicación sin confirmar y 263 sin cribar. No deben sumarse automáticamente a la selección canónica.

En RQ3, los tipos `modelo`, `producto` y `recurso_lexico` reúnen 132 recursos concretos. El filtro `cuenta_como_uso_rq3 == True` selecciona 389 pares únicos en 204 estudios. Las otras filas conservan menciones, familias o usos fuera de ese denominador.

## Procedencia y controles

`estado` determina la decisión canónica; `decision_final` conserva una etapa histórica. `rid` enlaza el estudio y `unidad` identifica el recurso. Los campos de los 539 estudios previos se conservaron. Los cambios de normalización anteriores están documentados en las instantáneas y auditorías históricas.

El autor confirmó la revisión y validación de selección, extracción, clasificación y resultados del corpus previo, además de validación por pares mediante kappa de Cohen. Los indicadores automáticos de localización de citas describen controles específicos dentro de ese proceso. La revisión del autor de las once incorporaciones queda registrada por separado.

Los textos completos se conservan localmente. `auditoria/incorporaciones_v8.csv` ofrece las fuentes editoriales, enlaces abiertos y huellas de los nuevos textos. Para reproducir los cálculos, utilice `scripts/reproducir.py`; los programas con sufijo `_v6_historico` no generan la v8.
