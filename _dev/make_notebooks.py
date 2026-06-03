"""
make_notebooks.py
-----------------
Generates the three teaching notebooks programmatically.
Run from the project root: python teaching/make_notebooks.py
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


# ─────────────────────────────────────────────────────────────────────────────
# NOTEBOOK 01 — Mreže i podaci
# ─────────────────────────────────────────────────────────────────────────────

cells_01 = [
    md("""# Notebook 01: Korelacijske mreže i mrežne mjere

**Projekt:** Financijske mreže na ZSE (CROBEX, 2004–2026)
**Teme:** Korelacijske matrice, P-prag filtriranje, mjere mrežne topologije
**Kolegiji:** Financijsko modeliranje, Analiza podataka, Uvod u mrežne znanosti

## Kontekst

Financijske mreže konstruiramo iz **matrice korelacija** dionica.
Svaka dionica je čvor; brid postoji samo ako je korelacija statistički značajna
(P-prag pristup, Xu et al. 2017).

Analiziramo **10 mrežnih mjera** koje opisuju strukturu tržišta u svakom vremenskom prozoru:

| Mjera | Opis |
|-------|------|
| M1 LCC | Frakcija dionica u najvećoj komponenti NG mreže |
| M2 APL | Prosječna duljina najkraćeg puta |
| M3 MeanDeg | Prosječni stupanj čvora |
| M4 NCom | Broj zajednica (samo u stresnim periodima) |
| M5 Mod | Modularnost (snaga zajednica) |
| M6 AbsRat | Apsorcijski omjer (sistemski rizik) |
| M7 Close | Prosječna centralnost blizine |
| M8 EigMn | Prosječna eigenvector centralnost |
| M9 EigMx | Maksimalna eigenvector centralnost (PG mreža) |
| M10 PCorr | Prosječna parcijalna korelacija |
"""),

    code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from pathlib import Path

DATA_DIR = Path("../sample_data")

# Učitaj mrežne mjere (W90 — prozori od 90 dana)
metrics = pd.read_csv(DATA_DIR / "sample_metrics_W90.csv",
                      index_col="window_end", parse_dates=True)

print(f"Oblik podataka: {metrics.shape}")
print(f"Vremenski raspon: {metrics.index.min().date()} do {metrics.index.max().date()}")
print()
print(metrics.head())"""),

    md("""## 1. Deskriptivna statistika mrežnih mjera"""),

    code("""desc = metrics.describe().T
desc["% missing"] = metrics.isna().mean() * 100
print(desc[["mean","std","min","max","% missing"]].round(3).to_string())"""),

    md("""## 2. Vremenska serija odabranih mjera

Vizualiziramo M1 (LCC frakcija), M3 (prosječni stupanj) i M6 (apsorcijski omjer).
Označeni su periodi tri financijske krize.
"""),

    code("""CRISES = {
    "GFC":     ("2007-10-01", "2009-09-30"),
    "EU_DEBT": ("2011-04-01", "2012-09-30"),
    "COVID":   ("2020-02-20", "2021-03-31"),
}

fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
cols = ["M1_LCC", "M3_MeanDeg", "M6_AbsRat"]
titles = ["M1: LCC frakcija", "M3: Prosječni stupanj", "M6: Apsorcijski omjer"]
colors = ["steelblue", "darkorange", "forestgreen"]

for ax, col, title, color in zip(axes, cols, titles, colors):
    ax.plot(metrics.index, metrics[col], color=color, lw=1.5, label=col)
    for name, (start, end) in CRISES.items():
        ax.axvspan(start, end, alpha=0.12, color="red", label=name if col == cols[0] else "")
    ax.set_title(title, fontsize=11)
    ax.grid(alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

axes[0].legend(loc="upper right")
fig.suptitle("Mrežne mjere CROBEX-a kroz vrijeme (W90)", fontsize=13)
plt.tight_layout()
plt.savefig("notebook01_figure.png", dpi=120, bbox_inches="tight")
plt.show()"""),

    md("""## 3. Korelacijska matrica mjera

Koliko su mjere međusobno korelirane? Visoka korelacija sugerira da mjere
hvate iste aspekte tržišne strukture.
"""),

    code("""corr = metrics.corr(method="spearman")

fig, ax = plt.subplots(figsize=(8, 6))
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
            center=0, vmin=-1, vmax=1, ax=ax, square=True,
            linewidths=0.5, cbar_kws={"shrink": 0.8})
ax.set_title("Spearman korelacija između mrežnih mjera (W90)")
plt.tight_layout()
plt.savefig("notebook01_heatmap.png", dpi=120, bbox_inches="tight")
plt.show()"""),

    md("""## 4. Razdioba mjera: krize vs. mirna razdoblja

Uspoređujemo raspodjele M1 (LCC) i M3 (stupanj) za krizna i mirna razdoblja.
Vizualni pregled — formalni statistički testovi su u Notebooku 02.
"""),

    code("""revs_dates = pd.read_csv(DATA_DIR / "Revisions.csv", sep=";", encoding="cp1250")
revs_dates["start_date"] = pd.to_datetime(revs_dates["start_date"], dayfirst=True)
revs_dates["end_date"]   = pd.to_datetime(revs_dates["end_date"],   dayfirst=True)

def is_crisis(date):
    for start, end in CRISES.values():
        if pd.Timestamp(start) <= date <= pd.Timestamp(end):
            return True
    return False

metrics["kriza"] = metrics.index.map(is_crisis)
print(f"Kriznih prozora: {metrics['kriza'].sum()} / {len(metrics)}")

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
for ax, col in zip(axes, ["M1_LCC", "M3_MeanDeg"]):
    for label, group in metrics.groupby("kriza")[col]:
        ax.hist(group.dropna(), bins=15, alpha=0.6,
                label="Kriza" if label else "Mirno", density=True)
    ax.set_title(col)
    ax.set_xlabel("Vrijednost mjere")
    ax.legend()
    ax.grid(alpha=0.3)
plt.suptitle("Razdioba mjera: krize vs. mirna razdoblja")
plt.tight_layout()
plt.show()
metrics.drop(columns=["kriza"], inplace=True)"""),

    md("""---

## Zadaci za studente

**1.** Koji par mjera ima najveću apsolutnu Spearman korelaciju? Zašto biste to
   očekivali s obzirom na njihove definicije?

**2.** Dodajte u vremenski graf M9 (EigMx — PG mreža). Ima li suprotan trend od M1?
   Što to govori o ulozi "hub" dionica u mirnim i kriznim periodima?

**3.** Koliko prozora pripada svakoj krizi (GFC, EU_DEBT, COVID)?
   Koristite `metrics.index` i datume kriza iz rječnika `CRISES`.

**4.** (Napredni) M4 i M8 imaju mnogo NaN vrijednosti. Pogledajte `% missing` iz
   deskriptivne statistike. Zašto bi te mjere bile dostupne samo u *nekim* prozorima?
   (Hint: NG-0.001 prag)
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# NOTEBOOK 02 — Detekcija kriza
# ─────────────────────────────────────────────────────────────────────────────

cells_02 = [
    md("""# Notebook 02: Statistička detekcija financijskih kriza

**Projekt:** Financijske mreže na ZSE (CROBEX, 2004–2026)
**Teme:** Mann-Whitney test, Cohen's d, logistička regresija, BH korekcija višestrukih testiranja
**Kolegiji:** Ekonometrija, Strojno učenje u financijama, Statistika

## Kontekst

Pitanje: **razlikuju li se mrežne mjere statistički između kriznih i mirnih perioda?**

Koristimo tri tehnike:
1. **Mann-Whitney U test** — neparametarski, ne pretpostavlja normalnost
2. **Cohen's d** — veličina efekta (koliko standardnih devijacija razlike?)
3. **Logistička regresija** — može li jedna mjera klasificirati period kao krizni?

Na kraju primjenjujemo **Benjamini-Hochberg (BH) korekciju** za višestruka testiranja.
"""),

    code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

DATA_DIR = Path("../sample_data")

metrics = pd.read_csv(DATA_DIR / "sample_metrics_W90.csv",
                      index_col="window_end", parse_dates=True)

CRISES = {
    "GFC":     ("2007-10-01", "2009-09-30"),
    "EU_DEBT": ("2011-04-01", "2012-09-30"),
    "COVID":   ("2020-02-20", "2021-03-31"),
}

def is_crisis(date):
    for start, end in CRISES.values():
        if pd.Timestamp(start) <= date <= pd.Timestamp(end):
            return True
    return False

metrics["kriza"] = metrics.index.map(is_crisis)
print(f"Kriznih prozora: {metrics['kriza'].sum()}, Mirnih: {(~metrics['kriza']).sum()}")"""),

    md("""## 1. Mann-Whitney U test i Cohen's d

Za svaku mjeru testiramo razliku između kriznih i mirnih prozora.

**Cohen's d** interpretacija:
- |d| < 0.2: zanemariv efekt
- |d| ≈ 0.5: srednji efekt
- |d| > 0.8: veliki efekt
"""),

    code("""def cohens_d(x, y):
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(((nx-1)*x.std(ddof=1)**2 + (ny-1)*y.std(ddof=1)**2) / (nx+ny-2))
    return (x.mean() - y.mean()) / pooled_std if pooled_std > 0 else np.nan

results = []
metric_cols = [c for c in metrics.columns if c != "kriza"]

for col in metric_cols:
    crisis  = metrics.loc[metrics["kriza"],  col].dropna()
    tranquil = metrics.loc[~metrics["kriza"], col].dropna()
    if len(crisis) < 3 or len(tranquil) < 3:
        continue
    stat, pval = stats.mannwhitneyu(crisis, tranquil, alternative="two-sided")
    d = cohens_d(crisis, tranquil)
    results.append({"mjera": col, "n_kriza": len(crisis), "n_mirno": len(tranquil),
                    "mean_kriza": crisis.mean(), "mean_mirno": tranquil.mean(),
                    "cohen_d": d, "mw_p": pval})

res = pd.DataFrame(results).sort_values("cohen_d", ascending=False)
print(res[["mjera","n_kriza","n_mirno","mean_kriza","mean_mirno","cohen_d","mw_p"]].to_string(index=False))"""),

    md("""## 2. Benjamini-Hochberg korekcija

Kad testiramo 10 mjera istovremeno, povećava se rizik lažno pozitivnih nalaza.
BH korekcija kontrolira **stopu lažnih otkrića (FDR)** umjesto individualne p-vrijednosti.
"""),

    code("""def bh_correct(pvals, q=0.05):
    m = len(pvals)
    ranked = sorted(enumerate(pvals), key=lambda x: x[1])
    reject = [False] * m
    for rank, (i, p) in enumerate(ranked, 1):
        if p <= q * rank / m:
            reject[i] = True
        else:
            break
    return reject

pvals = res["mw_p"].values
reject = bh_correct(pvals, q=0.05)
res["BH_sig"] = reject

print("BH korekcija (q=0.05):")
print(res[["mjera","cohen_d","mw_p","BH_sig"]].to_string(index=False))"""),

    md("""## 3. Logistička regresija: može li mjera predvidjeti krizu?

Koristimo M1 (LCC frakcija) kao prediktor binarne varijable "kriza".
"""),

    code("""from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler

best_metric = res.iloc[0]["mjera"]  # najjači Cohen's d
X_raw = metrics[best_metric].values.reshape(-1, 1)
y = metrics["kriza"].astype(int).values

# Izbaci NaN
mask = ~np.isnan(X_raw.ravel())
X_clean, y_clean = X_raw[mask], y[mask]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_clean)

model = LogisticRegression()
model.fit(X_scaled, y_clean)
proba = model.predict_proba(X_scaled)[:, 1]
auc = roc_auc_score(y_clean, proba)

fpr, tpr, _ = roc_curve(y_clean, proba)
plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, lw=2, label=f"ROC krivulja (AUC = {auc:.3f})")
plt.plot([0, 1], [0, 1], "k--", alpha=0.5)
plt.xlabel("Stopa lažno pozitivnih")
plt.ylabel("Stopa istinito pozitivnih")
plt.title(f"ROC krivulja — {best_metric} kao prediktor krize")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("notebook02_roc.png", dpi=120, bbox_inches="tight")
plt.show()
print(f"\\nPrva mjera: {best_metric}, AUC = {auc:.3f}")"""),

    md("""---

## Zadaci za studente

**1.** Mijenjate li `q` u BH korekciji s 0.05 na 0.10, koje dodatne mjere postaju
   statistički značajne? Što to znači za interpretaciju?

**2.** Izračunajte Cohen's d *po krizi* (GFC, EU_DEBT, COVID posebno).
   Je li GFC konzistentno jača kriza od COVID-19 u ovim podacima?

**3.** Zamijenite logistički regresiju s **SVM-om** (`sklearn.svm.SVC` s `probability=True`).
   Usporedite AUC s logističkim modelom. Koji model je bolji? Zašto?

**4.** (Napredni) M4 i M8 su NaN za mnoge prozore. Mogu li se koristiti u
   logističkoj regresiji? Što trebate napraviti s nedostajućim podacima?
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# NOTEBOOK 03 — Prognoziranje volatilnosti: Spearman pristup
# ─────────────────────────────────────────────────────────────────────────────

cells_03 = [
    md("""# Notebook 03: Mrežne mjere kao prediktori volatilnosti

**Projekt:** Financijske mreže na ZSE (CROBEX, 2004–2026)
**Teme:** Out-of-sample evaluacija, GARCH(1,1), OLS expanding window, QLIKE gubitak, DM test
**Kolegiji:** Strojno učenje u financijama, Financijsko modeliranje

## Kontekst

Uspoređujemo prognoznu točnost triju modela za **buduću volatilnost** CROBEX tržišta:

- **AR(1)** — autoregresija na sekvenci volatilnosti (standardni baseline)
- **NET** — OLS gdje je prediktor *mrežna mjera* (bez prošle volatilnosti)
- **GARCH(1,1)** — standardna referentna točka u praksi (ako arch paket dostupan)

**Ključno:** expanding window — model se uvijek trenira samo na prošlim podacima.
Kršenje ovog pravila (look-ahead bias) je najčešća greška u ML za financije.
"""),

    code("""import warnings
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

DATA_DIR = Path("../sample_data")

# CROBEX dnevni log-prinosi
crobex_raw = pd.read_csv(DATA_DIR / "CROBEX_values.csv", sep=";", encoding="cp1250")
crobex_raw["date"]   = pd.to_datetime(crobex_raw["date"], dayfirst=True)
crobex_raw["crobex"] = pd.to_numeric(crobex_raw["crobex"], errors="coerce")
crobex_ret = np.log(crobex_raw.sort_values("date").set_index("date")["crobex"]).diff().dropna()

# Revizijski prozori i mrežne mjere
revs = pd.read_csv(DATA_DIR / "Revisions.csv", sep=";", encoding="cp1250")
revs["start_date"] = pd.to_datetime(revs["start_date"], dayfirst=True)
revs["end_date"]   = pd.to_datetime(revs["end_date"],   dayfirst=True)
revs = revs[(revs["rev_cnt"] >= 10) & (revs["rev_cnt"] <= 52)].reset_index(drop=True)

metrics = pd.read_csv(DATA_DIR / "sample_metrics_revision.csv",
                      index_col="window_end", parse_dates=True)

print(f"CROBEX: {len(crobex_ret)} dnevnih prinosa")
print(f"Revizijskih prozora: {len(revs)}")"""),

    md("""## 1. Realizirana volatilnost po prozoru

Za svaki revizijski prozor izračunavamo anualiziranu standardnu devijaciju:

$$\\sigma_t = \\text{std}(r_d, d \\in [t_{start}, t_{end}]) \\times \\sqrt{252}$$

Cilj prognoze je $\\sigma_{t+1}$ — volatilnost *sljedećeg* prozora.
"""),

    code("""rows = []
for i, row in revs.iterrows():
    r = crobex_ret.loc[row["start_date"]:row["end_date"]].dropna()
    vol = float(r.std(ddof=1) * np.sqrt(252)) if len(r) >= 10 else np.nan
    diffs = (metrics.index - row["end_date"]).to_series().abs()
    best  = int(diffs.values.argmin())
    met_row = metrics.iloc[best] if diffs.iloc[best].days <= 5 else pd.Series(dtype=float)
    entry = {"end_date": row["end_date"], "start_date": row["start_date"], "vol": vol}
    for col in metrics.columns:
        entry[col] = float(met_row[col]) if col in met_row.index else np.nan
    rows.append(entry)

df = pd.DataFrame(rows)
df["vol_next"] = df["vol"].shift(-1)
df = df.iloc[:-1].copy()
print(f"Prozora za evaluaciju: {df['vol_next'].notna().sum()}")
print(df[["end_date","vol","vol_next","M1_LCC","M3_MeanDeg"]].head(6).to_string(index=False))"""),

    md("""## 2. OLS modeli — expanding window

Za svaki prozor $t$ (počevši od `MIN_TRAIN`):
- Treniraj OLS samo na prozorima $1, 2, ..., t-1$
- Prognozi $\\hat{\\sigma}_{t+1}$ koristeći vrijednosti u trenutku $t$
"""),

    code("""MIN_TRAIN = 15

def ols_predict(y_train, X_train, x_pred):
    try:
        X_c = np.column_stack([np.ones(len(X_train)), X_train])
        coef, *_ = np.linalg.lstsq(X_c, y_train, rcond=None)
        return float(coef @ np.concatenate([[1.0], x_pred]))
    except Exception:
        return np.nan

N = len(df)
ar1_hat = np.full(N, np.nan)
net_hat = {col: np.full(N, np.nan) for col in metrics.columns}

for t in range(MIN_TRAIN, N):
    y   = df["vol_next"].iloc[:t].values
    lag = df["vol"].iloc[:t].values
    ok  = ~np.isnan(y) & ~np.isnan(lag)
    if ok.sum() >= 5:
        p = ols_predict(y[ok], lag[ok].reshape(-1,1), [df["vol"].iloc[t]])
        ar1_hat[t] = max(p, 0.01) if not np.isnan(p) else np.nan
    for col in metrics.columns:
        met = df[col].iloc[:t].values
        ok_m = ~np.isnan(y) & ~np.isnan(met)
        if ok_m.sum() >= 5:
            p = ols_predict(y[ok_m], met[ok_m].reshape(-1,1), [df[col].iloc[t]])
            net_hat[col][t] = max(p, 0.01) if not np.isnan(p) else np.nan

df["vol_hat_ar1"] = ar1_hat
for col in metrics.columns:
    df[f"net_{col}"] = net_hat[col]
print("Modeli fitani.")"""),

    md("""## 3. QLIKE gubitak i Diebold-Mariano test

**QLIKE gubitak** (standardan za procjenu volatilnosti):
$$\\text{QLIKE} = \\log(\\hat{\\sigma}^2) + \\frac{\\sigma^2_{real}}{\\hat{\\sigma}^2}$$

**DM test** ($H_0$: jednaka točnost). Negativni DM statistik → NET model bolji od AR(1).
"""),

    code("""def qlike(hat, real):
    h2 = hat**2
    return np.log(h2) + real**2 / h2

def dm_test(loss_alt, loss_bench):
    d = loss_alt - loss_bench
    T = len(d)
    dm = d.mean() / np.sqrt(np.var(d, ddof=1) / T)
    k  = (T + 1 - 2 + 1.0/T) / T
    dm_adj = dm * np.sqrt(k)
    p = 2 * (1 - stats.norm.cdf(abs(dm_adj)))
    return float(dm_adj), float(p)

y_r = df["vol_next"].values
ql_ar1 = np.where(~np.isnan(df["vol_hat_ar1"]), qlike(df["vol_hat_ar1"].values, y_r), np.nan)

print(f"{'Mjera':<20} {'Mean QL NET':>12} {'Mean QL AR1':>12} {'DM stat':>9} {'p':>8} {'Bolji?':>7}")
print("-" * 72)
for col in metrics.columns:
    hat = df[f"net_{col}"].values
    ql = np.where(~np.isnan(hat), qlike(hat, y_r), np.nan)
    mask = ~np.isnan(ql) & ~np.isnan(ql_ar1)
    if mask.sum() < 5:
        continue
    stat, p = dm_test(ql[mask], ql_ar1[mask])
    bolji = "DA *" if stat < 0 and p < 0.10 else ("-" if p >= 0.10 else "LOŠIJI")
    print(f"{col:<20} {np.nanmean(ql[mask]):>12.4f} {np.nanmean(ql_ar1[mask]):>12.4f} "
          f"{stat:>9.3f} {p:>8.4f} {bolji:>7}")"""),

    md("""## 4. Vizualizacija"""),

    code("""fig, axes = plt.subplots(1, 2, figsize=(13, 4))

ax = axes[0]
ax.plot(df["end_date"], df["vol_next"], "k-", lw=1.5, label="Realizirana vol.")
ax.plot(df["end_date"], df["vol_hat_ar1"], "b--", lw=1, alpha=0.8, label="AR(1)")
ax.set_title("Realizirana vs. prognozirana volatilnost")
ax.set_ylabel("Anualizirana vol.")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.legend(); ax.grid(alpha=0.3)

ax = axes[1]
best_col = "M4_NCom"
mask = df[best_col].notna() & df["vol_next"].notna()
sc = ax.scatter(df.loc[mask, best_col], df.loc[mask, "vol_next"],
                c=df.loc[mask, "end_date"].astype(int), cmap="plasma", s=50, alpha=0.8)
rho = df.loc[mask, [best_col, "vol_next"]].corr(method="spearman").iloc[0, 1]
ax.set_xlabel(f"{best_col} (samo stresni prozori)")
ax.set_ylabel("Sljedeća vol.")
ax.set_title(f"{best_col} vs. buduća vol. (Spearman rho={rho:.3f})")
ax.grid(alpha=0.3)
plt.colorbar(sc, ax=ax, label="Godina")

plt.tight_layout()
plt.savefig("notebook03_figure.png", dpi=120, bbox_inches="tight")
plt.show()"""),

    md("""---

## Zadaci za studente

**1.** Zamijenite `M4_NCom` s `M1_LCC` u scatter plotu. Mijenja li se Spearman ρ?

**2.** Implementirajte **kombinirani model AR1NET**: $\\hat{\\sigma} = \\alpha + \\beta_1 \\sigma_t + \\beta_2 m_t$.
   Usporedite DM test s AR(1) baseline-om.

**3.** Smanjite `MIN_TRAIN` s 15 na 8 prozora. Što se događa s brojem OOS prozora?
   Poboljšavaju li se ili pogoršavaju procjene?

**4.** (Napredni) Zamijenite QLIKE s MSE gubidtkom: $(\\hat{\\sigma} - \\sigma_{real})^2$.
   Mijenja li se poredak modela? QLIKE penalizira podcjenjivanje volatilnosti više od MSE — zašto je to važno u upravljanju rizikom?
"""),
]

# ─────────────────────────────────────────────────────────────────────────────
# Spremi notebookove
# ─────────────────────────────────────────────────────────────────────────────

for filename, cells in [
    ("01_mreze_i_podaci.ipynb", cells_01),
    ("02_detekcija_kriza.ipynb", cells_02),
    ("03_prognoziranje.ipynb", cells_03),
]:
    path = OUT / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb(cells), f, ensure_ascii=False, indent=1)
    print(f"Saved: {path}")

print("\nSvi notebooki kreirani.")
