from django.shortcuts import render, redirect
from django.db.models import Case, When, F, Count
from django.http import Http404, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.middleware.csrf import get_token
from django.utils import timezone
from django.template.defaultfilters import floatformat
from .models import BramkaProxy
from .naglowki_stronicowania import dodaj_naglowki_stronicowania
from .templatetags.tagi import pelna_nazwa_kraju
from .siec import ping
from prx.settings import ADMIN_LOGIN, ADMIN_HASLO
import math
import re
import email.utils
import urllib.parse
import datetime

def lista(zadanie, strona=None, kraj=None, ip=None):
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

    # tytuł strony
    if ip is not None:
        tytul = ip
    elif kraj is not None:
        tytul = pelna_nazwa_kraju(kraj)
    else:
        tytul = None

    # kontekst dla szablonu
    kontekst = {
        'tytul': tytul,
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
    odpowiedz = render(zadanie, 'prx_aplikacja/lista.html', kontekst)
    
    if strona is not None:
        dodaj_naglowki_stronicowania(odpowiedz, strona, na_strone, obiekty.count(), prefiks_adresow_stron)

    return odpowiedz

def stary_kraj(zadanie, skrot, dalsza_sciezka):
    nowe_skroty = {
        'gb': 'uk',
        'tp': 'tl',
        'zr': 'cd',
    }
    return redirect('/kraj/' + nowe_skroty[skrot] + '/' + dalsza_sciezka, permanent=True)

def lista_krajow(zadanie):
    # wiersz: kraj i liczba bramek z niego
    kraje_z_liczbami = BramkaProxy.objects.values('kraj').exclude(kraj='')
    kraje_z_liczbami = kraje_z_liczbami.annotate(ile=Count('kraj')).order_by('-ile')
    
    kontekst = {
        'tytul': 'Według kraju',
        'kraje_z_liczbami': kraje_z_liczbami,
    }
    
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

    kontekst['tytul'] = 'Dodaj proxy'
    return render(zadanie, 'prx_aplikacja/dodawanie.html', kontekst)

def admin(zadanie):
    if not zadanie.session.get('czy_zalogowany'):
        return redirect('/admin/logowanie')

    kontekst = {
        'tytul': 'Panel administracyjny',
        'token': get_token(zadanie),
    }
    return render(zadanie, 'prx_aplikacja/admin.html', kontekst)

@csrf_exempt
# CSRF przy POST jest niemożliwy, ponieważ jednym z pól jest hasło
def admin_logowanie(zadanie):
    if zadanie.method == 'POST':
        # zalogowanie
        podany_login = zadanie.POST.get('login')
        podane_haslo = zadanie.POST.get('haslo')
        
        if (podany_login, podane_haslo) == (ADMIN_LOGIN, ADMIN_HASLO):
            zadanie.session['czy_zalogowany'] = True
        
        return redirect('/admin/')
    elif zadanie.GET.get('wyloguj'):
        # obsługa CSRF
        if zadanie.GET.get('token') != get_token(zadanie):
            return odpowiedz_nieprawidlowy_token()
    
        # wylogowanie
        zadanie.session['czy_zalogowany'] = False
        return redirect('/admin/')
    else:
        # pokazanie formularza logowania
        kontekst = {'tytul': 'Logowanie \u2022 Panel administracyjny'}
        return render(zadanie, 'prx_aplikacja/admin_logowanie.html', kontekst)

def admin_pinger(zadanie):
    if not zadanie.session.get('czy_zalogowany'):
        return redirect('/admin/logowanie')

    if zadanie.method != 'POST':
        # strona pokazująca postęp
    
        # obsługa CSRF
        if zadanie.GET.get('token') != get_token(zadanie):
            return odpowiedz_nieprawidlowy_token()
        
        lista = BramkaProxy.objects
        if not zadanie.GET.get('wszystkie'):
            lista = lista.filter(ost_spr_ping__lt=(timezone.now() - datetime.timedelta(days=7)))
        lista = lista.values_list('ip', flat=True).distinct()

        # kontekst, szablon
        kontekst = {
            'tytul': 'Pinger \u2022 Panel administracyjny',
            'token': get_token(zadanie),
            'adres_post': '/admin/pinger',
            'lista': lista,
        }

        return render(zadanie, 'prx_aplikacja/admin_operacje_ajax.html', kontekst)
    else:
        # żądanie AJAX dotyczące pojedynczego IP
        
        # aktualnie wybrany IP z listy w JS
        ip = zadanie.POST.get('wybrany_element', '')
        
        # ustalenie portu jakiejkolwiek bramki z tego IP
        url = urllib.parse.urlparse(BramkaProxy.objects.filter(ip=ip)[0].adres)
        port = url.port
        if port is None:
            if url.scheme == 'https':
                port = 443
            else:
                port = 80
        
        # czas odpowiedzi na żądanie TCP
        wartosc_ping = ping(ip, port)
        
        # aktualizacja dla wszystkich bramek z tego IP
        BramkaProxy.objects.filter(ip=ip).update(
            ping=wartosc_ping,
            ost_spr_ping=timezone.now()
        )

        # przygotowanie odpowiedzi do pokazania na stronie
        if wartosc_ping is not None:
            ping_str = floatformat(wartosc_ping, 2)
        else:
            ping_str = 'None'
            
        return HttpResponse(
            'ping (port ' + str(port) + ') wynosi ' + ping_str + ' ms.',
            content_type='text/plain; charset=UTF-8'
        )

def odpowiedz_nieprawidlowy_token():
    return HttpResponseForbidden('Nieprawidłowy token.', content_type='text/plain; charset=UTF-8')
