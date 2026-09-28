# Limitaciones e interpretación de la evidencia

1. **Cobertura bibliográfica.** OpenAlex es la fuente principal. No se declara una consulta directa y completa a Scopus, Web of Science, IEEE Xplore o ACM Digital Library. Las fechas, tipos y términos de búsqueda condicionan el corpus; 2026 es un año parcial.
2. **Historia de la búsqueda.** Se dispone de registros y documentación de procedencia, pero no de la respuesta original completa de la API ni de un registro independiente de la búsqueda principal. La fecha 15 de julio de 2026 se conserva como declarada en la documentación posterior.
3. **Selección automatizada.** Las decisiones y buena parte de la extracción fueron asistidas por modelos y reglas. Una cita localizada no demuestra que la interpretación sea correcta. No existe validación humana independiente global de los 539 incluidos.
4. **Texto disponible.** Solo 15 decisiones de inclusión se apoyan en fragmentos o comienzos de texto completo. Treinta y seis se basan solo en título. Los 267 pendientes no se convierten en exclusiones por contenido ni en evidencia negativa.
5. **Unidad de análisis.** El «estudio» corresponde al registro retenido. La deduplicación no garantiza eliminar todas las relaciones entre informes de un mismo trabajo.
6. **Disponibilidad del español.** Las fuentes de soporte directo tienen distinta fuerza. La presencia de español en entrenamiento o en una declaración comercial no equivale a evaluación de requisitos españoles. Una adaptación o alternativa requiere evaluación propia.
7. **Campos no informados.** La ausencia de declaración no demuestra ausencia de uso, evaluación, código o datos. El idioma del documento no identifica la lengua del conjunto evaluado.
8. **Evaluación comparativa.** Se extraen tipos de evaluación e indicadores, no resultados numéricos homogéneos para un metaanálisis. Los 282 casos de comparación declarada no son necesariamente comparaciones experimentales equivalentes.
9. **Trazabilidad del texto.** Los textos completos de terceros se conservan localmente. La copia preparada para Git contiene el índice de evidencia y citas atribuidas, lo que limita la auditoría textual directa sin consultar las fuentes originales.
10. **Reproducción computacional.** La coincidencia de sumas, identificadores y gráficos demuestra consistencia interna del paquete. No acredita exhaustividad bibliográfica, corrección semántica o validación humana.

Estas limitaciones forman parte de los resultados y deben mantenerse al reutilizar o citar el paquete. Un recuento nulo dentro del corpus no prueba inexistencia de investigación en todo el campo.
