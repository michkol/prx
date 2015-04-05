# https://blog.whatwg.org/the-road-to-html-5-link-relations
# https://support.google.com/webmasters/answer/1663744?hl=pl

import math

def dodaj_naglowek(odpowiedz, klucz, wartosc):
    if klucz not in odpowiedz:
        odpowiedz[klucz] = wartosc
    else:
        odpowiedz[klucz] += (', ' + wartosc)

def dodaj_naglowki_stronicowania(odpowiedz, aktualna_strona, ile_na_strone, ile_rekordow, prefiks_url):
    if aktualna_strona > 1:
        dodaj_naglowek(odpowiedz, 'Link', '<' + prefiks_url + '>; rel=first')

        poprzednia_url = str(aktualna_strona - 1)
        if poprzednia_url == '1':
            poprzednia_url = ''

        dodaj_naglowek(odpowiedz, 'Link',
            '<' + prefiks_url + poprzednia_url + '>; rel=prev')

    if aktualna_strona < math.ceil(ile_rekordow / ile_na_strone):
        nastepna_url = str(aktualna_strona + 1)

        dodaj_naglowek(odpowiedz, 'Link',
            '<' + prefiks_url + nastepna_url + '>; rel=next')
