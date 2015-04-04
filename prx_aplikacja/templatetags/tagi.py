from django import template
from django.utils.safestring import mark_safe
import math
import copy

register = template.Library()

@register.filter
def pokoloruj_ping(wartosc):
    if wartosc is not None:
        wartosc_liczbowa = float(wartosc)
        
        if (wartosc_liczbowa < 125):
            kolor = 'green'
        elif (wartosc_liczbowa < 400):
            kolor = 'black'
        elif (wartosc_liczbowa < 1100):
            kolor = '#FF6600'
        else:
            kolor = 'red'
        
        return mark_safe('<span style="color: ' + kolor + '">' + str(wartosc) + '</span>')
    else:
        return mark_safe('<span style="color: red">&#8734;</span>')

@register.simple_tag
def linki_stronicowania(aktualna_strona, ile_na_strone, ile_rekordow, ile_linkow, prefiks_href):
    ile_stron = max(1, math.ceil(ile_rekordow / ile_na_strone))
    ile_linkow //= 2
    wynik = ''

    # kilka poprzednich i następnych stron, z aktualną w środku
    strony = list(range(aktualna_strona - ile_linkow, aktualna_strona + ile_linkow + 1))
    
    for numer in copy.copy(strony):
        # blisko pierwszej strony - więcej linków do następnych,
        # ponieważ poprzednich jest za mało
        if numer < 1:
            strony.pop(0)
            nowa = max(strony) + 1
            if (nowa <= ile_stron):
                strony.append(nowa)
        # blisko ostatniej strony - więcej linków do poprzednich,
        # ponieważ następnych jest za mało
        elif numer > ile_stron:
            strony.pop()
            nowa = min(strony) - 1
            if (nowa >= 1):
                strony.insert(0, nowa)
    
    # jeżeli po lewej jest inna niż pierwsza, zastąpienie jej pierwszą
    # i dodanie ...
    if strony[0] != 1:
        strony = [1, '...'] + strony[1:]
    
    # jeżeli po prawej jest inna niż ostatnia, zastąpienie jej ostatnią
    # i dodanie ...
    if strony[-1] != ile_stron:
        strony = strony[:-1] + ['...', ile_stron]
    
    for strona in strony:
        if strona == '...':
            wynik += '<span>&hellip;</span>\n'
        elif strona == aktualna_strona:
            wynik += '<strong>[' + str(strona) + ']</strong>\n'
        else:
            if strona == 1:
                strona_url = ''
            else:
                strona_url = str(strona)
            wynik += '<a href="' + prefiks_href + strona_url + '">' + str(strona) + '</a>\n';

    return mark_safe(wynik)
