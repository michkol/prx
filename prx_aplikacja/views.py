from django.shortcuts import render
from django.db.models import Case, When, F
from django.http import Http404
from .models import BramkaProxy
from .naglowki_stronicowania import dodaj_naglowki_stronicowania
import math

def index(zadanie, strona, kraj=None):
    # utworzenie ORDER BY
    sortowanie = []

    # lista nie według kraju powinna zawierać szybkie polskie nad innymi
    if kraj is not None:
        sortowanie.append(Case(When(kraj='PL', ping__lt=250, then=1), default=0).desc())

    # nieodpowiadające pod innymi
    sortowanie.append(Case(When(ping__isnull=True, then=1), default=0).asc())

    # z niewyliczonym numerem sekwencyjnym dla IP jak z bardzo dużym
    # (trwa aktualizacja bazy, wyliczenie nastąpi po jej zakończeniu)
    sortowanie.append(Case(When(ip_indeks__isnull=True, then=1), default=0).asc())

    # według szybkości, ale z coraz mocniejszym obniżaniem pozycji    
    # kolejnych bramek z powtórzonym IP    
    sortowanie.append((F('ping') * F('ip_indeks') + 85 * (F('ip_indeks') - 1)).asc())

    # utworzenie zapytania
    obiekty = BramkaProxy.objects.order_by(*sortowanie)
    if kraj is not None:
        obiekty = obiekty.filter(kraj=kraj.upper())

    # nic nie znaleziono
    if not obiekty.exists():
        raise Http404('Nie znaleziono pasujących bramek proxy.')

    # stronicowanie
    na_strone = 80
    ile_stron = math.ceil(obiekty.count() / na_strone)

    if (strona in [None, '']) or (int(strona) < 1):
        strona = 1
    elif int(strona) > ile_stron:
        strona = ile_stron
    else:
        strona = int(strona)

    pierwszy = na_strone * (strona - 1)
    ostatni = pierwszy + na_strone

    # początek adresów wskazywanych przez linki do zmiany strony
    if kraj is None:
        prefiks_adresow_stron = '/'
    else:
        prefiks_adresow_stron = '/kraj/' + kraj + '/'

    # kontekst dla szablonu
    kontekst = {
        'lista': obiekty[pierwszy:ostatni],
        'kraj': kraj,
        'dlugosc_pelnej_listy': obiekty.count(),
        'strona': strona,
        'prefiks_adresow_stron': prefiks_adresow_stron,
        'nieklikalny_naglowek': (kraj is None and strona == 1),
        'description_widoczny': (kraj is None),
        'dluga_stopka': (kraj is None),
        'adres_ip': zadanie.META.get('REMOTE_ADDR'),
    }

    # wygenerowanie odpowiedzi wraz z odpowiednimi nagłówkami Link
    odpowiedz = render(zadanie, 'prx_aplikacja/index.html', kontekst)
    dodaj_naglowki_stronicowania(odpowiedz, strona, na_strone, obiekty.count(), prefiks_adresow_stron)
    return odpowiedz
