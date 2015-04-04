from django.shortcuts import render
from django.db.models import Case, When, F
from .models import BramkaProxy
import math

def index(zadanie, strona):
    obiekty = BramkaProxy.objects.order_by(
        # szybkie polskie nad innymi
        Case(When(kraj='PL', ping__lt=250, then=1), default=0).desc(),
        
        # nieodpowiadające pod innymi
        Case(When(ping__isnull=True, then=1), default=0).asc(),
        
        # z niewyliczonym numerem sekwencyjnym dla IP jak z bardzo dużym
        # (trwa aktualizacja bazy, wyliczenie nastąpi po jej zakończeniu)
        Case(When(ip_indeks__isnull=True, then=1), default=0).asc(),

        # według szybkości, ale z coraz mocniejszym obniżaniem pozycji
        # kolejnych bramek z powtórzonym IP
        (F('ping') * F('ip_indeks') + 85 * (F('ip_indeks') - 1)).asc()
    )

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

    kontekst = {
        'lista': obiekty[pierwszy:ostatni],
        'dlugosc_pelnej_listy': obiekty.count(),
        'strona': strona,
        'nieklikalny_naglowek': (strona == 1),
        'description_widoczny': True,
        'dluga_stopka': True,
    }

    return render(zadanie, 'prx_aplikacja/index.html', kontekst)
