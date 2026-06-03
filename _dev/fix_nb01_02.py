"""
fix_nb01_02.py
Adds explanatory markdown cells after output cells in notebooks 01 and 02,
and fixes Croatian language issues.
"""
import json
from pathlib import Path

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

# ── Language fixes (applied everywhere) ──────────────────────────────────────
LANG_FIXES = [
    ("nije pronaden", "nije pronađen"),
    ("Apsorcijski omjer", "Apsorpcijski omjer"),
    ("apsorcijski omjer", "apsorpcijski omjer"),
    ("AbsRat | Apsorcijski", "AbsRat | Apsorpcijski"),
]

# ── Explanations to insert after specific code cells ─────────────────────────
# Format: (notebook_file, marker_text_in_cell, markdown_to_insert_after)

INSERTS = [

    # ── NB01 ──────────────────────────────────────────────────────────────────
    ("01_mreze_i_podaci.ipynb",
     '["mean","std","min","max","% missing"]',
     '**Što čitati u tablici:** `mean` i `std` govore o tipičnim vrijednostima '
     'kroz sve prozore. `% missing` je ključan: M4, M5, M8 imaju ~50–70% missing '
     '— to su kondicionalne mjere aktivne samo u stresnim periodima (NG-0.001 neprazna). '
     'M1, M2, M3, M6, M7, M9, M10 imaju 0% missing — uvijek dostupne.\n\n'
     '> Visoka standardna devijacija kod M1 i M3 znači da te mjere jako variraju '
     'između mirnih i kriznih prozora — upravo to ih čini korisnima za detekciju stresa.'
    ),

    ("01_mreze_i_podaci.ipynb",
     'plt.savefig("notebook01_figure.png"',
     '**Što vidimo na vremenskom grafu:** Tri sjenčana pojasa označavaju GFC (2008–09), '
     'EU dug (2011–12) i COVID (2020–21). Sve tri mjere pokazuju skokove za vrijeme kriza.\n\n'
     '- **M1 (LCC frakcija):** dramatičan rast u GFC — negativna mreža postaje gusta i '
     'gotovo cijelo tržište u jednoj komponenti\n'
     '- **M3 (prosječni stupanj):** sličan obrazac, ali reagira brže (mjeri gustoću direktno)\n'
     '- **M6 (apsorpcijski omjer):** sporiji, konzistentni rast — mjeri dugoročnu koncentraciju '
     'sistemskog rizika, ne samo trenutni šok\n\n'
     '> Pitanje za razmisliti: zašto M6 ne vraća na bazičnu razinu jednako brzo kao M1 i M3?'
    ),

    ("01_mreze_i_podaci.ipynb",
     'plt.savefig("notebook01_heatmap.png"',
     '**Što vidimo na heatmapi:** Svaka ćelija = Spearman korelacija para mjera '
     'kroz sve prozore. Crvena = pozitivna, plava = negativna.\n\n'
     '- **M1, M2, M3, M7** visoko korelirani međusobno — sve mjere gustoće/povezanosti '
     'NG-0.05 mreže; hvata iste aspekte tržišnog stresa\n'
     '- **M6** umjereno koreliran s M1–M3 — apsorpcijski omjer gradi iz drugog izvora '
     '(kovarijacijska matrica, ne P-prag mreža) ali hvata sličan signal\n'
     '- **M4, M8** slabije korelirani s ostalima jer su kondicionalni — uzorak im je '
     'samo stresni prozori\n'
     '- **M9** (PG mreža) može imati suprotan predznak — mjeri hub-ove u *pozitivnoj* mreži\n\n'
     '> Visoka međukorelacija unutar grupe M1–M3–M7 znači da nije nužno koristiti sve '
     'tri — ali svaka nosi i jedinstven signal koji opravdava uključivanje.'
    ),

    ("01_mreze_i_podaci.ipynb",
     'metrics.drop(columns=["kriza"], inplace=True)',
     '**Što vidimo na histogramima:** Svaki histogram prikazuje raspodjelu mjere '
     'za krizne (narančasto) i mirne (plavo) prozore.\n\n'
     'Ako se distribucije **malo preklapaju** i narančasta je **pomaknuta desno** '
     '→ mjera dobro razlikuje krize od mirnih perioda.\n\n'
     'Ako se distribucije **jako preklapaju** → mjera sama nije dovoljna za klasifikaciju.\n\n'
     '> Ovo je vizualni pregled. Formalni statistički test (Mann-Whitney) koji kvantificira '
     'tu razliku vidjet ćete u Notebooku 02.'
    ),

    # ── NB02 ──────────────────────────────────────────────────────────────────
    ("02_detekcija_kriza.ipynb",
     'res[["mjera","n_kriza","n_mirno","mean_kriza","mean_mirno","cohen_d","mw_p"]]',
     '**Kako čitati tablicu (sortirana po Cohen\'s d opadajuće):**\n\n'
     '- `cohen_d`: veličina efekta. |d| < 0.2 = zanemariv; ≈ 0.5 = srednji; > 0.8 = veliki\n'
     '- `mw_p`: p-vrijednost Mann-Whitney testa (< 0.05 = statistički značajno)\n'
     '- Pozitivan d = krizni prozori imaju **više** vrijednosti (M1–M7: očekivano — '
     'viši stres u krizi)\n'
     '- Negativan d = krizni prozori imaju **manje** vrijednosti (M8, M9: hub centralnost '
     'se smanjuje u krizi)\n'
     '- Mali `n_kriza` za M4/M8 = kondicionalna mjera, manje opservacija\n\n'
     '> Koje mjere imaju |d| > 0.8? Koje imaju p < 0.05? Nisu nužno iste — '
     'p-vrijednost ovisi i o broju opservacija (n), ne samo o veličini efekta.'
    ),

    ("02_detekcija_kriza.ipynb",
     'res[["mjera","cohen_d","mw_p","BH_sig"]]',
     '**Kako čitati BH tablicu:**\n\n'
     '`BH_sig = True` = mjera preživi korekciju za višestruko testiranje.\n\n'
     'Usporedite s `mw_p`: neke mjere s p < 0.05 mogu postati `False` jer BH '
     'podešava prag ovisno o ukupnom broju testova i rangiranju p-vrijednosti.\n\n'
     '**Zašto je to važno?** Kad testiramo 10 mjera odjednom, slučajno bismo očekivali '
     '~0.5 lažno pozitivnih nalaza (10 × 0.05). BH osigurava da stopa lažnih otkrića '
     'ostane ≤ 5% kao *skupina*, ne po pojedinačnom testu.'
    ),

    ("02_detekcija_kriza.ipynb",
     'plt.savefig("notebook02_roc.png"',
     '**Kako čitati ROC krivulju:**\n\n'
     '- Os x = **stopa lažno pozitivnih** — koliko mirnih perioda model pogrešno '
     'klasificira kao krize\n'
     '- Os y = **stopa istinito pozitivnih** — koliko kriznih perioda model ispravno '
     'prepoznaje\n'
     '- Dijagonala = nasumično pogađanje (AUC = 0.50)\n'
     '- **AUC (Area Under Curve):** površina ispod krivulje. Savršen model = 1.0; '
     'nasumičan = 0.5\n\n'
     '**Interpretacija AUC za ekonomske podatke:**\n'
     '- 0.5–0.6: loše\n'
     '- 0.6–0.7: prihvatljivo\n'
     '- 0.7–0.8: dobro\n'
     '- > 0.8: odlično\n\n'
     '> Napomena: logistička regresija ovdje je fitana i evaluirana na istim podacima '
     '(in-sample). Za pravu prognoznu evaluaciju trebala bi se koristiti cross-validacija. '
     'Ovo je ilustrativni primjer — vidi Notebook 03 za pravi OOS test.'
    ),
]


def apply_fixes(nb_path):
    nb_file = Path("notebooks") / nb_path
    with open(nb_file, encoding="utf-8") as f:
        nb = json.load(f)

    # Language fixes in all cells
    n_lang = 0
    for cell in nb["cells"]:
        src = "".join(cell["source"])
        new_src = src
        for old, new in LANG_FIXES:
            new_src = new_src.replace(old, new)
        if new_src != src:
            cell["source"] = new_src.splitlines(keepends=True)
            n_lang += 1

    # Insert explanation cells
    inserts_for_file = [(marker, expl) for (f, marker, expl) in INSERTS if f == nb_path]
    n_inserted = 0
    for marker, expl in inserts_for_file:
        for i, cell in enumerate(nb["cells"]):
            if cell["cell_type"] == "code" and marker in "".join(cell["source"]):
                # Check if next cell is already an explanation (has the same first 30 chars)
                if i + 1 < len(nb["cells"]):
                    next_src = "".join(nb["cells"][i+1]["source"])
                    if next_src[:30] == expl[:30]:
                        break  # already inserted
                nb["cells"].insert(i + 1, md(expl))
                n_inserted += 1
                break

    with open(nb_file, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"{nb_path}: {n_lang} language fixes, {n_inserted} cells inserted")


if __name__ == "__main__":
    apply_fixes("01_mreze_i_podaci.ipynb")
    apply_fixes("02_detekcija_kriza.ipynb")
    print("Done.")
