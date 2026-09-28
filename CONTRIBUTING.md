# Proponer una corrección

Las aportaciones deben mejorar la trazabilidad y conservar la relación entre datos, evidencia y resultados.

Para una corrección de datos, indique el archivo, `rid` o unidad de recurso, campo, valor actual, valor propuesto, fuente y pasaje que respalda el cambio. Explique si se trata de identidad, selección, extracción, normalización o disponibilidad lingüística. Distinga revisión humana de comprobación automática.

No edite las instantáneas de `datos/versiones_previas/`. Una nueva interpretación debe generar una nueva versión documentada, no reescribir el estado histórico. Registre la modificación en `CHANGELOG.md` y en una tabla de cambios con su motivo. Si modifica la extracción, adapte su paso de generación para evitar que se pierda al reproducir el paquete.

Ejecute los controles y regenere tablas y figuras. Si cambian resultados del manuscrito, explique las diferencias antes de actualizar la referencia numérica. Añada únicamente material cuya procedencia pueda identificarse y cuya redistribución esté permitida. Los textos íntegros de terceros y la correspondencia editorial se mantienen fuera del repositorio versionado.
