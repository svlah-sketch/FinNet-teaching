# _dev — skripte za generiranje i održavanje

Ova mapa sadrži skripte koje generiraju notebookove i provode ispravke.
**Nisu dio nastavnih materijala** — namijenjene su isključivo autorima.

| Skripta | Opis |
|---------|------|
| `build_nb00.py` | Generira notebook 00 (uvod i metodologija) |
| `build_nb03.py` | Generira notebook 03 (prognoziranje) |
| `make_notebooks.py` | Generira notebookove 01–03 |
| `make_intro_notebook.py` | Starija verzija generatora za nb00 (arhiv) |
| `fix_nb01_02.py` | Dodaje objašnjenja i ispravlja jezik u nb01 i nb02 |

Za regeneraciju notebooka pokrenuti iz korijena repozitorija:
```bash
python _dev/build_nb00.py
python _dev/build_nb03.py
python _dev/make_notebooks.py
```
