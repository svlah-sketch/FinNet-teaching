"""
make_intro_notebook.py
-----------------------
Generates the introductory context notebook (00_uvod_i_metodologija.ipynb).
Run from the FinNet-teaching root: python make_intro_notebook.py
"""
import json
from pathlib import Path

OUT = Path("notebooks")
OUT.mkdir(parents=True, exist_ok=True)


def nb(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.0"},
        },
        "cells": cells,
    }


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "source": text.splitlines(keepends=True),
            "outputs": [], "execution_count": None}


COLAB_CELL = code(
    '# Postavljanje okolisa (automatski detektira Google Colab)\n'
    'import sys\n'
    'if "google.colab" in sys.modules:\n'
    '    import subprocess, os\n'
    '    subprocess.run(["git", "clone",\n'
    '                    "https://github.com/svlah-sketch/FinNet-teaching.git",\n'
    '                    "/content/FinNet-teaching"], check=True)\n'
    '    os.chdir("/content/FinNet-teaching/notebooks")\n'
    '    print("Colab: repozitorij kloniran.")\n'
    'else:\n'
    '    print("Lokalno pokretanje - nema potrebe za klonom.")'
)

cells = [

md("""# 00 - Uvod i metodologija: Financijske mreže na tržištu kapitala

Ovaj notebook daje metodološki kontekst za notebookove 01–03 i studentske projekte.
Čitajte ga jednom, na početku - ne sadrži zadatke za rješavanje.

**Autor materijala:** Silvija Vlah Jerić, Ekonomski fakultet Zagreb
**Tržište:** Zagrebačka burza (ZSE), indeks CROBEX, 2004–2026
**Napomena:** Materijal je izveden iz tekućeg istraživačkog projekta čiji rezultati
još nisu objavljeni - prikazana je isključivo metodologija i ilustrativni primjeri.
"""),

COLAB_CELL,

md("""## 1. Zašto mrežna analiza financijskih tržišta?

Klasični modeli (Markowitz, CAPM) sažimaju odnose između dionica u jednu
korelacijsku matricu. Mrežna analiza ide korak dalje: **struktura** te matrice -
tko je s kim povezan i koliko jako - nosi vlastitu informaciju o stanju tržišta.

| Pitanje | Mrežna mjera |
|---------|-------------|
| Koliko je tržište integrirano? | Veličina najveće komponente (LCC) |
| Koliko brzo se šire šokovi? | Prosječna duljina puta |
| Postoje li izolirane grupe dionica? | Broj zajednica, modularnost |
| Koje su dionice "hub" sistemskog rizika? | Eigenvector centralnost |
| Koliko je rizik koncentiran? | Apsorcijski omjer |

**Ključna literatura:**
- Mantegna, R.N. (1999). Hierarchical structure in financial markets. *European Physical Journal B*, 11.
- Billio, M. et al. (2012). Econometric measures of connectedness and systemic risk. *Journal of Financial Economics*, 104(3).
"""),

md("""## 2. Metodološki pipeline: od povrata do mreže

Ovo je **ključna sekcija** - razumijte ovaj pipeline prije nego krenete na notebookove.

### Korak 1: Dnevni log-povrati

$$r_{it} = \\log\\left(\\frac{P_{it}}{P_{i,t-1}}\\right)$$

### Korak 2: EW-LOO tržišni faktor

Za svaku dionicu $i$ posebno, tržišni faktor je jednako-ponderirani prosjek
svih **ostalih** dionica (leave-one-out):

$$m_{it} = \\frac{1}{N-1} \\sum_{j \\neq i} r_{jt}$$

Zašto ne standardni indeks? Na malom tržištu dionica $i$ čini dio indeksa, što uvodi
pristranost u regresiju. EW-LOO to eliminira.

### Korak 3: OLS regresija ->> reziduali

Za svaku dionicu $i$ unutar vremenskog prozora:

$$r_{it} = \\alpha_i + \\beta_i \\cdot m_{it} + \\varepsilon_{it}$$

Rezidual $\\varepsilon_{it}$ je **idiosinkratska** komponenta - ono što dionica radi
*iznad ili ispod* zajedničkog tržišnog kretanja. Zajednički faktor je uklonjen.

### Korak 4: Parcijalna korelacija između para $(i, j)$

$$\\rho_{ij}^{\\text{parc}} = \\text{corr}(\\varepsilon_{it},\\, \\varepsilon_{jt})$$

Ovo je **parcijalna** korelacija uz kontrolu za tržišni faktor - mjeri isključivo
idiosinkratsku vezu između dviju dionica.

> **Važno:** parcijalna korelacija ≠ sirova korelacija.
> Sirova: $\\text{corr}(r_{it}, r_{jt})$ - sadrži i zajednički tržišni signal.
> Parcijalna: $\\text{corr}(\\varepsilon_{it}, \\varepsilon_{jt})$ - samo idiosinkratski dio.

### Korak 5: P-prag filtriranje ->> PG i NG podmreže

Za svaki par $(i, j)$ testiramo $H_0: \\rho_{ij}^{\\text{parc}} = 0$.
Brid postoji samo ako je parcijalna korelacija **statistički značajno** ≠ 0:

$$p_{ij} < \\alpha \\quad (\\text{npr. } \\alpha = 0.05)$$

Mreža se dijeli prema predznaku parcijalne korelacije:
- **PG (Positive Graph):** $\\rho_{ij}^{\\text{parc}} > 0$ ->> dionice se idiosinkratski kreću **zajedno**
- **NG (Negative Graph):** $\\rho_{ij}^{\\text{parc}} < 0$ ->> dionice se idiosinkratski kreću **suprotno**

> **Ključno razlikovanje:**
> - Negativna parcijalna korelacija **ne znači** da dionice padaju zajedno.
>   (Zajedničko padanje = zajednički faktor = *pozitivna* sirova korelacija.)
> - Negativna parcijalna korelacija znači: kada dionica $i$ nadmašuje tržište
>   (pozitivan rezidual), dionica $j$ ga podmašuje (negativan rezidual), i obrnuto.
>   To su **relativno suprotna kretanja** u idiosinkratskim komponentama.
"""),

md("""## 3. Podaci: CROBEX i Zagrebačka burza

| Karakteristika | Detalj |
|---------------|--------|
| Tip tržišta | Granično (frontier) |
| Dionice u uzorku | 78 (sve ikad bile u CROBEX, 2004–2026) |
| Frekvencija | Dnevno, CT model trgovanja |
| Valuta | HRK do 31.12.2022.; EUR od 1.1.2023. (fiksni tečaj 7,53450) |
| Prozora (W90) | ≈ 59 nepreklapajućih |
| Rev. prozora | 43 (revizije 10–52) |

### Krizni periodi

| Kriza | Početak | Kraj |
|-------|---------|------|
| GFC | 1.10.2007. | 30.9.2009. |
| EU dug | 1.4.2011. | 30.9.2012. |
| COVID | 20.2.2020. | 31.3.2021. |
"""),

md("""## 4. Deset mrežnih mjera

| ID | Naziv | Opis | Mreža | Prag |
|----|-------|------|-------|------|
| M1 | LCC frakcija | Udio dionica u najvećoj komponenti | NG | 0.05 |
| M2 | Avg path length | Prosj. duljina najkraćeg puta | NG | 0.05 |
| M3 | Mean degree | Prosj. broj bridova po čvoru | NG | 0.05 |
| M4 | # zajednica | Broj Louvain zajednica | NG | 0.001* |
| M5 | Modularnost | Snaga klaster strukture | NG | 0.001* |
| M6 | Apsorcijski omjer | Sistemski rizik (spektralni) | Svi | - |
| M7 | Mean closeness | Prosj. centralnost blizine | NG | 0.10 |
| M8 | Mean eigenvector | Prosj. eigenvector centralnost | NG | 0.001* |
| M9 | Max eigenvector | Maks. eigenvector centralnost | PG | 0.10 |
| M10 | Avg parcijalna kor. | Prosj. parcijalna korelacija po svim parovima | - | - |

*M4, M5, M8 dostupne samo kada je NG-0.001 mreža neprazna (≈ 30–40% prozora).

**M10:** jedina mjera koja ne dolazi iz mreže nego direktno iz matrice parcijalnih
korelacija - prosječna vrijednost $\\rho_{ij}^{\\text{parc}}$ po svim parovima.
"""),

md("""## 5. Ilustrativni primjer: sirove vs. parcijalne korelacije

Koristimo **sintetičke** podatke (ne stvarne cijene dionica) da ilustriramo pipeline.

Dva scenarija:
- **Mirno tržište**: umjeren zajednički faktor, slabija sektorska divergencija
- **Krizni scenarij**: jak zajednički pad + amplificirana sektorska divergencija

Za svaki scenarij prikazujemo:
1. Sirovu korelacijsku matricu - $\\text{corr}(r_{it}, r_{jt})$
2. Parcijalnu korelacijsku matricu - $\\text{corr}(\\varepsilon_{it}, \\varepsilon_{jt})$
3. Rezultirajuće PG i NG mreže
"""),

code("""import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from scipy import stats
from numpy.linalg import lstsq
from matplotlib.patches import Patch

np.random.seed(42)

# ── Parametri ─────────────────────────────────────────────────────────────────
N_STOCKS = 12
N_DAYS   = 90
LABELS   = [f"A{i}" for i in range(1,5)] + [f"B{i}" for i in range(1,5)] + [f"C{i}" for i in range(1,5)]
SECTORS  = [0]*4 + [1]*4 + [2]*4

NODE_COLORS = {"A": "#d62728", "B": "#1f77b4", "C": "#2ca02c"}
ALPHA = 0.10

# ── Simulacija ────────────────────────────────────────────────────────────────
def simulate(market_std, idio_std, sector_extra=None):
    market = np.random.randn(N_DAYS) * market_std
    sector_f = np.random.randn(N_DAYS, 3) * 0.3
    if sector_extra:
        for s, v in sector_extra.items():
            sector_f[:, s] += v
    idio = np.random.randn(N_DAYS, N_STOCKS) * idio_std
    R = np.zeros((N_DAYS, N_STOCKS))
    for i in range(N_STOCKS):
        R[:, i] = 0.5*market + 0.4*sector_f[:, SECTORS[i]] + idio[:, i]
    return R

R_norm = simulate(market_std=0.5, idio_std=0.8)

# Kriza: jak zajednički pad + divergencija: sektor A "osjetljiv", C "otporan"
R_cris = simulate(
    market_std=1.5, idio_std=1.2,
    sector_extra={
        0: np.random.randn(N_DAYS) * (-1.0),   # sektor A: pada više od prosjeka
        2: np.random.randn(N_DAYS) *   0.7,    # sektor C: pada manje od prosjeka
    }
)

# ── EW-LOO i reziduali ────────────────────────────────────────────────────────
def ew_loo(R):
    return (R.sum(axis=1, keepdims=True) - R) / (R.shape[1] - 1)

def residuals(R, M):
    E = np.zeros_like(R)
    for i in range(R.shape[1]):
        X = np.column_stack([np.ones(N_DAYS), M[:, i]])
        coef, *_ = lstsq(X, R[:, i], rcond=None)
        E[:, i] = R[:, i] - X @ coef
    return E

def corr_matrix(X):
    n, k = X.shape
    rho, pval = np.zeros((k,k)), np.ones((k,k))
    for i in range(k):
        for j in range(i+1, k):
            r, p = stats.pearsonr(X[:, i], X[:, j])
            rho[i,j]=rho[j,i]=r; pval[i,j]=pval[j,i]=p
    return rho, pval

E_norm = residuals(R_norm, ew_loo(R_norm))
E_cris = residuals(R_cris, ew_loo(R_cris))

rho_raw_n, p_raw_n = corr_matrix(R_norm)
rho_raw_c, p_raw_c = corr_matrix(R_cris)
rho_par_n, p_par_n = corr_matrix(E_norm)
rho_par_c, p_par_c = corr_matrix(E_cris)

print("Prosječna korelacija (gornji trokut):")
idx = np.triu_indices(N_STOCKS, k=1)
print(f"  Sirova:     mirno={rho_raw_n[idx].mean():+.3f}  kriza={rho_raw_c[idx].mean():+.3f}")
print(f"  Parcijalna: mirno={rho_par_n[idx].mean():+.3f}  kriza={rho_par_c[idx].mean():+.3f}")"""),

code("""# ── Slika 1: 4 korelacijske matrice ──────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(13, 10))
data = [
    ("Mirno - SIROVA\ncorr(r_it, r_jt)", rho_raw_n),
    ("Kriza - SIROVA\ncorr(r_it, r_jt)", rho_raw_c),
    ("Mirno - PARCIJALNA\ncorr(ε_it, ε_jt)", rho_par_n),
    ("Kriza - PARCIJALNA\ncorr(ε_it, ε_jt)", rho_par_c),
]
for ax, (title, rho) in zip(axes.flat, data):
    im = ax.imshow(rho, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(N_STOCKS)); ax.set_xticklabels(LABELS, rotation=45, fontsize=7)
    ax.set_yticks(range(N_STOCKS)); ax.set_yticklabels(LABELS, fontsize=7)
    for pos in [3.5, 7.5]:
        ax.axhline(pos, color="k", lw=1.5); ax.axvline(pos, color="k", lw=1.5)
    ax.set_title(title, fontsize=10)
    plt.colorbar(im, ax=ax, shrink=0.8)

fig.suptitle(
    "Sirova vs. parcijalna korelacija - mirno vs. krizno tržište\n"
    "(sintetički podaci: A=osjetljivi, B=neutralni, C=otporni sektor)",
    fontsize=11)
plt.tight_layout()
plt.savefig("nb00_korelacije.png", dpi=120, bbox_inches="tight")
plt.show()

print("""
Što vidimo:
  Gornji red (SIROVA):
    Mirno: pozitivne korelacije, vidljiva blok-struktura po sektorima
    Kriza: sve korelacije RASTU - sve dionice padaju zajedno ->> pozitivna sirova korelacija!
           Crvene (pozitivne) prevladavaju, NG bi bio gotovo prazan.

  Donji red (PARCIJALNA - reziduali nakon uklanjanja EW-LOO):
    Mirno: slabije, bliže nuli
    Kriza: pojavljuju se NEGATIVNE parcijalne korelacije između A i C sektora
           ->> A pada VIŠE nego što tržišni faktor predviđa (negativan rezidual)
           ->> C pada MANJE (pozitivan rezidual)
           ->> njihovi reziduali su negativno korelirani ->> brid u NG mreži
""")"""),

code("""# ── Slika 2: PG i NG mreže ───────────────────────────────────────────────────
def build_graphs(rho, pval):
    G_PG, G_NG = nx.Graph(), nx.Graph()
    G_PG.add_nodes_from(LABELS); G_NG.add_nodes_from(LABELS)
    for i in range(N_STOCKS):
        for j in range(i+1, N_STOCKS):
            if pval[i,j] < ALPHA:
                (G_PG if rho[i,j] > 0 else G_NG).add_edge(
                    LABELS[i], LABELS[j], weight=abs(rho[i,j]))
    return G_PG, G_NG

def draw_g(ax, G, title):
    colors = [NODE_COLORS[l[0]] for l in LABELS]
    pos = nx.spring_layout(G, seed=42, weight="weight") if G.number_of_edges() else nx.circular_layout(G)
    widths = [G[u][v]["weight"]*4 for u,v in G.edges()] if G.number_of_edges() else []
    nx.draw_networkx(G, pos=pos, ax=ax, node_color=colors, node_size=500,
                     font_size=8, font_color="white", edge_color="gray",
                     width=widths if widths else 1, with_labels=True)
    n_edges = G.number_of_edges()
    lcc = max((len(c) for c in nx.connected_components(G)), default=1) if n_edges else 1
    ax.set_title(f"{title}\n{n_edges} bridova | LCC={lcc}/{N_STOCKS}", fontsize=9)
    ax.axis("off")

PG_n, NG_n = build_graphs(rho_par_n, p_par_n)
PG_c, NG_c = build_graphs(rho_par_c, p_par_c)

fig, axes = plt.subplots(2, 2, figsize=(13, 10))
draw_g(axes[0,0], PG_n, f"PG mirno (α={ALPHA})")
draw_g(axes[0,1], PG_c, f"PG kriza (α={ALPHA})")
draw_g(axes[1,0], NG_n, f"NG mirno (α={ALPHA})")
draw_g(axes[1,1], NG_c, f"NG kriza (α={ALPHA})")

legend = [Patch(color=c, label=f"Sektor {s}") for s,c in NODE_COLORS.items()]
fig.legend(handles=legend, loc="lower center", ncol=3, fontsize=10, frameon=False)
fig.suptitle(
    f"PG i NG mreže od PARCIJALNIH korelacija (α={ALPHA})\n"
    "Mirno vs. krizno tržište - sintetički podaci", fontsize=12)
plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig("nb00_mreze.png", dpi=120, bbox_inches="tight")
plt.show()

print(f"""
NG mirno:  {NG_n.number_of_edges()} bridova  (malo ili ništa - nema divergencije)
NG kriza:  {NG_c.number_of_edges()} bridova  (bridovi između A i C - sektorska divergencija)

Zaključak: NG se puni u krizi jer amplificirana sektorska divergencija stvara
značajne negativne PARCIJALNE korelacije - ne zbog apsolutnog smjera kretanja,
nego zbog relativnih razlika u idiosinkratskim komponentama.
""")"""),

md("""## 6. Sažetak: sirove vs. parcijalne, i što NG zapravo znači

| | Sirova korelacija | Parcijalna korelacija |
|--|---|---|
| **Formula** | corr(r_it, r_jt) | corr(ε_it, ε_jt) |
| **Što sadrži** | Zajednički faktor + idiosinkratiku | Samo idiosinkratiku |
| **U krizi** | Raste (sve padaju zajedno) | Može rasti negativna između divergentnih sektora |
| **NG u krizi** | Rijetko pun | Puni se - hvata relativnu divergenciju |

**NG ne mjeri "dionice padaju zajedno"** - to bi bila *pozitivna* sirova korelacija.
NG mjeri: dionica $i$ pada **više** od tržišta, dok $j$ pada **manje** - ili obrnuto.
Upravo ta relativna divergencija postaje statistički vidljiva u krizama.

---

## 7. Kako koristiti ostatak materijala

| Notebook | Tema |
|----------|------|
| **01** | Stvarne mrežne mjere kroz 20 godina |
| **02** | Statističko testiranje razlika kriza vs. mirno |
| **03** | Out-of-sample prognoziranje volatilnosti |

---

## 8. Literatura

### Mrežna analiza financijskih tržišta
- Mantegna, R.N. (1999). Hierarchical structure in financial markets. *European Physical Journal B*, 11.
- Onnela, J.-P. et al. (2003). Dynamics of market correlations. *Physical Review E*, 68.
- Billio, M., Getmansky, M., Lo, A.W., Pelizzon, L. (2012). Econometric measures of connectedness and systemic risk. *Journal of Financial Economics*, 104(3).
- Xu, R. et al. (2017). Topological change of the world stock market. *Studies in Economics and Finance*, 34(3).

### Mrežne mjere
- Newman, M.E.J. (2010). *Networks: An Introduction*. Oxford University Press.
- Blondel, V.D. et al. (2008). Fast unfolding of communities in large networks. *Journal of Statistical Mechanics*, P10008.
- Kritzman, M. et al. (2011). Principal components as a measure of systemic risk. *Journal of Portfolio Management*, 37(4).

### Prognoziranje i testiranje
- Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics*, 31(3).
- Diebold, F.X., Mariano, R.S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics*, 13(3).
- Harvey, D., Leybourne, S., Newbold, P. (1997). Testing the equality of prediction mean squared errors. *International Journal of Forecasting*, 13(2).
"""),

]

path = OUT / "00_uvod_i_metodologija.ipynb"
with open(path, "w", encoding="utf-8") as f:
    json.dump(nb(cells), f, ensure_ascii=False, indent=1)
print(f"Saved: {path}")
