# Ampliación bibliográfica v8

Fecha de cierre de esta incorporación: 28 de septiembre de 2026. Se conserva la base anterior de 539 incluidos. Se añaden once publicaciones formales con DOI editorial confirmado y versión abierta obtenida en arXiv. No se incorporan prepublicaciones sin revista o congreso confirmado. La verificación se apoya en Crossref y en la correspondencia de título y autoría, sin afirmar lectura de la versión editorial de pago.

## Recuperación y alcance

Consulta exacta de la API de arXiv:

```
(ti:"requirements engineering" OR ti:"software requirements" OR ti:"user stories" OR ti:"requirements classification" OR ti:"requirements traceability") AND submittedDate:[201501010000 TO 202609282359]
```

Orden: submittedDate descendente. Páginas de 100 registros, offsets 0, 100 y 200. La API informó 300 resultados y se recuperaron las tres páginas. La ventana se refiere al depósito; el año de inclusión se verificó con la publicación editorial. La consulta de títulos no garantiza recuperar toda la literatura elegible.

Se cotejaron coincidencias exactas de DOI y títulos con los incluidos. Los candidatos elegidos se contrastaron también con los títulos editoriales y los textos de los 1746 registros históricos. La coincidencia de título editorial identificó un estudio educativo ya excluido. Se conservó esa exclusión. El cribado detallado priorizó 15 candidatos con DOI y aparente aplicación pertinente: once incluidos, dos exclusiones por aplicación en construcción, una exclusión previa conservada y un DOI editorial sin confirmar. Los otros 263 registros sin cribar no cuentan como incluidos ni como exclusiones. Los 22 resultados ya incluidos tampoco aumentan el corpus.

Las búsquedas web exploratorias restringidas a IEEE Xplore se archivan como apoyo de descubrimiento. No fueron una consulta exhaustiva a la API de IEEE y no se contabilizan como otro flujo sistemático. Cuatro de las once incorporaciones tienen DOI de publicaciones IEEE; su texto se consultó mediante la versión abierta.

## Denominadores

- Corpus: 550 = 539 previos + 11 nuevos.
- Análisis general combinado: 544 = 533 principales históricos + 11 nuevos.
- Complementarios dirigidos: seis, conservados fuera del análisis general.
- Datos explícitos en español: ocho en el corpus, cuatro en el análisis general.
- Recursos concretos: 132 en 204 estudios, con 389 pares únicos estudio–recurso.
- Inventario bruto: 149 filas, incluidas familias sin versión y algoritmos.
- Evidencia directa del español: 39 recursos y 109 usos. Vías de adaptación, versión multilingüe o alternativa: 68 recursos y 240 usos.
- Verificación lingüística pendiente: nueve recursos y diez usos. Esto no equivale a falta de soporte.

El archivo de selección canónica contiene 1757 registros: conserva los 1746 anteriores y agrega las once inclusiones nuevas. El descubrimiento de arXiv está en un registro separado y no se suma automáticamente al embudo histórico. Se conservan 267 pendientes de información de la base anterior.

## Extracción e interpretación

Se examinaron métodos y resultados en versiones abiertas completas, de forma automatizada y focalizada. La investigación previa contó con revisión y validación del autor en selección, extracción, clasificación de recursos y resultados, además de validación por pares mediante kappa de Cohen. Las once incorporaciones de esta sesión conservan separada su revisión por el autor. Las notas interpretativas nuevas no sustituyen esa revisión. Los documentos abiertos pueden preceder a la publicación editorial; su identificador de versión se conserva por estudio. Los campos históricos no se revalidaron ni se reescribieron.

Los modelos evaluados en comparaciones se registran como usos cuando se ejecutan, pero las menciones de antecedentes se excluyen. Las variantes siguen la normalización histórica cuando tienen unidad existente. Los nombres inconsistentes `gwen2:7b`, `gemma2:7b` y `ChatGPT 4.0 / 4.o` se conservan sin inventar una identidad concreta. Los 38 codificadores de la tabla comparativa del estudio de trazabilidad legal se registran individualmente, lo que explica una parte sustancial del aumento de diversidad.

Las etiquetas de idiomas de las fichas oficiales son evidencia documental del proveedor. La falta de etiqueta española no se interpreta como incapacidad. Las alternativas multilingües de representación de oraciones se proponen por función, sin afirmar equivalencia de rendimiento. La lengua de los datos se mantiene desconocida si no se documenta explícitamente.

## Reproducción y límites

Ejecutar `python scripts/reproducir.py`. Para figuras se necesitan NumPy y Matplotlib. Con `--sin-figuras` basta la biblioteca estándar. La validación pública v8 comprueba 23 condiciones de consistencia, incluida la conservación de los 539 registros anteriores, los balances de selección y los denominadores. Once controles adicionales de hashes de textos nuevos se ejecutan solo cuando existe el archivo textual local. Se registran como no ejecutados en la copia pública, que conserva las huellas y enlaces de procedencia. Estas comprobaciones complementan la validación humana del corpus previo y no prueban exhaustividad.

Los scripts de normalización y validación v6 se conservan con sufijo `_v6_historico`; no son el procedimiento de la v8. El punto de entrada vigente es `scripts/reproducir.py`. La documentación de la base anterior está en `documentacion/historico_v6`.

## Distribución pública 1.1.0

El artículo asociado es el manuscrito v8. El repositorio público incluye las respuestas de arXiv, metadatos editoriales y fichas de recursos. Los textos completos de terceros y los registros de trabajo privados quedan en el archivo local; sus enlaces e identificadores se conservan en la auditoría de incorporaciones. Los procedimientos vigentes están en `scripts/`.
