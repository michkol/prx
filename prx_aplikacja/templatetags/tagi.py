from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import floatformat
import math
import copy

register = template.Library()

@register.filter
def pokoloruj_ping(wartosc):
    if wartosc is not None:
        if wartosc < 125:
            kolor = 'green'
        elif wartosc < 400:
            kolor = 'black'
        elif wartosc < 1100:
            kolor = '#FF6600'
        else:
            kolor = 'red'
        
        return mark_safe('<span style="color: ' + kolor + '">' + floatformat(wartosc, 2) + '</span>')
    else:
        return mark_safe('<span style="color: red">&#8734;</span>')

@register.filter
def pelna_nazwa_kraju(skrot):
    nazwy = {
        'AD': 'Andora',
        'AE': 'Zjednoczone Emiraty Arabskie',
        'AF': 'Afganistan',
        'AG': 'Antigua i Barbuda',
        'AI': 'Anguilla',
        'AL': 'Albania',
        'AM': 'Armenia',
        'AN': 'Antyle Holenderskie',
        'AO': 'Angola',
        'AQ': 'Antarktyda',
        'AR': 'Argentyna',
        'AS': 'Samoa Amerykańskie',
        'AT': 'Austria',
        'AU': 'Australia',
        'AW': 'Aruba',
        'AZ': 'Azerbejdżan',
        'BA': 'Bośnia i Hercegowina',
        'BB': 'Barbados',
        'BD': 'Bangladesz',
        'BE': 'Belgia',
        'BF': 'Burkina Faso',
        'BG': 'Bułgaria',
        'BH': 'Bahrajn',
        'BI': 'Burundi',
        'BJ': 'Benin',
        'BM': 'Bermudy',
        'BN': 'Brunei',
        'BO': 'Boliwia',
        'BR': 'Brazylia',
        'BS': 'Bahamy',
        'BT': 'Bhutan',
        'BV': 'Wyspa Bouveta',
        'BW': 'Botswana',
        'BY': 'Białoruś',
        'BZ': 'Belize',
        'CA': 'Kanada',
        'CC': 'Wyspy Kokosowe',
        'CD': 'Demokratyczna Republika Konga',
        'CF': 'Republika Środkowoafrykańska',
        'CG': 'Kongo',
        'CH': 'Szwajcaria',
        'CI': 'Wybrzeże Kości Słoniowej',
        'CK': 'Wyspy Cooka',
        'CL': 'Chile',
        'CM': 'Kamerun',
        'CN': 'Chiny',
        'CO': 'Kolumbia',
        'CR': 'Kostaryka',
        'CU': 'Kuba',
        'CV': 'Republika Zielonego Przylądka',
        'CX': 'Wyspa Bożego Narodzenia',
        'CY': 'Cypr',
        'CZ': 'Czechy',
        'DE': 'Niemcy',
        'DJ': 'Dżibuti',
        'DK': 'Dania',
        'DM': 'Dominika',
        'DO': 'Dominikana',
        'DZ': 'Algieria',
        'EC': 'Ekwador',
        'EE': 'Estonia',
        'EG': 'Egipt',
        'EH': 'Sahara Zachodnia',
        'ER': 'Erytrea',
        'ES': 'Hiszpania',
        'ET': 'Etiopia',
        'FI': 'Finlandia',
        'FJ': 'Fidżi',
        'FK': 'Falklandy',
        'FM': 'Mikronezja',
        'FO': 'Wyspy Owcze',
        'FR': 'Francja',
        'FX': 'Francja metropolitarna',
        'GA': 'Gabon',
        'GD': 'Grenada',
        'GE': 'Gruzja',
        'GF': 'Gujana Francuska',
        'GH': 'Ghana',
        'GI': 'Gibraltar',
        'GL': 'Grenlandia',
        'GM': 'Gambia',
        'GN': 'Gwinea',
        'GP': 'Gwadelupa',
        'GQ': 'Gwinea Równikowa',
        'GR': 'Grecja',
        'GS': 'Georgia Południowa i Sandwich Południowy',
        'GT': 'Gwatemala',
        'GU': 'Guam',
        'GW': 'Gwinea Bissau',
        'GY': 'Gujana',
        'HK': 'Hongkong',
        'HM': 'Wyspy Heard i McDonalda',
        'HN': 'Honduras',
        'HR': 'Chorwacja',
        'HT': 'Haiti',
        'HU': 'Węgry',
        'ID': 'Indonezja',
        'IE': 'Irlandia',
        'IL': 'Izrael',
        'IN': 'Indie',
        'IO': 'Brytyjskie Terytorium Oceanu Indyjskiego',
        'IQ': 'Irak',
        'IR': 'Iran',
        'IS': 'Islandia',
        'IT': 'Włochy',
        'JM': 'Jamajka',
        'JO': 'Jordania',
        'JP': 'Japonia',
        'KE': 'Kenia',
        'KG': 'Kirgistan',
        'KH': 'Kambodża',
        'KI': 'Kiribati',
        'KM': 'Komory',
        'KN': 'Saint Kitts i Nevis',
        'KP': 'Korea Północna',
        'KR': 'Korea Południowa',
        'KW': 'Kuwejt',
        'KY': 'Kajmany',
        'KZ': 'Kazachstan',
        'LA': 'Laos',
        'LB': 'Liban',
        'LC': 'Saint Lucia',
        'LI': 'Liechtenstein',
        'LK': 'Sri Lanka',
        'LR': 'Liberia',
        'LS': 'Lesotho',
        'LT': 'Litwa',
        'LU': 'Luksemburg',
        'LV': 'Łotwa',
        'LY': 'Libia',
        'MA': 'Maroko',
        'MC': 'Monako',
        'MD': 'Mołdawia',
        'ME': 'Czarnogóra',
        'MG': 'Madagaskar',
        'MH': 'Wyspy Marshalla',
        'MK': 'Macedonia',
        'ML': 'Mali',
        'MM': 'Birma',
        'MN': 'Mongolia',
        'MO': 'Makau',
        'MP': 'Mariany Północne',
        'MQ': 'Martynika',
        'MR': 'Mauretania',
        'MS': 'Montserrat',
        'MT': 'Malta',
        'MU': 'Mauritius',
        'MV': 'Malediwy',
        'MW': 'Malawi',
        'MX': 'Meksyk',
        'MY': 'Malezja',
        'MZ': 'Mozambik',
        'NA': 'Namibia',
        'NC': 'Nowa Kaledonia',
        'NE': 'Niger',
        'NF': 'Norfolk',
        'NG': 'Nigeria',
        'NI': 'Nikaragua',
        'NL': 'Holandia',
        'NO': 'Norwegia',
        'NP': 'Nepal',
        'NR': 'Nauru',
        'NU': 'Niue',
        'NZ': 'Nowa Zelandia',
        'OM': 'Oman',
        'PA': 'Panama',
        'PE': 'Peru',
        'PF': 'Polinezja Francuska',
        'PG': 'Papua-Nowa Gwinea',
        'PH': 'Filipiny',
        'PK': 'Pakistan',
        'PL': 'Polska',
        'PM': 'Saint-Pierre i Miquelon',
        'PN': 'Pitcairn',
        'PR': 'Portoryko',
        'PT': 'Portugalia',
        'PW': 'Palau',
        'PY': 'Paragwaj',
        'QA': 'Katar',
        'RE': 'Reunion',
        'RO': 'Rumunia',
        'RS': 'Serbia',
        'RU': 'Rosja',
        'RW': 'Rwanda',
        'SA': 'Arabia Saudyjska',
        'SB': 'Wyspy Salomona',
        'SC': 'Seszele',
        'SD': 'Sudan',
        'SE': 'Szwecja',
        'SG': 'Singapur',
        'SH': 'Święta Helena',
        'SI': 'Słowenia',
        'SJ': 'Svalbard i Jan Mayen',
        'SK': 'Słowacja',
        'SL': 'Sierra Leone',
        'SM': 'San Marino',
        'SN': 'Senegal',
        'SO': 'Somalia',
        'SR': 'Surinam',
        'ST': 'Wyspy Świętego Tomasza i Książęca',
        'SV': 'Salwador',
        'SY': 'Syria',
        'SZ': 'Suazi',
        'TC': 'Wyspy Turks i Caicos',
        'TD': 'Czad',
        'TF': 'Francuskie Terytoria Południowe',
        'TG': 'Togo',
        'TH': 'Tajlandia',
        'TJ': 'Tadżykistan',
        'TK': 'Tokelau',
        'TL': 'Timor Wschodni',
        'TM': 'Turkmenistan',
        'TN': 'Tunezja',
        'TO': 'Tonga',
        'TR': 'Turcja',
        'TT': 'Trynidad i Tobago',
        'TV': 'Tuvalu',
        'TW': 'Tajwan',
        'TZ': 'Tanzania',
        'UA': 'Ukraina',
        'UG': 'Uganda',
        'UK': 'Wielka Brytania',
        'UM': 'Dalekie Wyspy Mniejsze Stanów Zjednoczonych',
        'US': 'Stany Zjednoczone',
        'UY': 'Urugwaj',
        'UZ': 'Uzbekistan',
        'VA': 'Watykan',
        'VC': 'Saint Vincent i Grenadyny',
        'VE': 'Wenezuela',
        'VG': 'Brytyjskie Wyspy Dziewicze',
        'VI': 'Wyspy Dziewicze Stanów Zjednoczonych',
        'VN': 'Wietnam',
        'VU': 'Vanuatu',
        'WF': 'Wallis i Futuna',
        'WS': 'Samoa',
        'YE': 'Jemen',
        'YT': 'Majotta',
        'YU': 'Jugosławia',
        'ZA': 'Republika Południowej Afryki',
        'ZM': 'Zambia',
        'ZW': 'Zimbabwe',
    }
    
    return nazwy[skrot.upper()]

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
