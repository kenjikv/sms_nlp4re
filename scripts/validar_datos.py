"""Comprueba integridad, relaciones, denominadores y concordancia con el artículo v6."""

import hashlib
import json
from comun import (
    ROOT,
    SELECCION,
    EXTRACCION,
    INVENTARIO,
    PARES,
    TIPOS_CONCRETOS,
    leer,
    lista,
    comprobar,
    guardar_json,
)
from normalizar_extraccion import construir
from recalcular_resultados import calcular, seleccion


def validar():
    pruebas = []

    def exigir(condicion, descripcion):
        comprobar(condicion, descripcion)
        pruebas.append(descripcion)

    sel, ext, inv, pares = map(leer, [SELECCION, EXTRACCION, INVENTARIO, PARES])
    pendientes = leer(ROOT / "datos/seleccion/pendientes_texto_completo.csv")
    for nombre, filas, clave in [
        ("selección", sel, "rid"),
        ("extracción", ext, "rid"),
        ("inventario", inv, "unidad"),
        ("pendientes", pendientes, "rid"),
    ]:
        exigir(
            len({r[clave] for r in filas}) == len(filas),
            f"Identificador único en {nombre}",
        )
    ids_sel, ids_ext = {r["rid"] for r in sel}, {r["rid"] for r in ext}
    exigir(
        ids_ext == {r["rid"] for r in sel if r["estado"] == "INCLUIDO"},
        "Extracción = incluidos según estado definitivo",
    )
    exigir(
        {r["rid"] for r in pendientes}
        == {r["rid"] for r in sel if r["estado"] == "NO_EVALUABLE"},
        "Pendientes separados de exclusiones por contenido",
    )
    exigir(
        all((r["CE5"] == "True") == (r["estado"] == "CE5") for r in sel),
        "Duplicados coherentes con CE5",
    )
    exigir(
        all(r["conservado_en_lugar"] in ids_sel for r in sel if r["estado"] == "CE5"),
        "Duplicados enlazados a registros existentes",
    )
    exigir(
        ext == construir()[0],
        "Normalización reproduce exactamente la extracción canónica",
    )
    unidades = {r["unidad"]: r for r in inv}
    exigir(
        all(r["rid"] in ids_ext for r in pares),
        "Todos los pares vinculados a estudios incluidos",
    )
    usados = [r for r in pares if r["cuenta_como_uso_rq3"] == "True"]
    exigir(
        all(r["unidad"] in unidades for r in usados),
        "Todos los usos contados tienen unidad en el inventario",
    )
    exigir(
        len(usados) == len({(r["rid"], r["unidad"]) for r in usados}),
        "Usos únicos por estudio y unidad",
    )
    exigir(
        all(
            r["flujo"] == "principal"
            and r["tipo_unidad"] in TIPOS_CONCRETOS
            and r["rol"] != "solo_menciona"
            for r in usados
        ),
        "RQ3 cuenta recursos concretos usados en el flujo principal",
    )
    exigir(
        all(r["estado_rq3"] == unidades[r["unidad"]]["estado_rq3"] for r in usados),
        "Estados RQ3 coherentes entre inventario y usos",
    )
    exigir(
        len({r["rid"] for r in usados}) == 196,
        "RQ3 representa 196 estudios principales",
    )
    stats, embudo = calcular(), seleccion()
    referencia = json.loads(
        (ROOT / "datos/auditoria/resultados_articulo_v6.json").read_text(
            encoding="utf-8"
        )
    )
    exigir(
        stats == referencia,
        "Todas las agregaciones coinciden con los resultados del manuscrito v6",
    )
    exigir(
        embudo["identificados"] == embudo["duplicados"] + embudo["cribados"],
        "Identificados = duplicados + cribados",
    )
    exigir(
        embudo["cribados"]
        == embudo["excluidos"] + embudo["no_evaluados"] + embudo["incluidos"],
        "Balance del cribado completo",
    )
    for k in ["anio", "tarea", "tipo_evaluacion"]:
        exigir(
            sum(stats[k].values()) == stats["principal"], f"Partición completa de {k}"
        )
    exigir(
        sum(stats["rq3_recursos"].values()) == 90
        and sum(stats["rq3_usos"].values()) == 318,
        "Denominadores RQ3: 90 recursos y 318 usos",
    )
    exigir(
        len(stats["espanol"]) == 8,
        "Ocho estudios con datos en español entre los tres flujos",
    )
    for key in ["metricas", "conjuntos_datos"]:
        exigir(
            all(isinstance(v["verificada"], bool) for r in ext for v in lista(r[key])),
            f"Indicadores booleanos válidos en {key}",
        )
    indice = leer(ROOT / "datos/auditoria/indice_evidencia_textual.csv")
    exigir(
        {r["rid"] for r in indice} == ids_sel,
        "Índice de evidencia cubre todos los registros",
    )
    local = ROOT / "evidencia_local/textos_usados_verificacion.csv"
    if local.exists():
        textos = {r["rid"]: r["texto_usado"] for r in leer(local)}
        exigir(
            all(
                hashlib.sha256(textos[r["rid"]].encode("utf-8")).hexdigest()
                == r["sha256_texto"]
                for r in indice
            ),
            "Integridad de textos locales mediante SHA-256",
        )
    resultado = {
        "version_paquete": "1.0.0",
        "referencia": "manuscrito v6",
        "resultado": "correcto",
        "comprobaciones": pruebas,
        "alcance": "Integridad y consistencia computacional; no validación semántica humana.",
    }
    guardar_json(ROOT / "resultados/validacion.json", resultado)
    print(
        f"Validación correcta: {len(pruebas)} comprobaciones; resultados idénticos a v6."
    )


if __name__ == "__main__":
    validar()
