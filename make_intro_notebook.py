"""
make_intro_notebook.py
-----------------------
Generates the introductory context notebook (00_uvod_i_metodologija.ipynb).
Run from the project root: python teaching/make_intro_notebook.py
"""
import json
from pathlib import Path

OUT = Path("teaching/notebooks")
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


cells = [

md("""# 00 — Uvod i metodologija: Financijske mreže na tržištu kapitala

Ovaj notebook daje metodološki kontekst za notebookove 01–03 i studentske projekte.
Čitate ga jednom, na početku — ne sadrži zadatke za rješavanje.

**Autor materijala:** Silvija Vlah Jerić, Ekonomski fakultet Zagreb
**Tržište:** Zagrebačka burza (ZSE), indeks CROBEX, 2004–2026
**Napomena:** Materijal je izveden iz tekućeg istraživačkog projekta. Rezultati
istraživanja su u fazi recenzije i nisu dostupni — ovdje je prikazana samo
metodologija, podaci i ilustrativni primjeri.

---
"""),

md("""## 1. Zašto mrežna analiza financijskih tržišta?

Klasični modeli upravljanja portfeljem (Markowitz, CAPM) tretiraju dionice
kao skup u osnovi nepovezanih imovine, a korelacija je sažeta u jednoj matrici.
Mrežna analiza ide korak dalje: **struktura korelacija sama po sebi nosi informaciju**.

Ključna pitanja koja mrežna analiza može adresirati:

| Pitanje | Što mjerimo |
|---------|-------------|
| Je li tržište više ili manje integrirano u krizi? | Veličina i gustoća najveće komponente |
| Koliko brzo se informacije šire? | Prosječna duljina puta |
| Postoje li klasterirane grupe dionica? | Modularnost, broj zajednica |
| Koje su dionice sistemski važne? | Centralnost (eigenvector, closeness) |
| Koliko je sistemski rizik koncentiran? | Apsorcijski omjer |

**Ključna literatura:**
- Mantegna, R.N. (1999). Hierarchical structure in financial markets. *European Physical Journal B*.
- Onnela, J.-P. et al. (2003). Dynamics of market correlations. *Physical Review E*, 68.
- Billio, M. et al. (2012). Econometric measures of connectedness and systemic risk. *Journal of Financial Economics*, 104.
"""),

md("""## 2. P-prag mreže (Xu et al., 2017)

Standardni pristup (Mantegna 1999) koristi korelacije bez formalnog statističkog testa.
**P-prag pristup** (Xu et al. 2017) dodaje testiranje hipoteza:

### Korak 1: Pearson ili Spearman korelacija

Za svaki par dionica $(i, j)$ u vremenskom prozoru $[t_1, t_2]$:

$$\\rho_{ij} = \\text{corr}(r_i, r_j), \\quad p_{ij} = \\Pr(|T| > t_{obs} \\mid H_0: \\rho = 0)$$

gdje su $r_i, r_j$ log-povrati dionice $i$ i $j$ (dnevni, standardizirani CAPM reziduali).

### Korak 2: Dekompozicija na pozitivnu i negativnu podmrežu

- **PG (Positive Graph):** brid $(i,j)$ postoji ako $\\rho_{ij} > 0$ i $p_{ij} < \\alpha$
- **NG (Negative Graph):** brid $(i,j)$ postoji ako $\\rho_{ij} < 0$ i $p_{ij} < \\alpha$

Tipični pragovi: $\\alpha \\in \\{0.001, 0.01, 0.05, 0.10\\}$

### Zašto koristiti NG mrežu za stresne signale?

Negativne korelacije između dionica *rastu* u krizama (zajednički pad).
NG mreža hvata upravo taj signal — u mirnim periodima je prazna ili rijetka,
u krizama postaje gusta i povezana.

**Ključna literatura:**
- Xu, R. et al. (2017). A new nonlinear cointegration framework with an application
  to the environmental Kuznets curve. *Econometrics*, 5(1). *(metodološki temelj)*
"""),

md("""## 3. Podaci: CROBEX i Zagrebačka burza

**CROBEX** je službeni dionički indeks Zagrebačke burze (ZSE).
Rebalansira se dva puta godišnje (revizije) — skup dionica koje čine indeks
se mijenja svake pola godine.

### Karakteristike tržišta

| Karakteristika | Detalj |
|---------------|--------|
| Tip | Granično (frontier) tržište |
| Broj dionica u uzorku | 78 (sve ikad bile u CROBEX, 2004–2026) |
| Frekvencija podataka | Dnevno, CT model trgovanja (aukcija isključena) |
| Valuta | HRK do 31.12.2022.; EUR od 1.1.2023. (fiksni tečaj 7,53450) |
| Broj revizija u analizi | 43 (revizije 10–52, od rujna 2004.) |

### Tržišni faktor

Umjesto CROBEX indeksa koristimo **EW-LOO (equal-weighted leave-one-out)**:
za svaku dionicu $i$, tržišni faktor = jednako-ponderiran prosjek svih *ostalih* dionica.
Razlog: samouključivanje dionice u vlastiti tržišni faktor stvara pristranost u malim indeksima.

### Valutna konverzija

Hrvatska je uvela euro 1.1.2023. Sve cijene prije 2023. su preračunate u EUR
dijeljenjem s 7,53450 kako bi se izbjegao arteficijelni prinos od −87% na prvi
dan 2023. u povratnoj seriji.
"""),

md("""## 4. Vremenski prozori

Analiza se provodi na **nepreklapajućim prozorima** — svaki prozor je neovisan uzorak,
što omogućuje valjanu statističku inferenciju (p-vrijednosti Spearmanovog rho).

### Shema 1: Fiksni prozori (W90)

- Duljina: 90 kalendarskih dana (≈ 60 dana trgovanja)
- Korak: 90 dana (bez preklapanja)
- Broj prozora: ≈ 59

### Shema 2: Revizijski prozori (primarna ko-potvrda)

- Jedan prozor po svakoj CROBEX reviziji
- Granice = granice revizijskog razdoblja
- Broj prozora: 43 (revizije 10–52)

### Krizni periodi

| Kriza | Početak | Kraj | Napomena |
|-------|---------|------|----------|
| GFC | 1.10.2007. | 30.9.2009. | CROBEX −75% peak-to-trough |
| EU dug | 1.4.2011. | 30.9.2012. | + 6 godina domaće recesije |
| COVID | 20.2.2020. | 31.3.2021. | Produženo do sporog oporavka |
"""),

md("""## 5. Deset mrežnih mjera

Sve analize koriste isključivo ove 10 mjera, organizirane u 5 dimenzija.

| ID | Naziv | Opis | Mreža | Prag |
|----|-------|------|-------|------|
| M1 | LCC frakcija | Udio dionica u najvećoj komponenti | NG | 0.05 |
| M2 | Avg path length | Prosj. duljina najkraćeg puta | NG | 0.05 |
| M3 | Mean degree | Prosj. broj bridova po čvoru | NG | 0.05 |
| M4 | # zajednica | Broj Louvain zajednica | NG | 0.001* |
| M5 | Modularnost | Snaga klaster strukture | NG | 0.001* |
| M6 | Apsorcijski omjer | Sistemski rizik (spektralni) | Svi | — |
| M7 | Mean closeness | Prosj. centralnost blizine | NG | 0.10 |
| M8 | Mean eigenvector | Prosj. eigenvector centralnost | NG | 0.001* |
| M9 | Max eigenvector | Maks. eigenvector centralnost | PG | 0.10 |
| M10 | Avg parcijalna kor. | Prosj. parcijalna korelacija | — | — |

*M4, M5, M8 su kondicionalne mjere — izračunate samo kad je NG-0.001 mreža neprazna
(≈30–40% prozora, pretežno stresni periodi). U mirnim periodima = NaN.

### Intuicija po dimenziji

**Povezivost (M1–M3):** U krizama dionice padaju zajedno → negativne korelacije
jačaju → NG mreža postaje gušća i više povezana.

**Fragmentiranost (M4–M5):** U ozbiljnoj krizi NG mreža se može rascijepiti
na jasne klastere (npr. financije vs. industrija).

**Sistemski rizik (M6):** Apsorcijski omjer mjeri koliki udio varijance tržišta
objašnjava mali broj glavnih komponenti — visok M6 = visoka sistemska ranjivost.

**Centralnost (M7–M9):** Mjere koje dionice su "hubovi" negativnih veza (M7, M8)
ili pozitivnih veza (M9).

**Rezidualna ovisnost (M10):** Prosječna parcijalna korelacija kontrolira za
tržišni faktor — mjeri "izravne" veze između dionica iznad tržišnog kretanja.
"""),

md("""## 6. Ilustrativni primjer: konstrukcija mreže

Sljedeći kod pokazuje logiku P-prag mreže na *sintetičkim* podacima
(ne koristimo stvarne cijene dionica kako bismo izbjegli copyright).
"""),

code("""import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from scipy import stats

np.random.seed(42)

# Simuliraj 10 dionica, 90 dana — tri klastera (sektor A, B, C)
n_stocks, n_days = 10, 90
labels = [f"A{i}" for i in range(1,4)] + [f"B{i}" for i in range(1,4)] + [f"C{i}" for i in range(1,5)]

# Tržišni faktor + sektorski faktori + idiosinkratski šum
market  = np.random.randn(n_days)
sector  = np.random.randn(n_days, 3)
idio    = np.random.randn(n_days, n_stocks) * 0.5

returns = np.zeros((n_days, n_stocks))
for i in range(n_stocks):
    s = i // 4  # sektor 0, 1, ili 2
    returns[:, i] = 0.4*market + 0.4*sector[:,min(s,2)] + idio[:,i]

R = pd.DataFrame(returns, columns=labels)
print("Dnevni povrati (prvih 5 dana):")
print(R.head().round(3))
"""),

code("""# Korelacijska matrica i p-vrijednosti
n = len(labels)
rho_mat = np.zeros((n, n))
p_mat   = np.ones((n, n))

for i in range(n):
    for j in range(n):
        if i != j:
            r, p = stats.spearmanr(R.iloc[:, i], R.iloc[:, j])
            rho_mat[i, j] = r
            p_mat[i, j]   = p

# P-prag filtriranje: alpha = 0.10
alpha = 0.10
sig   = p_mat < alpha

# Negativna podmreža (NG): rho < 0 i statistički značajno
NG_adj = (rho_mat < 0) & sig

# Izgradi NetworkX graf
G_NG = nx.from_numpy_array(NG_adj.astype(float))
G_NG = nx.relabel_nodes(G_NG, {i: labels[i] for i in range(n)})

print(f"NG mreža (alpha={alpha}): {G_NG.number_of_edges()} bridova od mogućih {n*(n-1)//2}")
print(f"Čvorovi u najvećoj komponenti: {max(len(c) for c in nx.connected_components(G_NG))} / {n}")
"""),

code("""fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# 1. Korelacijska matrica
ax = axes[0]
im = ax.imshow(rho_mat, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
ax.set_xticks(range(n)); ax.set_xticklabels(labels, rotation=45, fontsize=8)
ax.set_yticks(range(n)); ax.set_yticklabels(labels, fontsize=8)
plt.colorbar(im, ax=ax, shrink=0.8)
ax.set_title(f"Korelacijska matrica (Spearman)\\n10 dionica, 90 dana")

# 2. NG mreža
ax = axes[1]
colors = {"A": "steelblue", "B": "darkorange", "C": "forestgreen"}
node_colors = [colors[label[0]] for label in G_NG.nodes()]
pos = nx.spring_layout(G_NG, seed=42)
nx.draw_networkx(G_NG, pos=pos, ax=ax, node_color=node_colors,
                 node_size=600, font_size=9, font_color="white",
                 edge_color="gray", width=1.5, with_labels=True)
ax.set_title(f"NG mreža (alpha={alpha})\\nPlave=A, Narančaste=B, Zelene=C")
ax.axis("off")

plt.suptitle("P-prag mreža: od korelacijske matrice do grafa", fontsize=12)
plt.tight_layout()
plt.savefig("notebook00_network_example.png", dpi=120, bbox_inches="tight")
plt.show()
print("Napomena: ove dionice su simulirane — samo za ilustraciju metodologije.")
"""),

md("""## 7. Kako koristiti notebookove

| Notebook | Što ćete naučiti | Preporučeni redoslijed |
|----------|-----------------|----------------------|
| **00** (ovaj) | Metodološki kontekst, ilustrativni primjer | Čitati jednom na početku |
| **01** | Rad s pravim mrežnim mjerama, vizualizacija | Drugi |
| **02** | Statistički testovi za detekciju kriza | Treći |
| **03** | Out-of-sample prognoziranje | Četvrti |

Notebooki koriste podatke iz `../sample_data/` — mali CSV-ovi koji sadrže:
- `sample_metrics_W90.csv` — 10 mrežnih mjera za 59 W90 prozora
- `sample_metrics_revision.csv` — iste mjere za 43 revizijska prozora
- `CROBEX_values.csv` — dnevne razine indeksa
- `Revisions.csv` — datumi revizia

**Nema potrebe za pokretanjem originalnih skripti ili pristupom cache datotekama.**
Svi notebooki su u potpunosti samodostatni s ovim CSV-ovima.
"""),

md("""## 8. Literatura za daljnje čitanje

### Mrežna analiza financijskih tržišta
- Mantegna, R.N. (1999). Hierarchical structure in financial markets. *European Physical Journal B*, 11, 193–197.
- Onnela, J.-P., Chakraborti, A., Kaski, K., Kertész, J. (2003). Dynamics of market correlations. *Physical Review E*, 68, 056110.
- Billio, M., Getmansky, M., Lo, A.W., Pelizzon, L. (2012). Econometric measures of connectedness and systemic risk. *Journal of Financial Economics*, 104(3), 535–559.
- Xu, R., Wong, W.-K., Chen, G., Huang, S. (2017). Topological change of the world stock market. *Studies in Economics and Finance*, 34(3), 331–363. *(P-prag metodologija)*

### Mjere mrežne topologije
- Newman, M.E.J. (2010). *Networks: An Introduction*. Oxford University Press. *(standardni udžbenik)*
- Brandes, U. (2001). A faster algorithm for betweenness centrality. *Journal of Mathematical Sociology*, 25(2), 163–177.
- Blondel, V.D. et al. (2008). Fast unfolding of communities in large networks. *Journal of Statistical Mechanics*, P10008. *(Louvain algoritam za zajednice)*

### Sistemski rizik
- Kritzman, M., Li, Y., Page, S., Rigobon, R. (2011). Principal components as a measure of systemic risk. *Journal of Portfolio Management*, 37(4), 112–126. *(apsorcijski omjer)*

### Prognoziranje volatilnosti
- Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics*, 31(3), 307–327. *(GARCH)*
- Diebold, F.X., Mariano, R.S. (1995). Comparing predictive accuracy. *Journal of Business & Economic Statistics*, 13(3), 253–263. *(DM test)*
- Harvey, D., Leybourne, S., Newbold, P. (1997). Testing the equality of prediction mean squared errors. *International Journal of Forecasting*, 13(2), 281–291. *(HLN korekcija)*

### Financijska tržišta u razvoju i graničnim ekonomijama
- Bekaert, G., Harvey, C.R. (2002). Research in emerging markets finance: looking to the future. *Emerging Markets Review*, 3(4), 429–448.
"""),

]

path = OUT / "00_uvod_i_metodologija.ipynb"
with open(path, "w", encoding="utf-8") as f:
    json.dump(nb(cells), f, ensure_ascii=False, indent=1)
print(f"Saved: {path}")
