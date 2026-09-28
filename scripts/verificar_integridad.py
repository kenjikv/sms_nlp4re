"""Verifica el manifiesto o lo actualiza explícitamente tras una revisión."""

import argparse
import hashlib
from pathlib import Path
from comun import ROOT, comprobar

OMITIR = {".git", ".venv", "venv", "__pycache__", ".cache", "evidencia_local"}


def archivos():
    for path in sorted(ROOT.rglob("*")):
        relativo = path.relative_to(ROOT)
        if (
            path.is_file()
            and not (set(relativo.parts) & OMITIR)
            and path.name not in {"MANIFEST.sha256", ".DS_Store", "validacion.json"}
        ):
            yield path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actualizar", action="store_true")
    args = parser.parse_args()
    manifiesto = ROOT / "MANIFEST.sha256"
    if args.actualizar:
        texto = "".join(
            f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}\n"
            for p in archivos()
        )
        manifiesto.write_text(texto, encoding="utf-8")
        print(f"Manifiesto actualizado: {len(texto.splitlines())} archivos.")
        return
    entradas = [
        linea.split("  ", 1)
        for linea in manifiesto.read_text(encoding="utf-8").splitlines()
    ]
    esperados = {nombre for _, nombre in entradas}
    existentes = {p.relative_to(ROOT).as_posix() for p in archivos()}
    comprobar(
        esperados == existentes,
        f"Inventario diferente: faltantes={esperados - existentes}, adicionales={existentes - esperados}",
    )
    for sha, nombre in entradas:
        comprobar(
            hashlib.sha256((ROOT / nombre).read_bytes()).hexdigest() == sha,
            f"Integridad diferente: {nombre}",
        )
    print(f"Integridad correcta: {len(entradas)} archivos.")


if __name__ == "__main__":
    main()
