# Mini-projekti za vježbu i isprobavanje

Svaki projekt traje **1–2 tjedna** i oslanja se na notebookove i podatke iz ovog
repozitorija. Polazište je uvijek gotov notebook — proširuješ ga ili modificiraš.

---

## P2 — Novo vremensko razdoblje

**Pitanje:** Jesu li mrežne mjere jednako dobre prediktori krize u *svakom* podrazdoblju,
ili su rezultati vođeni samo GFC-om (2007–2009)?

**Zadatak:**
1. Kopirajte `02_detekcija_kriza.ipynb` kao `P2_podrazdoblje.ipynb`
2. Filtrirajte `sample_metrics_W90.csv` na prozore **od 2015. nadalje**
3. Ponovite Mann-Whitney testove i Cohen's d na tom podskupu
4. Usporedite rezultate s punim uzorkom (2005–2026)
5. Napišite interpretaciju: koje mjere ostaju robusne, koje ne?

**Polazna skripta:** `nonolap_analysis_3crises.py` (originalna istraživačka skripta, za referencu)

**Očekivani output:** tablica s Cohen's d za puni uzorak vs. uzorak od 2015.,
kratka interpretacija (~300 riječi)

---

## P3 — Alternativni prag

**Pitanje:** Mijenja li se struktura mreže ako promijenimo granicu statističke
značajnosti za uključivanje bridova (P-prag)?

**Zadatak:**
1. Otvorite `01_mreze_i_podaci.ipynb` kao polazište
2. Originalna analiza koristi prag **α = 0.05** za negativnu mrežu (NG).
   Usporedite s pragovima α = 0.01 i α = 0.10.
   *(Napomena: podatke za različite pragove možete naći u stupcima cache datoteka —
   koristite `allev_W90_S90_spearman_ew_mean_loo.pkl` ako imate pristup,
   ili postavite pitanje mentoru za subset podataka.)*
3. Vizualizirajte: kako se mijenja M1 (LCC frakcija) za α = 0.01 vs. α = 0.05 vs. α = 0.10?
4. Koji prag daje najveću razliku između kriznih i mirnih perioda (Cohen's d)?

**Polazna skripta:** `network_utils.py` — funkcija `filter_by_pvalue()`

**Očekivani output:** usporedna vizualizacija (3 vremenske serije na jednom grafu),
tablica Cohen's d po pragu

---

## P4 — Alternativni ML model

**Pitanje:** Nadmašuje li **Random Forest** logističku regresiju u klasifikaciji
kriznih perioda?

**Zadatak:**
1. Kopirajte `02_detekcija_kriza.ipynb` kao `P4_random_forest.ipynb`
2. Zamijenite `LogisticRegression` s `RandomForestClassifier` iz scikit-learn
3. Koristite **Leave-One-Out Cross-Validation** (ili k-fold, k=5) za procjenu AUC
   — nemojte fitati i evaluirati na istim podacima!
4. Usporedite ROC krivulje obaju modela na jednom grafu
5. Ispišite važnost značajki (feature importance) za Random Forest:
   koja mrežna mjera najviše doprinosi klasifikaciji?

**Hint za implementaciju:**
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

clf = RandomForestClassifier(n_estimators=100, random_state=42)
auc_cv = cross_val_score(clf, X, y, cv=5, scoring="roc_auc")
print(f"AUC (5-fold CV): {auc_cv.mean():.3f} ± {auc_cv.std():.3f}")
```

**Važno:** S malim uzorkom (N≈59 prozora) CV rezultati će biti nestabilni —
to je dio zaključka!

**Polazna skripta:** `directional_prediction.py` (za uvid u strukturu, ne kopirati direktno)

**Očekivani output:** usporedna ROC krivulja, tablica AUC logit vs. RF,
interpretacija (~300 riječi)
