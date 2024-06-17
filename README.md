## Engeto-pa-3-projekt
Třetí projekt na Python akademii od Engeta.
### Popis projektu
Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017.
### Instalace knihoven
Knihovny použité v kódu jsou uloženy v souboru `requirements.txt`. 
Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:
```bash
$ pip3 --version                    # Ověří verzi manažeru
$ pip3 install -r requirements.txt  # Nainstalují se knihovny
```
### Spuštění projektu
Spuštění souboru main.py v rámci příkazového řádku vyžaduje dva argumenty:
```bash
python main.py <odkaz-uzemniho-celku> <vysledny-soubor>
```
Následně se vám stáhnou výsledky jako soubor s příponou `.csv`
### Ukázka projektu
Výsledky hlasování pro okres Žďár nad Sázavou:
1. argument: `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6105`
2. argument: `vysledek_ZR.csv`

Spuštění programu:
```bash
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6105" "vysledek_ZR.csv"
```
Průběh stahování:
```bash
STAHUJI DATA Z VYBRANEHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6105
UKLADAM DO SOUBORU: vysledek_ZR.csv
UKONCUJI election-scraper
```
Částečný výstup:
```bash
code,location,registered,envelopes,valid,...
595217,Baliny,102,71,71,8,0,0,6,0,3,8,2,1,0,0,...
595241,Blažkov,229,162,161,7,0,0,15,0,9,26,2,3,4,1,...
...
```

