"""Punto de entrada único para verificar, recalcular y generar figuras."""

import argparse
import os
import subprocess
import sys
from comun import ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sin-figuras", action="store_true", help="Solo biblioteca estándar de Python."
    )
    args = parser.parse_args()
    env = os.environ.copy()
    env.setdefault("MPLCONFIGDIR", str(ROOT / ".cache/matplotlib"))
    nombres = [
        "normalizar_extraccion.py",
        "validar_datos.py",
        "recalcular_resultados.py",
    ]
    if not args.sin_figuras:
        nombres.append("crear_figuras.py")
    for nombre in nombres:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / nombre)],
            check=True,
            cwd=ROOT,
            env=env,
        )
    print("Reproducción terminada. Consulte resultados/ y figuras/.")


if __name__ == "__main__":
    main()
