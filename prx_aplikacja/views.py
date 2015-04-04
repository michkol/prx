from django.shortcuts import render
from django.db.models import Case, When, F
from .models import BramkaProxy

def index(zadanie, strona):
    if strona in [None, '']:
        strona = 1
    else:
        strona = int(strona)

    na_strone = 80
    pierwszy = 80 * (strona - 1)
    ostatni = pierwszy + 80

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

    kontekst = {
        'lista': obiekty[pierwszy:ostatni],
        'dlugosc_pelnej_listy': obiekty.count(),
        'strona': strona,
        'nieklikalny_naglowek': (strona == 1),
        'description_widoczny': True,
        'dluga_stopka': True,
    }

    return render(zadanie, 'prx_aplikacja/index.html', kontekst)
