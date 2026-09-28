"""Consolida contadores derivados sin modificar decisiones ni evidencia textual."""

from comun import ROOT, EXTRACCION, leer, lista, escribir_csv


def construir():
    origen = ROOT / "datos/versiones_previas/extraccion_completa_incluidos_v6.csv"
    filas = leer(origen)
    cambios = []
    for fila in filas:
        for columna, prefijo, plural in [
            ("metricas", "n_metricas", "verificadas"),
            ("conjuntos_datos", "n_conjuntos_datos", "verificados"),
        ]:
            valores = lista(fila[columna])
            derivados = {
                f"{prefijo}_{plural}": str(
                    sum(v["verificada"] is True for v in valores)
                ),
                f"{prefijo}_no_{plural}": str(
                    sum(v["verificada"] is not True for v in valores)
                ),
                (
                    "metricas_canonicas"
                    if columna == "metricas"
                    else "conjuntos_datos_canonicos"
                ): "; ".join(
                    sorted({v["canonico"] for v in valores if v["verificada"] is True})
                ),
            }
            for campo, nuevo in derivados.items():
                if fila.get(campo, "") != nuevo:
                    cambios.append(
                        {
                            "rid": fila["rid"],
                            "campo": campo,
                            "anterior": fila.get(campo, ""),
                            "nuevo": nuevo,
                            "motivo": "Recalculado desde el campo JSON; sin reinterpretar la cita.",
                        }
                    )
                fila[campo] = nuevo
        # La entrega v6 añadió estos alias masculinos y conservó contadores antiguos.
        # El repositorio utiliza exclusivamente los nombres originales femeninos.
        for alias in ["n_metricas_verificados", "n_metricas_no_verificados"]:
            fila.pop(alias, None)
    return filas, cambios


def main():
    filas, cambios = construir()
    escribir_csv(EXTRACCION, filas, list(filas[0]))
    escribir_csv(
        ROOT / "datos/auditoria/normalizacion_repositorio.csv",
        cambios,
        ["rid", "campo", "anterior", "nuevo", "motivo"],
    )
    print(
        f"Extracción normalizada: {len(filas)} estudios; {len(cambios)} ajustes de campos derivados."
    )


if __name__ == "__main__":
    main()
