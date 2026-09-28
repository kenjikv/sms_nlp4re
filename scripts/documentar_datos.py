"""Genera catálogo y esquema observados; no inventa categorías ausentes."""

import csv
import hashlib
import json
from collections import Counter
from comun import ROOT, leer, guardar_json, escribir_csv

DESCRIPCIONES = {
    "rid": "Identificador estable del registro; clave de relación entre selección, extracción, evidencias y pares.",
    "flujo": "Procedencia: principal, dirigida o ronda2_kappa. No mezclar denominadores entre flujos.",
    "oa_id": "Identificador de OpenAlex registrado; puede estar ausente en registros complementarios.",
    "doi": "DOI conservado en la tabla, cuando consta; no se inventa si falta.",
    "anio": "Año bibliográfico registrado. 2026 tiene cobertura parcial.",
    "titulo": "Título de la publicación asociado al registro.",
    "autores": "Autoría bibliográfica de la publicación, en el formato recibido.",
    "fuente_autores": "Procedencia declarada de la autoría bibliográfica.",
    "sede": "Revista, conferencia u otra sede registrada; no acredita por sí sola revisión por pares.",
    "con_resumen": "Indicador recibido de disponibilidad de resumen.",
    "idioma_texto": "Idioma del texto bibliográfico; distinto de lengua_datos.",
    "tipo_documento": "Clasificación documental extraída.",
    "subtipo_no_estudio": "Subtipo identificado cuando el documento no corresponde a un estudio primario elegible.",
    "trata_requisitos_software": "Detección de que el objeto son requisitos de software.",
    "procesa_texto_con_pln_o_aa": "Detección de procesamiento de requisitos mediante PLN o aprendizaje automático.",
    "recursos": "Lista JSON de recursos con nombre, familia, rol y cita; la mención sola no acredita uso.",
    "recursos_verif": "Lista JSON de comprobaciones asociadas a los recursos; no representa validación humana.",
    "tarea_principal": "Categoría principal asignada al propósito del estudio; una por incluido.",
    "tareas_secundarias": "Lista JSON de tareas adicionales; no sustituye la categoría principal.",
    "tipo_contribucion": "Tipo de aportación declarado en la extracción.",
    "lengua_datos": "Lengua identificada de los datos procesados; espanol permite seleccionar el subconjunto español.",
    "aporta_espanol": "Indicador de contribución relativa al español según la extracción recibida.",
    "aporta_espanol_b": "Indicador auxiliar heredado sobre aportación al español; no sustituye lengua_datos.",
    "disponibilidad": "Declaración de disponibilidad de código o datos, no prueba de acceso efectivo.",
    "informacion_suficiente": "Evaluación asistida de suficiencia de información para decidir.",
    "estado": "Estado definitivo tras las correcciones y deduplicación; usarlo para reconstruir el flujo.",
    "decision_final": "Decisión heredada de una fase anterior. Pese al nombre, no reemplaza estado.",
    "decision_auto": "Decisión automática agregada conservada como trazabilidad.",
    "nota_decision": "Explicación asociada a la decisión recibida.",
    "CE5": "Booleano textual de duplicación o versión redundante, coherente con estado CE5.",
    "conservado_en_lugar": "rid del registro conservado en lugar del duplicado; no implica inclusión del destino.",
    "ce4_script": "Indicador auxiliar del filtro automatizado de idioma.",
    "etapa_julio": "Etapa registrada en el proceso histórico de julio; conservada para trazabilidad.",
    "escenario_824": "Etiqueta de un escenario histórico de trabajo; no se utiliza como corpus vigente.",
    "base_decision": "Texto disponible para decidir: título, título y resumen, o fragmentos/inicio del texto completo.",
    "base_texto": "Tipo de evidencia textual utilizado por el procedimiento o asociado al par.",
    "recribado": "Indicador heredado de reconsideración de elegibilidad.",
    "motivo_recribado": "Razón registrada para reconsiderar la decisión.",
    "estado_texto_completo": "Estado de recuperación de texto completo registrado.",
    "dominio_pdf": "Dominio de procedencia de la copia localizada.",
    "es_retractacion": "Indicador recibido sobre retractación o documento de retractación.",
    "identidad_documental": "Estado del contraste de identidad entre título, resumen y fuente.",
    "identidad_motivo": "Razón del resultado del contraste de identidad.",
    "citas_criticas_fallidas": "Resultado heredado de comprobaciones fallidas en citas críticas.",
    "citas_decisivas_no_localizadas": "Citas decisivas que no pudieron localizarse en la base textual disponible.",
    "cita_tarea_localizada": "Indicador de localización del pasaje sobre la tarea; no valida su interpretación.",
    "correcciones_cita": "Registro de ajustes de pasajes citados.",
    "verificacion_citas": "Detalle o estado de comprobación de citas; conservar el alcance automático declarado.",
    "flags": "Alertas del procedimiento recibido.",
    "modelo": "Identificador declarado del modelo/procedimiento; no es una verificación independiente de su identidad.",
    "consigna": "Identificador o descripción de la consigna recibida; no contiene necesariamente su texto completo.",
    "lote": "Identificador de lote de procesamiento o recuperación.",
    "estabilidad": "Concordancia o estabilidad entre pasadas automáticas, no acuerdo entre personas.",
    "pasada_elegida": "Pasada automática utilizada para la decisión conservada.",
    "reintento_citas": "Indicador o detalle de reintento de localización de citas.",
    "tipo_evaluacion": "Categoría principal del diseño de evaluación declarado.",
    "tipos_adicionales": "Tipos secundarios de evaluación conservados en la extracción.",
    "metricas": "Lista JSON de indicadores con nombre, cita, verificada y canonico. Es la fuente del recuento de métricas.",
    "metricas_canonicas": "Nombres canónicos con evidencia comprobada, separados por punto y coma.",
    "conjuntos_datos": "Lista JSON de conjuntos de evaluación con nombre, cita, verificada y canonico.",
    "conjuntos_datos_canonicos": "Nombres canónicos de conjuntos con evidencia comprobada, separados por punto y coma.",
    "n_metricas_verificadas": "Número de elementos de metricas con verificada=true. Canónico solo en estudios_incluidos.csv; puede estar desactualizado en instantáneas.",
    "n_metricas_no_verificadas": "Número de elementos de metricas sin comprobación positiva. Recalculado en la extracción canónica.",
    "n_metricas_verificados": "Alias masculino de v6, solo histórico; eliminado de la extracción canónica.",
    "n_metricas_no_verificados": "Alias masculino de v6, solo histórico; eliminado de la extracción canónica.",
    "n_conjuntos_datos_verificados": "Número de elementos de conjuntos_datos con verificada=true.",
    "n_conjuntos_datos_no_verificados": "Número de elementos de conjuntos_datos sin comprobación positiva.",
    "compara_con_linea_base": "Declaración de comparación con una referencia; no garantiza comparación experimental equivalente.",
    "eval_estabilidad": "Concordancia entre pasadas automáticas de extracción de evaluación.",
    "eval_nota": "Nota del procedimiento sobre evaluación.",
    "eval_consigna": "Identificador declarado de la consigna para extraer evaluación.",
    "eval_modelo": "Modelo/procedimiento declarado para extraer evaluación.",
    "unidad": "Nombre normalizado de la unidad de recurso o categoría.",
    "familia": "Familia de recurso asignada; un estudio puede tener varias.",
    "tipo": "Tipo de unidad en inventario o clase de incidencia, según el archivo.",
    "tipo_unidad": "Tipo de unidad asociada al par estudio–recurso.",
    "estudios": "Número de estudios asociado a la unidad según el inventario recibido.",
    "nombres": "Variantes de nombres asociadas a la unidad.",
    "nombre_en_estudio": "Nombre tal como fue extraído del estudio.",
    "indice_recurso": "Posición del recurso en la extracción de origen.",
    "rol": "Relación del recurso con el estudio; solo_menciona se excluye del uso.",
    "nivel_unidad": "Nivel de concreción: recurso concreto, familia u otra categoría registrada.",
    "primera_aparicion": "Indicador recibido de primera aparición del par para evitar duplicación.",
    "cuenta_como_uso_rq3": "True selecciona los 318 pares únicos del denominador principal de RQ3.",
    "cuenta_en_tabla_15": "Indicador de una tabla de trabajo histórica; no identifica la numeración del manuscrito v6.",
    "motivo_no_cuenta": "Razón por la que la fila no entra en el recuento RQ3.",
    "unidades_rq3": "Unidades RQ3 asociadas al estudio en la extracción.",
    "estado_rq3_unidades": "Estados lingüísticos de las unidades asociadas al estudio.",
    "estado_rq3": "Categoría final de evidencia y alternativa para español, utilizada en la síntesis RQ3.",
    "estatus_soporte": "Estado agregado de soporte documental del español.",
    "soporte_espanol": "Descripción de evidencia lingüística recibida para la unidad.",
    "tipo_evidencia_espanol": "Tipo de evidencia documental identificada sobre español.",
    "tipo_evidencia_directo": "Clase de evidencia dentro de los casos de soporte directo.",
    "subtipo_evidencia_directo": "Subtipo usado para desglosar la fuerza de la evidencia directa.",
    "clase_alternativa": "Adaptación, versión multilingüe, alternativa distinta o ausencia de alternativa identificada.",
    "transferencia": "Descripción de una posible transferencia o adaptación al español.",
    "recurso_transferencia": "Recurso identificado como adaptación, versión o alternativa.",
    "otras_transferencias": "Otras alternativas documentadas.",
    "usado_con_datos_en_espanol": "Indicador de uso documentado con datos españoles, distinto de soporte general del proveedor.",
    "soporte_espanol_criterio_conservador": "Clasificación auxiliar con criterio conservador; no sustituye estado_rq3 en la figura v6.",
    "acceso": "Modalidad de acceso documentada para el recurso.",
    "licencia": "Condiciones de licencia documentadas para el recurso, sin otorgar derechos nuevos.",
    "licencia_normalizada": "Expresión normalizada de la licencia identificada.",
    "clase_licencia": "Categoría de licencia de trabajo.",
    "alcance_licencia": "Componente o versión a los que se aplica la evidencia de licencia.",
    "version": "Versión identificada del recurso, cuando consta.",
    "version_consultada": "Versión consultada en la documentación de la unidad.",
    "version_verificada": "Versión para la que se comprobó evidencia.",
    "versiones_comparten_soporte": "Indicación recibida sobre soporte compartido entre variantes.",
    "versiones_mismo_soporte": "Comprobación adicional recibida sobre homogeneidad de soporte entre versiones.",
    "homogeneidad_versiones": "Evaluación documental de homogeneidad de variantes agrupadas.",
    "referencia_previa": "Referencia de trabajo conservada de una revisión anterior.",
    "contraste_referencia_previa": "Resultado del contraste respecto de esa referencia anterior.",
    "estado_verificacion": "Estado de verificación documental recibido; no equivale a validación humana global.",
    "modo_consulta_fuentes": "Modalidad declarada de acceso a fuentes para contrastar atributos.",
    "modo_evidencia": "Forma en que se obtuvo la evidencia: documento, fragmento indexado u otra modalidad.",
    "deteccion": "Procedencia y alcance de detección/contraste declarados por el archivo de origen.",
    "evidencia_complementaria": "Evidencia adicional sobre la unidad.",
    "fecha_consulta": "Fecha de consulta declarada de las fuentes de atributos del recurso.",
    "busqueda_texto_completo": "Detalle o estado de búsqueda de texto completo para el pendiente.",
    "motivo_pendiente": "Razón de información insuficiente; no se cuenta como exclusión por contenido.",
    "intentos_registrados": "Número o descripción de intentos de recuperación registrados.",
    "vias_probadas": "Vías de acceso o fuentes consultadas para recuperar el texto.",
    "resultados": "Resultados de los intentos de recuperación conservados.",
    "resultado_recuperacion": "Resultado final registrado de recuperación.",
    "fecha_cierre_recuperacion": "Fecha declarada de cierre de los intentos de recuperación.",
    "interpretacion": "Alcance interpretativo del estado de recuperación.",
    "destino": "Destino del registro tras el cierre de recuperación.",
    "accion_para_reabrir": "Evidencia o acción requerida para reconsiderar el pendiente.",
    "found": "Indicador recibido de que se localizó una copia o resultado.",
    "source": "Fuente/vía del intento de recuperación.",
    "oa_status": "Estado de acceso abierto registrado por la fuente consultada.",
    "pdf_url": "Dirección de la copia identificada; no garantiza disponibilidad futura.",
    "title_devuelto": "Título retornado por el servicio de recuperación.",
    "jaccard_titulo": "Medida registrada de similitud entre títulos para contrastar identidad.",
    "chars": "Longitud de texto registrada en el intento de recuperación.",
    "texto_valido": "Indicador recibido de validez del texto recuperado para el procedimiento.",
    "tried": "Vías o intentos realizados, en el formato de origen.",
    "intento": "Identificador o número de intento de recuperación.",
    "consulta_ok": "Indicador de éxito de la consulta, distinto de elegibilidad del estudio.",
    "arxiv_id": "Identificador de arXiv recuperado, cuando consta.",
    "arxiv_title": "Título asociado al resultado de arXiv.",
    "archivo_arxiv": "Nombre de archivo de trabajo declarado; el archivo no se redistribuye necesariamente.",
    "texto_usado_en_recribado": "Indicación de uso del texto recuperado en la reconsideración.",
    "campo": "Columna afectada por la corrección registrada.",
    "anterior": "Valor antes de la corrección.",
    "nuevo": "Valor después de la corrección.",
    "motivo": "Justificación documentada del cambio o estado.",
    "motivo_detalle": "Explicación detallada del motivo de selección.",
    "tipo_cambio": "Clase de cambio respecto de la versión auditada.",
    "valor_auditado": "Valor de la versión anterior auditada.",
    "valor_actual": "Valor en la entrega a la que pertenece la tabla de cambios.",
    "autor": "Responsable o procedimiento consignado en el registro de cambio/incidencia.",
    "archivo": "Archivo al que hace referencia la incidencia.",
    "fila_csv": "Número de fila registrado en el archivo de origen; no garantiza igual posición tras reordenar.",
    "detalle": "Descripción de la incidencia recibida.",
    "estado_actual_previo": "Estado registrado antes de la resolución de la incidencia.",
    "estado_incidencia": "Estado de resolución de la incidencia en la entrega.",
    "situacion_actual": "Explicación del estado de la incidencia.",
    "accion": "Acción documentada para resolver la incidencia.",
    "estado_registro": "Estado del registro según la tabla de incidencias; el estado definitivo se consulta en selección.",
    "fecha_estado": "Fecha del estado consignado en la tabla de incidencias.",
    "en_recribado": "Indicación de participación en la reconsideración.",
    "v13_fallidas": "Comprobaciones fallidas de una pasada histórica v1.3.",
    "v13_tarea_ok": "Comprobación de la tarea en la pasada histórica v1.3.",
    "grupo": "Grupo temático de la conciliación numérica histórica.",
    "medida": "Nombre de la cifra en la conciliación histórica.",
    "valor": "Valor registrado en la conciliación histórica, anterior a los ajustes v6.",
    "fichero": "Nombre del archivo en el manifiesto de origen.",
    "filas": "Número de filas declarado en el manifiesto de origen.",
    "sha256": "Huella SHA-256 del archivo en el paquete al que pertenece el manifiesto.",
    "sha256_texto": "SHA-256 del texto UTF-8 exacto usado por registro, sin normalización adicional.",
    "caracteres": "Número de caracteres Unicode del texto usado por registro.",
    "artifact_id": "Identificador de artefacto del sistema que generó la entrega original.",
    "version_id": "Identificador de versión del sistema de origen.",
    "contenido": "Descripción de contenido en el manifiesto original.",
    "papel": "Papel del archivo en el paquete original.",
}


def descripcion(nombre):
    if nombre in DESCRIPCIONES:
        return DESCRIPCIONES[nombre]
    if nombre.startswith("v_cita_") or nombre == "cita_verificada":
        return "Indicador de comprobación/localización textual del pasaje asociado; no significa validación humana de la interpretación."
    if nombre.startswith("cita_") or nombre == "cita":
        return "Pasaje de la fuente aportado como evidencia del atributo indicado; conserva los derechos de su fuente."
    if nombre.startswith("fuente_"):
        return "Referencia o dirección de la fuente que respalda el atributo indicado."
    if nombre.startswith("decision_p") or nombre.startswith("eval_pasada"):
        return "Resultado de una pasada automática conservado para trazabilidad; no corresponde a un evaluador humano."
    if nombre.startswith("nota") or nombre.startswith("observaciones"):
        return "Nota explicativa heredada sobre el atributo o la verificación indicada por el nombre del campo."
    return "Campo auxiliar heredado del paquete de origen; no interviene en las agregaciones de esta versión. Su definición operacional original no está documentada por separado."


def tipo_observado(valores):
    if not valores:
        return "sin valores"
    if set(valores) <= {"True", "False"}:
        return "booleano textual"
    if all(v.isdigit() or (v.startswith("-") and v[1:].isdigit()) for v in valores):
        return "entero textual"
    if all(v.startswith(("[", "{")) for v in valores):
        try:
            for v in valores:
                json.loads(v)
            return "JSON en celda"
        except (ValueError, TypeError):
            pass
    return "texto"


def main():
    catalogo, esquema, campos = [], {}, set()
    for path in sorted((ROOT / "datos").rglob("*.csv")):
        filas = leer(path)
        with path.open(encoding="utf-8-sig", newline="") as f:
            nombres = next(csv.reader(f))
        relativo = path.relative_to(ROOT).as_posix()
        papel = (
            "histórico; no usar como base vigente"
            if "versiones_previas" in relativo
            else "datos del paquete vigente"
        )
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        catalogo.append(
            {
                "archivo": relativo,
                "filas": len(filas),
                "columnas": len(nombres),
                "papel": papel,
                "sha256": sha,
            }
        )
        columnas = []
        for nombre in nombres:
            campos.add(nombre)
            valores = [r[nombre] for r in filas if r[nombre] != ""]
            conteos = Counter(valores)
            tipo = tipo_observado(valores)
            dato = {
                "campo": nombre,
                "descripcion": descripcion(nombre),
                "tipo_observado": tipo,
                "vacios": len(filas) - len(valores),
                "valores_distintos": len(conteos),
            }
            if len(conteos) <= 20 and all(len(v) < 160 for v in conteos):
                dato["valores_observados"] = dict(sorted(conteos.items()))
            columnas.append(dato)
        esquema[relativo] = {"filas": len(filas), "sha256": sha, "columnas": columnas}
    escribir_csv(
        ROOT / "documentacion/CATALOGO_DATOS.csv",
        catalogo,
        ["archivo", "filas", "columnas", "papel", "sha256"],
    )
    escribir_csv(
        ROOT / "documentacion/DICCIONARIO_CAMPOS.csv",
        [{"campo": n, "descripcion": descripcion(n)} for n in sorted(campos)],
        ["campo", "descripcion"],
    )
    guardar_json(
        ROOT / "documentacion/esquema_datos.json",
        {
            "alcance": "Tipos y valores observados, no un vocabulario exhaustivo del dominio.",
            "archivos": esquema,
        },
    )
    introduccion = """# Diccionario de datos

Este diccionario cubre todos los campos de los CSV del directorio `datos/`. El [esquema por archivo](esquema_datos.json) incluye tipo observado, valores vacíos y categorías cuando son pocas; el [catálogo](CATALOGO_DATOS.csv) indica filas, columnas y huellas. Los tipos son observados en esta versión, no restricciones universales para nuevas investigaciones.

## Reglas de lectura

- Una celda vacía no equivale a «no» ni a cero.
- Los booleanos del CSV suelen ser `True` y `False`; en una lista JSON son `true` y `false`.
- `estado` es la selección definitiva; `decision_final` conserva una fase previa.
- `rid` vincula registros. `unidad` vincula recursos. No todas las menciones genéricas tienen inventario de recurso concreto.
- «Verificada» significa comprobación documental automatizada según la entrega. No acredita por sí sola revisión humana.
- La extracción canónica recalcula `n_metricas_verificadas` desde `metricas`; los campos históricos quedan en sus instantáneas.

## Estructuras JSON principales

| Campo | Estructura de los elementos | Uso |
| --- | --- | --- |
| `recursos` | `nombre`, `familia`, `rol`, `cita` | Familias y atribución del uso; excluir `solo_menciona` |
| `recursos_verif` | Lista de indicadores | Comprobaciones de los recursos en la extracción recibida |
| `metricas` | `nombre`, `canonico`, `cita`, `verificada` | Contar categorías con `verificada=true`, una vez por estudio |
| `conjuntos_datos` | `nombre`, `canonico`, `cita`, `verificada` | Contar conjuntos con `verificada=true`, una vez por estudio |
| `tareas_secundarias` | Lista de categorías | Información complementaria; no sustituye la tarea principal |

Los valores `canonico` son etiquetas normalizadas de la extracción recibida, no garantizan por sí solos que una herramienta o colección citada sea un banco de evaluación formal. El recuento reproduce esas anotaciones y mantiene esta limitación.

## Campos

| Campo | Definición y alcance |
| --- | --- |
"""
    texto = (
        introduccion
        + "\n".join(f"| `{n}` | {descripcion(n)} |" for n in sorted(campos))
        + "\n"
    )
    (ROOT / "documentacion/DICCIONARIO_DATOS.md").write_text(texto, encoding="utf-8")
    print(
        f"Documentación generada: {len(catalogo)} tablas y {len(campos)} campos distintos."
    )


if __name__ == "__main__":
    main()
