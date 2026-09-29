"""Cinco figuras del manuscrito v8; datos y rutas relativos al repositorio."""

from pathlib import Path
import csv, json
from collections import Counter
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch
from recalcular_resultados import calcular, seleccion

O = Path(__file__).resolve().parent.parent
F = O / "figuras"
F.mkdir(exist_ok=True)
s = calcular()
flujo = seleccion()


def read(n):
    with (O / n).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


main = [
    r
    for r in read("datos/extraccion/estudios_incluidos.csv")
    if r["flujo"] in {"principal", "ampliacion_v8"}
]
inv = read("datos/recursos/inventario_RQ3_unidades_verificado.csv")
pairs = read("datos/recursos/rq3_pares_estudio_unidad.csv")
used = [r for r in pairs if r["cuenta_como_uso_rq3"] == "True"]
con = [r for r in inv if r["tipo"] in ["modelo", "producto", "recurso_lexico"]]
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "savefig.dpi": 300,
        "svg.fonttype": "none",
        "svg.hashsalt": "SMS_NLP4RE_v1",
    }
)
blue = "#23557b"
teal = "#2b8492"
light = "#a2cbd1"
orange = "#cf862d"
grey = "#9aa0a5"


def save(fig, n):
    fig.savefig(F / (n + ".png"), bbox_inches="tight", facecolor="white", dpi=300)
    fig.savefig(
        F / (n + ".svg"),
        bbox_inches="tight",
        facecolor="white",
        metadata={"Date": None},
    )
    plt.close(fig)


# Figure 1: historical selection and bounded complementary discovery remain separate.
fig, ax = plt.subplots(figsize=(7.2, 4.8))
ax.set(xlim=(0,10),ylim=(0,10)); ax.axis("off")
def box(x,y,w,h,txt,color="#edf3f6"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.05",facecolor=color,edgecolor=blue,lw=1))
    ax.text(x+w/2,y+h/2,txt,ha="center",va="center",fontsize=10)
def arr(a,b):
    ax.annotate("",xy=b,xytext=a,arrowprops={"arrowstyle":"->","color":blue,"lw":1.2})
box(.2,7.5,4.4,1.9,"Base previa de OpenAlex\ny vías dirigidas\n1.746 registros / 539 incluidos\n267 pendientes de información")
box(5.1,7.7,4.7,1.5,"Consulta complementaria en arXiv\n300 registros recuperados\nSolo publicaciones formales elegibles")
box(5.1,3.6,4.7,3.3,"22 ya incluidos en la base\n1 exclusión previa conservada\n2 exclusiones por dominio\n1 publicación sin confirmar\n263 pendientes de cribado\n11 incorporaciones verificadas", "#f4f1e9")
arr((7.45,7.7),(7.45,6.9));arr((2.4,7.5),(2.4,1.85));arr((7.45,3.6),(7.45,1.85))
box(.8,.4,8.4,1.45,"Corpus actualizado: 550 estudios\nAnálisis general: 533 históricos + 11 nuevos = 544\nSeis estudios de vías dirigidas se conservan por separado", "#d6e9ed")
save(fig,"Figura_1_seleccion")
# Figure 2, annual output and tasks.
years = list(range(2015, 2027))
counts = [s["anio"][str(y)] for y in years]
fig, ax = plt.subplots(figsize=(7.2, 3.65))
bars = ax.bar(years, counts, color=blue, width=0.7)
bars[-1].set_facecolor("#eeeeee")
bars[-1].set_edgecolor(blue)
bars[-1].set_hatch("///")
for b, v in zip(bars, counts):
    ax.text(b.get_x() + b.get_width() / 2, v + 3, str(v), ha="center", fontsize=10)
ax.set_xticks(years, [str(y) if y != 2026 else "2026*" for y in years], rotation=45)
ax.set(ylim=(0, 200), ylabel="Estudios incluidos", xlabel="Año registrado en la fuente")
ax.grid(axis="y", alpha=0.15)
ax.set_axisbelow(True)
fig.tight_layout()
save(fig, "Figura_2_distribucion_anual")
# Figure 3, all family/task combinations, non-exclusive.
famlabels = {
    "llm_generativo": "Modelos generativos",
    "codificador_bert": "Codificadores tipo BERT",
    "embeddings": "Vectores de palabras",
    "similitud_semantica": "Representaciones de similitud",
    "ontologia": "Ontologías",
    "transformer_otro": "Otros transformadores",
    "grafo_conocimiento": "Grafos de conocimiento",
    "marcos_roles": "Marcos y roles",
    "wordnet": "WordNet y afines",
    "otro": "Otros",
    "tesauro_glosario": "Tesauros y glosarios",
}
tasklabels = {
    "extraccion_a_modelos_u_ontologias": "Extracción a modelos",
    "clasificacion": "Clasificación",
    "generacion": "Generación",
    "ambiguedad_y_calidad": "Ambigüedad y calidad",
    "similitud_y_recuperacion": "Similitud y recuperación",
    "trazabilidad": "Trazabilidad",
    "otra": "Otras",
    "priorizacion": "Priorización",
}
fams = sorted(s["familia"], key=lambda x: -s["familia"][x])
tasks = sorted(s["tarea"], key=lambda x: -s["tarea"][x])
a = np.zeros((len(fams), len(tasks)), dtype=int)
for r in main:
    for fam in {
        x["familia"] for x in json.loads(r["recursos"]) if x["rol"] != "solo_menciona"
    }:
        a[fams.index(fam), tasks.index(r["tarea_principal"])] += 1
assert a.sum() == sum(s["familia"].values())
fig, ax = plt.subplots(figsize=(8.3, 5.8))
im = ax.imshow(a, cmap="Blues", aspect="auto", vmin=0)
for (i, j), v in np.ndenumerate(a):
    ax.text(
        j,
        i,
        str(v),
        ha="center",
        va="center",
        color="white" if v > a.max() * 0.55 else "#152b37",
        fontsize=10,
    )
ax.set_xticks(
    range(len(tasks)),
    [tasklabels[t] for t in tasks],
    rotation=40,
    ha="right",
    fontsize=10,
)
ax.set_yticks(range(len(fams)), [famlabels[f] for f in fams], fontsize=10)
ax.tick_params(length=0)
ax.set_xlabel("Tarea principal")
fig.colorbar(im, ax=ax, shrink=0.6, label="Estudios")
fig.tight_layout()
save(fig, "Figura_3_recursos_tareas")
# Figure 4, documentary criteria, not a blanket claim of validated Spanish support.
states = [
    "directo: nativo en español",
    "directo: multilingüe con el español documentado",
    "sin soporte documentado; adaptación del mismo recurso",
    "sin soporte documentado; versión multilingüe del mismo recurso",
    "sin soporte documentado; alternativa distinta",
    "soporte desconocido; alternativa distinta",
    "sin soporte documentado; sin equivalente identificado",
    "soporte desconocido; sin equivalente identificado",
    "indeterminado: depende de la versión",
    "soporte pendiente de verificación",
]
countsres = Counter(r["estado_rq3"] for r in con)
countsuse = Counter(r["estado_rq3"] for r in used)
valsres = [countsres[states[0]] + countsres[states[1]]] + [
    countsres[x] for x in states[2:]
]
valsuse = [countsuse[states[0]] + countsuse[states[1]]] + [
    countsuse[x] for x in states[2:]
]
colors = [blue, teal, "#71b8c3", "#b6dce2", "#b6dce2", orange, orange, grey, "#e4e4e4"]
hatches = ["", "", "", "", "///", "", "///", "", "xx"]
fig, (ax, bx) = plt.subplots(
    2, 1, figsize=(8.1, 6.6), gridspec_kw={"height_ratios": [1, 1.7]}
)
for y, vs, n in [(1, valsres, len(con)), (0, valsuse, len(used))]:
    left = 0
    for v, c, h in zip(vs, colors, hatches):
        w = 100 * v / n
        ax.barh(y, w, left=left, height=0.47, color=c, edgecolor="white", hatch=h)
        if w >= 5:
            ax.text(
                left + w / 2,
                y,
                str(v),
                ha="center",
                va="center",
                color="white" if c in [blue, teal] else "black",
                fontsize=11,
            )
        left += w
ax.set_yticks([1, 0], [f"Recursos ({len(con)})", f"Usos ({len(used)})"])
ax.set(xlim=(0, 100), xlabel="Porcentaje")
ax.set_title(
    "a  Evidencia y alternativas para el español", loc="left", fontweight="bold"
)
leg = [
    Patch(facecolor=blue, label="Respaldo directo del español"),
    Patch(facecolor=teal, label="Adaptación del mismo recurso"),
    Patch(facecolor="#71b8c3", label="Versión multilingüe"),
    Patch(facecolor="#b6dce2", label="Alternativa distinta"),
    Patch(facecolor=orange, label="Sin equivalente identificado"),
    Patch(facecolor=grey, label="Depende de la versión"),
    Patch(facecolor="#e4e4e4",hatch="xx",label="Verificación pendiente"),
]
ax.legend(
    handles=leg,
    loc="upper left",
    bbox_to_anchor=(-0.01, -0.43),
    ncol=2,
    fontsize=9.3,
    frameon=False,
)
labels = [
    "Recurso nativo del español",
    "Declaración del proveedor",
    "Resultado propio del español",
    "Evaluación agregada con español",
    "Solo evaluación de seguridad",
    "Español en el entrenamiento",
]
evs = [
    "nativo",
    "declaración de soporte del proveedor",
    "evaluación con resultado propio del español",
    "evaluación agregada que incluye el español",
    "solo evaluación de seguridad en español",
    "presencia en los datos de entrenamiento",
]
ec = Counter(
    r["subtipo_evidencia_directo"]
    for r in con
    if r["estatus_soporte"] == "soporte directo"
)
eu = Counter(
    r["subtipo_evidencia_directo"]
    for r in used
    if r["estatus_soporte"] == "soporte directo"
)
y = np.arange(6)
vals = [ec[x] for x in evs]
bx.hlines(y, 0, vals, color=blue, lw=2)
bx.scatter(vals, y, color=blue, s=45)
for i, k in enumerate(evs):
    bx.text(ec[k] + 0.45, i, f"{ec[k]} ({eu[k]} usos)", va="center", fontsize=10)
bx.set_yticks(y, labels, fontsize=10)
bx.invert_yaxis()
bx.set_xlim(0, 23)
bx.set_xticks([0, 5, 10, 15, 20])
bx.set_xlabel("Recursos (n = 39)")
bx.set_title(
    "b  Fuerza y alcance de la evidencia directa", loc="left", fontweight="bold", pad=13
)
fig.subplots_adjust(hspace=1.55, left=0.36, right=0.97, top=0.95, bottom=0.1)
save(fig, "Figura_4_disponibilidad_espanol")
# Figure 5, partial coverage, separate denominators explicit.
span = Counter(
    r["tarea_principal"]
    for r in read("datos/extraccion/estudios_incluidos.csv")
    if r["lengua_datos"] == "espanol"
)
fig, (ax, bx) = plt.subplots(
    1, 2, figsize=(8, 4.3), sharey=True, gridspec_kw={"width_ratios": [2.3, 1]}
)
y = np.arange(len(tasks))
ax.barh(y, [s["tarea"][t] for t in tasks], color=blue)
bx.barh(y, [span[t] for t in tasks], color=teal)
for i, t in enumerate(tasks):
    ax.text(s["tarea"][t] + 2, i, str(s["tarea"][t]), va="center", fontsize=10)
    bx.text(span[t] + 0.08, i, str(span[t]), va="center", fontsize=10)
ax.set_yticks(y, [tasklabels[t] for t in tasks])
ax.invert_yaxis()
ax.set_xlim(0, 180)
bx.set_xlim(0, 5)
ax.set_title("General ampliado (n = 544)", fontsize=11)
bx.set_title("Datos en español (n = 8)", fontsize=11)
ax.set_xlabel("Estudios")
bx.set_xlabel("Estudios")
bx.tick_params(left=False)
fig.tight_layout()
save(fig, "Figura_5_tareas_espanol")
print("Cinco figuras PNG y SVG creadas.")
