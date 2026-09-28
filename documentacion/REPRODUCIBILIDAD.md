# Reproducción y verificaciones

## Entorno y ejecución

Python 3.12; biblioteca estándar para selección, normalización, controles y tablas. Las figuras requieren las versiones indicadas en `requirements.txt`. `requirements-lock.txt` conserva también las dependencias transitivas del entorno utilizado, descrito en `ENTORNO_REPRODUCCION.json`. La ejecución no requiere credenciales, API, conexión a Internet ni acceso al texto íntegro de los artículos, una vez instaladas las bibliotecas.

Desde la raíz del repositorio:

```bash
python scripts/reproducir.py --sin-figuras
```

Para figuras, instale antes las dependencias en un entorno virtual y ejecute:

```bash
python -m pip install -r requirements.txt
python scripts/reproducir.py
```

El programa usa rutas relativas a su propia ubicación. Puede ejecutarse desde otra carpeta indicando la ruta a `scripts/reproducir.py`. Los CSV usan punto decimal en los valores numéricos para facilitar el análisis; el artículo utiliza la convención española.

## Orden de procesamiento

1. `normalizar_extraccion.py`: toma la instantánea v6, recalcula campos derivados y guarda la extracción canónica y su registro de cambios.
2. `validar_datos.py`: comprueba unicidad, relaciones entre tablas, balance del flujo, normalización y coincidencia con las agregaciones del manuscrito.
3. `recalcular_resultados.py`: genera JSON y tablas CSV desde las tablas canónicas.
4. `crear_figuras.py`: regenera las cinco figuras en PNG a 300 ppp y SVG, calculando la síntesis desde los datos.

`datos/auditoria/resultados_articulo_v6.json` conserva los resultados esperados del manuscrito. No se sobrescribe al ejecutar los programas. Una diferencia provoca un error y debe explicarse antes de cambiar la referencia.

El catálogo, diccionario y esquema se regeneran con `python scripts/documentar_datos.py` cuando cambia una tabla. Sus huellas corresponden a los CSV de esta versión.

## Resultados esperados

| Control | Resultado |
| --- | ---: |
| Identificados | 1.746 |
| Duplicados / cribados | 106 / 1.640 |
| Exclusiones / pendientes / incluidos | 834 / 267 / 539 |
| Principal / dirigida / ronda de kappa incluidos | 533 / 2 / 4 |
| Recursos concretos / usos / estudios con uso RQ3 | 90 / 318 / 196 |
| Estudios con datos en español | 8 |
| Con conjunto de evaluación / con métrica identificada, flujo principal | 249 / 264 |

Las tablas de año, tarea principal y evaluación son particiones de los 533 estudios principales. Familias, métricas y conjuntos de evaluación admiten varias categorías por estudio. La tabla de RQ3 usa denominadores de 90 y 318 según corresponda.

La comprobación de textos locales mediante SHA-256 solo se ejecuta si existe `evidencia_local/textos_usados_verificacion.csv`. Por eso hay una comprobación adicional en el equipo del autor. La validación de las agregaciones funciona también en una copia pública sin esos textos.

## Integridad y versiones

```bash
python scripts/verificar_integridad.py
```

`MANIFEST.sha256` identifica los archivos incluidos al preparar la versión. La reproducción de gráficos puede producir diferencias binarias entre plataformas o versiones de bibliotecas; los controles científicos comparan cifras y relaciones, no píxeles. El manifiesto no es una firma digital ni demuestra validez científica.

Tras una modificación autorizada, regenere los resultados, revise la diferencia y actualice conscientemente el manifiesto con `python scripts/verificar_integridad.py --actualizar`. No use esta opción para ocultar una diferencia no explicada.

La configuración de GitHub Actions comprueba la integridad y reproduce las tablas en cada envío o propuesta de cambio. El estado de la ejecución más reciente puede consultarse en la insignia del README o en la sección Actions de GitHub.

## Qué no se reproduce

La consulta histórica completa a OpenAlex; los llamados originales a modelos; la extracción semántica; la evaluación humana global; el coeficiente histórico de kappa; ni la maquetación del Word. El Word entregado es una copia del manuscrito v6, con sus citas y bibliografía ya registradas. Su fuente Markdown se incluye para lectura y edición, con marcadores de citas que requieren un procesador bibliográfico para generar otro documento.
