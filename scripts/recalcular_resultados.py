"""Reproduce agregaciones de la extracción v6, sin llamadas a servicios externos."""

from collections import Counter
from comun import (
    ROOT,
    SELECCION,
    EXTRACCION,
    INVENTARIO,
    PARES,
    TIPOS_CONCRETOS,
    leer,
    lista,
    guardar_json,
    escribir_csv,
)


def calcular():
    ext = leer(EXTRACCION)
    principal = [r for r in ext if r["flujo"] in {"principal", "ampliacion_v8"}]
    usos = [r for r in leer(PARES) if r["cuenta_como_uso_rq3"] == "True"]
    recursos = [r for r in leer(INVENTARIO) if r["tipo"] in TIPOS_CONCRETOS]
    flujos = Counter(r["flujo"] for r in ext)
    familias = Counter(
        f
        for r in principal
        for f in {
            v["familia"] for v in lista(r["recursos"]) if v["rol"] != "solo_menciona"
        }
    )

    def categorias(campo):
        return dict(
            Counter(
                c
                for r in principal
                for c in {
                    v["canonico"] for v in lista(r[campo]) if v["verificada"] is True
                }
            )
        )

    def numero(campo, fila):
        return sum(v["verificada"] is True for v in lista(fila[campo]))

    return {
        "incluidos": len(ext),
        "principal": len(principal),
        "dirigida": flujos["dirigida"],
        "ronda2": flujos["ronda2_kappa"],
        "anio": dict(Counter(r["anio"] for r in principal)),
        "tarea": dict(Counter(r["tarea_principal"] for r in principal)),
        "familia": dict(familias),
        "tipo_evaluacion": dict(Counter(r["tipo_evaluacion"] for r in principal)),
        "tipo_evaluacion_cita": sum(
            r["v_cita_evaluacion"] == "True" for r in principal
        ),
        "comparacion_verificada": sum(
            r["compara_con_linea_base"] == "si" and r["v_cita_linea_base"] == "True"
            for r in principal
        ),
        "metricas": categorias("metricas"),
        "datasets": categorias("conjuntos_datos"),
        "estudios_metricas": sum(numero("metricas", r) > 0 for r in principal),
        "estudios_datasets": sum(numero("conjuntos_datos", r) > 0 for r in principal),
        "metricas_citas": sum(numero("metricas", r) for r in principal),
        "dataset_citas": sum(numero("conjuntos_datos", r) for r in principal),
        "espanol": [r["rid"] for r in ext if r["lengua_datos"] == "espanol"],
        "rq3_recursos": dict(Counter(r["estado_rq3"] for r in recursos)),
        "rq3_usos": dict(Counter(r["estado_rq3"] for r in usos)),
    }


def seleccion():
    filas = leer(SELECCION)
    estados = Counter(r["estado"] for r in filas)
    entrada = Counter(r["flujo"] for r in filas)
    return {
        "identificados": len(filas),
        "flujos": dict(entrada),
        "duplicados": estados["CE5"],
        "cribados": len(filas) - estados["CE5"],
        "incluidos": estados["INCLUIDO"],
        "no_evaluados": estados["NO_EVALUABLE"],
        "excluidos": sum(
            v
            for k, v in estados.items()
            if k not in {"CE5", "INCLUIDO", "NO_EVALUABLE"}
        ),
        "estados": dict(estados),
    }


def exportar_tablas(stats, embudo):
    salida = ROOT / "resultados/tablas"
    escribir_csv(
        salida / "seleccion.csv",
        [
            {"etapa": k, "registros": embudo[k]}
            for k in [
                "identificados",
                "duplicados",
                "cribados",
                "excluidos",
                "no_evaluados",
                "incluidos",
            ]
        ],
        ["etapa", "registros"],
    )
    for key in [
        "anio",
        "tarea",
        "familia",
        "tipo_evaluacion",
        "metricas",
        "datasets",
        "rq3_recursos",
        "rq3_usos",
    ]:
        denominador = (
            sum(stats[key].values()) if key.startswith("rq3") else stats["principal"]
        )
        filas = [
            {
                "categoria": k,
                "n": v,
                "denominador": denominador,
                "porcentaje": f"{100 * v / denominador:.4f}",
            }
            for k, v in sorted(stats[key].items())
        ]
        escribir_csv(
            salida / f"{key}.csv",
            filas,
            ["categoria", "n", "denominador", "porcentaje"],
        )
    principal = [r for r in leer(EXTRACCION) if r["flujo"] in {"principal", "ampliacion_v8"}]
    cruces = Counter(
        (f, r["tarea_principal"])
        for r in principal
        for f in {
            v["familia"] for v in lista(r["recursos"]) if v["rol"] != "solo_menciona"
        }
    )
    escribir_csv(
        salida / "familia_tarea.csv",
        [
            {"familia": f, "tarea": t, "estudios": n}
            for (f, t), n in sorted(cruces.items())
        ],
        ["familia", "tarea", "estudios"],
    )
    espanoles = [r for r in leer(EXTRACCION) if r["lengua_datos"] == "espanol"]
    escribir_csv(
        salida / "estudios_espanol.csv",
        [
            {
                k: r[k]
                for k in [
                    "rid",
                    "flujo",
                    "titulo",
                    "anio",
                    "doi",
                    "tarea_principal",
                    "cita_lengua_datos",
                ]
            }
            for r in espanoles
        ],
        [
            "rid",
            "flujo",
            "titulo",
            "anio",
            "doi",
            "tarea_principal",
            "cita_lengua_datos",
        ],
    )
    recursos = [r for r in leer(INVENTARIO) if r["tipo"] in TIPOS_CONCRETOS]
    usos = [r for r in leer(PARES) if r["cuenta_como_uso_rq3"] == "True"]
    ev_r = Counter(
        r["subtipo_evidencia_directo"]
        for r in recursos
        if r["estatus_soporte"] == "soporte directo"
    )
    ev_u = Counter(
        r["subtipo_evidencia_directo"]
        for r in usos
        if r["estatus_soporte"] == "soporte directo"
    )
    escribir_csv(
        salida / "rq3_evidencia_directa.csv",
        [{"evidencia": e, "recursos": ev_r[e], "usos": ev_u[e]} for e in sorted(ev_r)],
        ["evidencia", "recursos", "usos"],
    )


def main():
    stats, embudo = calcular(), seleccion()
    guardar_json(ROOT / "resultados/resultados.json", stats)
    guardar_json(ROOT / "resultados/seleccion.json", embudo)
    exportar_tablas(stats, embudo)
    print(
        f"Resultados recalculados: {stats['incluidos']} incluidos; {stats['principal']} principales."
    )


if __name__ == "__main__":
    main()
