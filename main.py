# https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xnumnuts=7103
"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Michal Jelínek
email: jelmic@gmail.com
discord: michal2853
"""
import requests
from requests import get
from bs4 import BeautifulSoup as bs
import csv
import sys

#promenne
seznam_vsech_stran = {} #seznam stran, dict{'cislo_strany': 'název strany'}

def odstran_vsechny_mezery(retezec: str) -> str:
    """
    Odstraní v řetězci mezery a nedělitelné mezery
    Požít, pokud by měly být čísla bez mezer (ze zadání projektu není jasné)
    :param retezec: cislo jako string s mezerou, 1 235
    :return: cislo jako string bez mezer, 1235
    """
    # Odstranění běžných mezer
    retezec = retezec.replace(" ", "")
    # Odstranění nedělitelných mezer
    retezec = retezec.replace("\xa0", "")
    return retezec

def vrat_pocet_hlasu_obce(adresa: str) -> dict:
    """
    Vrátí slovník obsahující počty voličů, odevzdaných a platných hlasů obce obce
    :param adresa: html adresa na webu https://volby.cz/ s výsledky pro jednotlivou obec
    :return: slovník obsahující počty voličů (registered, odevzdaných (envelopes) a platných (valid) hlasů obce obce
    """
    rozdelene_html = bs(get(adresa).text, features="html.parser")
    tabulka = rozdelene_html.select_one('div #publikace table')
    registered = tabulka.find("td", attrs={"headers": "sa2"}).text
    envelopes = tabulka.find("td", attrs={"headers": "sa3"}).text
    valid = tabulka.find("td", attrs={"headers": "sa6"}).text
    vysledek = {
        "registered": registered,
        "envelopes": envelopes,
        "valid": valid
    }
    seznam_stran(rozdelene_html)
    vysledky_obce = vrat_vysledky_obce(rozdelene_html)
    vysledek.update(vysledky_obce)
    return(vysledek)

def seznam_stran(rozdelene_html: bs):
    """
    Do globální proměnné seznam_vsech_stran doplní a aktualizuje seznam stran
    :param rozdelene_html: html parsované pomocí: BeautifulSoup(get(adresa).text, features="html.parser")
    """
    global seznam_vsech_stran
    tabulka_1 = rozdelene_html.select_one("div.t2_470:nth-of-type(1) table")
    tabulka_2 = rozdelene_html.select_one("div.t2_470:nth-of-type(2) table")
    tabulka_1.extend(tabulka_2)
    cislo_strana = tabulka_1.select("tr > td:nth-child(1), tr > td:nth-child(2)")
    vysledek = dict(map(lambda i: (cislo_strana[i].text, cislo_strana[i + 1].text), range(len(cislo_strana) - 1)[::2]))
    vysledek.pop("-")
    seznam_vsech_stran.update(vysledek)
    return()

def vrat_vysledky_obce(rozdelene_html: bs) -> dict:
    """
    Vrátí počty hlasů pro jednotlivé strany v dané obci
    :param rozdelene_html: html s výsledky v obci parsované pomocí: BeautifulSoup(get(adresa).text, features="html.parser")
    :return: dict{'cislo_strany': 'pocet_hlasu'} např: dict{'2': '635'}
    """
    tabulka_1 = rozdelene_html.select_one("div.t2_470:nth-of-type(1) table")
    tabulka_2 = rozdelene_html.select_one("div.t2_470:nth-of-type(2) table")
    tabulka_1.extend(tabulka_2)
    cislo_pocet_hlasu = tabulka_1.select("tr > td:nth-child(1), tr > td:nth-child(3)")
    vysledek = dict(map(lambda i: (cislo_pocet_hlasu[i].text, cislo_pocet_hlasu[i + 1].text), range(len(cislo_pocet_hlasu) - 1)[::2]))
    vysledek.pop("-")
    return(vysledek)

def vrat_volebni_vysledky_uzemniho_celku(adresa: str) -> list:
    """
    Hlavní funkce (Public) pro získání výsledků voleb v daném okrese
    :param adresa: html adresa na webu https://volby.cz/ s výsledky v kraji
    :return: List obsahující volební výsledky všech obcí v kraji (jako dict)
            [{'code': '65487', 'location': 'Přelov',...},{'code': '21654', ....},{...}]
    """
    seznam_celku = list()
    vysledek = list()
    rozdelene_html = bs(get(adresa).text, features="html.parser")
    tabulky = rozdelene_html.select("table > tr")
    for radek in tabulky:
        cislo = radek.find("td", {"class": "cislo"})
        nazev = radek.find("td", {"class": "overflow_name"})
        if cislo and nazev is not None:
            seznam_celku.append([cislo.text, nazev.text, "https://volby.cz/pls/ps2017nss/" + cislo.a['href']])
    # vysledky pro jednotlive obce
    a = 0
    for celek in seznam_celku:
        vysledek_obce = vrat_pocet_hlasu_obce(celek[2])
        pomocna = {"code": celek[0], "location": celek[1]}
        pomocna.update(vysledek_obce)
        vysledek.append(pomocna)
    return(vysledek)

def zapis_vysledky_do_csv(vysledky: list, soubor: str):
    # první řádek
    nadpis = ['code', 'location', 'registered', 'envelopes', 'valid']
    for strana in seznam_vsech_stran.values():
        nadpis.append(strana)
    # data v dalších řádcích
    radek = []
    radky = []
    for vysledek in vysledky:
        radek.append(vysledek['code'])
        radek.append(vysledek['location'])
        radek.append(vysledek['registered'])
        radek.append(vysledek['envelopes'])
        radek.append(vysledek['valid'])
        for strana in seznam_vsech_stran:
            radek.append(vysledek[strana])
        radky.append(radek)
        radek = []
    with open(soubor, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';')
        csvwriter.writerow(nadpis)
        csvwriter.writerows(radky)
    return()

filename = "records.csv"
hlavni_odkaz = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103'


if len(sys.argv) != 2:
    print(
        "Pro spuštění chybí argument 'jmeno',",
        "Zapiš: python povinny_argument.py 'jmeno'", sep="\n"
    )
else:
    volebni_vysledky = vrat_volebni_vysledky_uzemniho_celku(hlavni_odkaz)
    zapis_vysledky_do_csv(volebni_vysledky, filename)