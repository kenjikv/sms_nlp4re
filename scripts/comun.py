"""Lectura uniforme de las tablas del suplemento. Solo biblioteca estándar."""

from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parent.parent
SELECCION = ROOT / "datos/seleccion/seleccion_global_cribado.csv"
EXTRACCION = ROOT / "datos/extraccion/estudios_incluidos.csv"
INVENTARIO = ROOT / "datos/recursos/inventario_RQ3_unidades_verificado.csv"
PARES = ROOT / "datos/recursos/rq3_pares_estudio_unidad.csv"
TIPOS_CONCRETOS = {"modelo", "producto", "recurso_lexico"}


def leer(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def escribir_csv(path, filas, campos):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=campos, lineterminator="\n")
        writer.writeheader()
        writer.writerows(filas)


def lista(valor):
    return json.loads(valor or "[]")


def comprobar(condicion, mensaje):
    if not condicion:
        raise ValueError(mensaje)


def guardar_json(path, objeto):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(
        json.dumps(objeto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
