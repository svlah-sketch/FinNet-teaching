# Financijske mreže i rizik: nastavni materijali

Nastavni materijali razvijeni iz istraživačkog projekta  
**"Financial Network Topology for Systemic Risk: Early Warning, Forecasting, and Euro Adoption on a Frontier Equity Market"**  
(Zagreb Stock Exchange / CROBEX, 2004–2026)

---

## Sadržaj

```
notebooks/
  00_uvod_i_metodologija.ipynb  — Kontekst, P-prag mreže, ilustrativni primjer, literatura
  01_mreze_i_podaci.ipynb       — Korelacijske matrice, P-prag mreže, mrežne mjere
  02_detekcija_kriza.ipynb      — Statistički testovi, detekcija kriza, logistička regresija
  03_prognoziranje.ipynb        — Out-of-sample prognoziranje, GARCH, OLS, DM test
sample_data/
  sample_metrics_W90.csv        — 10 mrežnih mjera, 59 90-dnevnih prozora (2005–2026)
  sample_metrics_revision.csv   — 10 mjera, 43 revizijska prozora CROBEX-a
  CROBEX_values.csv             — Dnevne razine CROBEX indeksa
  Revisions.csv                 — Datumi revizia CROBEX sastava
student_projects/
  README_projekti.md            — 3 studentska mini-projekta
requirements.txt
```

## Otvaranje u Google Colabu

Klikni na gumb za željeni notebook — otvara se odmah u Colabu, bez ikakve instalacije:

| Notebook | Otvori u Colabu |
|----------|----------------|
| 00 — Uvod i metodologija | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/svlah-sketch/FinNet-teaching/blob/main/notebooks/00_uvod_i_metodologija.ipynb) |
| 01 — Mreže i podaci | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/svlah-sketch/FinNet-teaching/blob/main/notebooks/01_mreze_i_podaci.ipynb) |
| 02 — Detekcija kriza | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/svlah-sketch/FinNet-teaching/blob/main/notebooks/02_detekcija_kriza.ipynb) |
| 03 — Prognoziranje | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/svlah-sketch/FinNet-teaching/blob/main/notebooks/03_prognoziranje.ipynb) |

> Prva ćelija svakog notebooka automatski klonira potrebne podatke — samo pokrenite sve ćelije redom.

## Lokalno postavljanje (alternativa)

```bash
pip install -r requirements.txt
jupyter notebook
```

## Podaci

Notebooki koriste podatke iz `sample_data/` — mali CSV-ovi koji ne zahtijevaju
pristup originalnim cache datotekama. Svaki notebook objašnjava strukturu podataka
u prvoj ćeliji.

## Kolegiji

| Notebook | Primjeren za |
|----------|-------------|
| 01 — Mreže i podaci | Financijsko modeliranje, Analiza podataka |
| 02 — Detekcija kriza | Ekonometrija, Strojno učenje u financijama |
| 03 — Prognoziranje | Strojno učenje, Financijsko modeliranje |

## Studentski projekti

Vidi `student_projects/README_projekti.md` za 3 mini-projekta u trajanju 1–2 tjedna.

---

# Financial Networks and Risk: Teaching Materials (EN)

Teaching materials derived from the research project on Zagreb Stock Exchange
network topology. Notebooks cover: correlation-based network construction,
crisis detection, and out-of-sample forecasting — using real Croatian equity
market data (CROBEX, 2004–2026).

**Setup:** `pip install -r requirements.txt` then `jupyter notebook`
