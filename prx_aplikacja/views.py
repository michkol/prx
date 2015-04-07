from django.shortcuts import render, redirect
from django.db.models import Case, When, F, Count
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from .models import BramkaProxy
from .naglowki_stronicowania import dodaj_naglowki_stronicowania
import math
import re
import email.utils

def index(zadanie, strona=None, kraj=None, ip=None):
    # utworzenie ORDER BY
    sortowanie = []

    if ip is None:
        # lista nie według kraju powinna zawierać szybkie polskie nad innymi
        if kraj is None:
            sortowanie.append(Case(When(kraj='PL', ping__lt=250, then=1), default=0).desc())

        # nieodpowiadające pod innymi
        sortowanie.append(Case(When(ping__isnull=True, then=1), default=0).asc())

        # z niewyliczonym numerem sekwencyjnym dla IP jak z bardzo dużym
        # (trwa aktualizacja bazy, wyliczenie nastąpi po jej zakończeniu)
        sortowanie.append(Case(When(ip_indeks__isnull=True, then=1), default=0).asc())

        # według szybkości, ale z coraz mocniejszym obniżaniem pozycji    
        # kolejnych bramek z powtórzonym IP    
        sortowanie.append((F('ping') * F('ip_indeks') + 85 * (F('ip_indeks') - 1)).asc())
    else:
        # według adresu alfabetycznie
        sortowanie.append('adres')

    # utworzenie zapytania
    obiekty = BramkaProxy.objects.order_by(*sortowanie)
    if kraj is not None:
        obiekty = obiekty.filter(kraj=kraj.upper())
    elif ip is not None:
        obiekty = obiekty.filter(ip=ip)

    # nic nie znaleziono
    if not obiekty.exists():
        raise Http404('Nie znaleziono pasujących bramek proxy.')

    # stronicowanie
    if ip is None:
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
    else:
        # lista bramek z jednego IP bez stronicowania
        strona, pierwszy, ostatni = None, None, None
        prefiks_adresow_stron = None

    # kontekst dla szablonu
    kontekst = {
        'lista': obiekty[pierwszy:ostatni],
        'kraj': kraj,
        'ip': ip,
        'dlugosc_pelnej_listy': obiekty.count(),
        'strona': strona,
        'prefiks_adresow_stron': prefiks_adresow_stron,
        'nieklikalny_naglowek': ((kraj, ip) == (None, None) and strona == 1),
        'description_widoczny': ((kraj, ip) == (None, None)),
        'dluga_stopka': ((kraj, ip) == (None, None) and strona == 1),
        'adres_ip_klienta': zadanie.META.get('REMOTE_ADDR'),
    }

    # wygenerowanie odpowiedzi wraz z nagłówkami Link gdy istnieje podział na strony
    odpowiedz = render(zadanie, 'prx_aplikacja/index.html', kontekst)
    
    if strona is not None:
        dodaj_naglowki_stronicowania(odpowiedz, strona, na_strone, obiekty.count(), prefiks_adresow_stron)

    return odpowiedz

def lista_krajow(zadanie):
    # wiersz: kraj i liczba bramek z niego
    kraje_z_liczbami = BramkaProxy.objects.values('kraj').exclude(kraj='')
    kraje_z_liczbami = kraje_z_liczbami.annotate(ile=Count('kraj')).order_by('-ile')
    
    kontekst = {'kraje_z_liczbami': kraje_z_liczbami}
    
    return render(zadanie, 'prx_aplikacja/lista_krajow.html', kontekst)

def losowy(zadanie):
    # losowa działająca bramka proxy z sensowną szybkością
    # z ograniczeniem zbyt częstego wybierania proxy z tego samego IP
    obiekty = BramkaProxy.objects.filter(ping__lt=700, ip_blad=0)
    obiekty = obiekty.extra(select={'waga': 'RANDOM() / (ip_liczba / 2)'}, order_by=['-waga'])
    adres = obiekty.first().adres
    return redirect(adres)

@csrf_exempt
# bez ochrony przed CSRF, ponieważ efektem ubocznym jest tylko wysłanie maila
# a formularz ma być dostępny dla użytkowników z wyłączoną obsługą cookies
# zwłaszcza wchodzących przez bramkę proxy
def dodaj(zadanie):
    if zadanie.method == 'POST':
        # POST - odebranie danych wpisanych do formularza
        proxy = zadanie.POST.get('proxy')

        # wyrażenie regularne pasujące do linków HTML i BBCode
        # często pojawiających się w spamie formularzowym
        wyrazenie_spam = re.compile(r'<a(\s+[^\s]+)*\s+href=|\[url[=\]]',
            re.IGNORECASE | re.DOTALL)

        if proxy in [None, '']:
            # niewypełnione pole
            kontekst = {'stan': 'puste_pole'}
        elif wyrazenie_spam.search(proxy):
            # prawdopodobnie spam
            kontekst = {'stan': 'spam'}
        else:
            # prawidłowa zawartość - wysłanie e-maila
            
            dodatkowe_naglowki = {
                'Received': 'from ' + zadanie.META.get('REMOTE_ADDR') + ' ' +
                            'by prx.centrump2p.com with HTTP; ' +
                            email.utils.formatdate(),
                'User-Agent': 'prx.centrump2p.com',
            }
            
            EmailMessage(
                subject='Nowe proxy do dodania',
                body=proxy,
                to=['colin@colin.net.pl'],
                headers=dodatkowe_naglowki
            ).send()
            
            kontekst = {'stan': 'wyslano'}
    else:
        # nie POST - pokazanie formularza
        kontekst = {'stan': ''}

    return render(zadanie, 'prx_aplikacja/dodawanie.html', kontekst)
