import timeit
import socket
import urllib.parse
import re

def ping(ip, port):
    pingi = []

    for i in range(2):
        try:
            czas_poczatkowy = timeit.default_timer()
            gniazdo = socket.create_connection((ip, port), 5)
            czas_koncowy = timeit.default_timer()

            gniazdo.close
            pingi.append((czas_koncowy - czas_poczatkowy) * 1000);
        except OSError:
            pass

    if len(pingi) > 0:
        return min(pingi)
    else:
        return None

def kraj_ip(ip):
    odwrotny_ip = '.'.join(reversed(ip.split('.')))

    try:
        kody_liczbowe = socket.gethostbyname_ex(odwrotny_ip + '.zz.countries.nerd.dk')[2]
    except socket.gaierror:
        return ''

    if len(kody_liczbowe) == 0:
        return ''

    if '127.0.2.104' in kody_liczbowe:
        return 'PL'

    wszystkie_kody_liczbowe = {
        '127.0.0.20': 'AD',
        '127.0.3.16': 'AE',
        '127.0.0.4': 'AF',
        '127.0.0.28': 'AG',
        '127.0.2.148': 'AI',
        '127.0.0.8': 'AL',
        '127.0.0.51': 'AM',
        '127.0.2.18': 'AN',
        '127.0.0.24': 'AO',
        '127.0.0.10': 'AQ',
        '127.0.0.32': 'AR',
        '127.0.0.16': 'AS',
        '127.0.0.40': 'AT',
        '127.0.0.36': 'AU',
        '127.0.2.21': 'AW',
        '127.0.0.31': 'AZ',
        '127.0.0.70': 'BA',
        '127.0.0.52': 'BB',
        '127.0.0.50': 'BD',
        '127.0.0.56': 'BE',
        '127.0.3.86': 'BF',
        '127.0.0.100': 'BG',
        '127.0.0.48': 'BH',
        '127.0.0.108': 'BI',
        '127.0.0.204': 'BJ',
        '127.0.0.60': 'BM',
        '127.0.0.96': 'BN',
        '127.0.0.68': 'BO',
        '127.0.0.76': 'BR',
        '127.0.0.44': 'BS',
        '127.0.0.64': 'BT',
        '127.0.0.74': 'BV',
        '127.0.0.72': 'BW',
        '127.0.0.112': 'BY',
        '127.0.0.84': 'BZ',
        '127.0.0.124': 'CA',
        '127.0.0.166': 'CC',
        '127.0.0.140': 'CF',
        '127.0.0.178': 'CG',
        '127.0.2.244': 'CH',
        '127.0.1.128': 'CI',
        '127.0.0.184': 'CK',
        '127.0.0.152': 'CL',
        '127.0.0.120': 'CM',
        '127.0.0.156': 'CN',
        '127.0.0.170': 'CO',
        '127.0.0.188': 'CR',
        '127.0.0.192': 'CU',
        '127.0.0.132': 'CV',
        '127.0.0.162': 'CX',
        '127.0.0.196': 'CY',
        '127.0.0.203': 'CZ',
        '127.0.1.20': 'DE',
        '127.0.1.6': 'DJ',
        '127.0.0.208': 'DK',
        '127.0.0.212': 'DM',
        '127.0.0.214': 'DO',
        '127.0.0.12': 'DZ',
        '127.0.0.218': 'EC',
        '127.0.0.233': 'EE',
        '127.0.3.50': 'EG',
        '127.0.2.220': 'EH',
        '127.0.0.232': 'ER',
        '127.0.2.212': 'ES',
        '127.0.0.231': 'ET',
        '127.0.0.246': 'FI',
        '127.0.0.242': 'FJ',
        '127.0.0.238': 'FK',
        '127.0.2.71': 'FM',
        '127.0.0.234': 'FO',
        '127.0.0.250': 'FR',
        '127.0.0.249': 'FX',
        '127.0.1.10': 'GA',
        '127.0.3.58': 'UK',
        '127.0.1.52': 'GD',
        '127.0.1.12': 'GE',
        '127.0.0.254': 'GF',
        '127.0.1.32': 'GH',
        '127.0.1.36': 'GI',
        '127.0.1.48': 'GL',
        '127.0.1.14': 'GM',
        '127.0.1.68': 'GN',
        '127.0.1.56': 'GP',
        '127.0.0.226': 'GQ',
        '127.0.1.44': 'GR',
        '127.0.0.239': 'GS',
        '127.0.1.64': 'GT',
        '127.0.1.60': 'GU',
        '127.0.2.112': 'GW',
        '127.0.1.72': 'GY',
        '127.0.1.88': 'HK',
        '127.0.1.78': 'HM',
        '127.0.1.84': 'HN',
        '127.0.0.191': 'HR',
        '127.0.1.76': 'HT',
        '127.0.1.92': 'HU',
        '127.0.1.104': 'ID',
        '127.0.1.116': 'IE',
        '127.0.1.120': 'IL',
        '127.0.1.100': 'IN',
        '127.0.0.86': 'IO',
        '127.0.1.112': 'IQ',
        '127.0.1.108': 'IR',
        '127.0.1.96': 'IS',
        '127.0.1.124': 'IT',
        '127.0.1.132': 'JM',
        '127.0.1.144': 'JO',
        '127.0.1.136': 'JP',
        '127.0.1.148': 'KE',
        '127.0.1.161': 'KG',
        '127.0.0.116': 'KH',
        '127.0.1.40': 'KI',
        '127.0.0.174': 'KM',
        '127.0.2.147': 'KN',
        '127.0.1.152': 'KP',
        '127.0.1.154': 'KR',
        '127.0.1.158': 'KW',
        '127.0.0.136': 'KY',
        '127.0.1.142': 'KZ',
        '127.0.1.162': 'LA',
        '127.0.1.166': 'LB',
        '127.0.2.150': 'LC',
        '127.0.1.182': 'LI',
        '127.0.0.144': 'LK',
        '127.0.1.174': 'LR',
        '127.0.1.170': 'LS',
        '127.0.1.184': 'LT',
        '127.0.1.186': 'LU',
        '127.0.1.172': 'LV',
        '127.0.1.178': 'LY',
        '127.0.1.248': 'MA',
        '127.0.1.236': 'MC',
        '127.0.1.242': 'MD',
        '127.0.1.194': 'MG',
        '127.0.2.72': 'MH',
        '127.0.3.39': 'MK',
        '127.0.1.210': 'ML',
        '127.0.0.104': 'MM',
        '127.0.1.240': 'MN',
        '127.0.1.190': 'MO',
        '127.0.2.68': 'MP',
        '127.0.1.218': 'MQ',
        '127.0.1.222': 'MR',
        '127.0.1.244': 'MS',
        '127.0.1.214': 'MT',
        '127.0.1.224': 'MU',
        '127.0.1.206': 'MV',
        '127.0.1.198': 'MW',
        '127.0.1.228': 'MX',
        '127.0.1.202': 'MY',
        '127.0.1.252': 'MZ',
        '127.0.2.4': 'NA',
        '127.0.2.28': 'NC',
        '127.0.2.50': 'NE',
        '127.0.2.62': 'NF',
        '127.0.2.54': 'NG',
        '127.0.2.46': 'NI',
        '127.0.2.16': 'NL',
        '127.0.2.66': 'NO',
        '127.0.2.12': 'NP',
        '127.0.2.8': 'NR',
        '127.0.2.58': 'NU',
        '127.0.2.42': 'NZ',
        '127.0.2.0': 'OM',
        '127.0.2.79': 'PA',
        '127.0.2.92': 'PE',
        '127.0.1.2': 'PF',
        '127.0.2.86': 'PG',
        '127.0.2.96': 'PH',
        '127.0.2.74': 'PK',
        '127.0.2.104': 'PL',
        '127.0.2.154': 'PM',
        '127.0.2.100': 'PN',
        '127.0.2.118': 'PR',
        '127.0.2.108': 'PT',
        '127.0.2.73': 'PW',
        '127.0.2.88': 'PY',
        '127.0.2.122': 'QA',
        '127.0.2.126': 'RE',
        '127.0.2.130': 'RO',
        '127.0.2.131': 'RU',
        '127.0.2.134': 'RW',
        '127.0.2.170': 'SA',
        '127.0.0.90': 'SB',
        '127.0.2.178': 'SC',
        '127.0.2.224': 'SD',
        '127.0.2.240': 'SE',
        '127.0.2.190': 'SG',
        '127.0.2.142': 'SH',
        '127.0.2.193': 'SI',
        '127.0.2.232': 'SJ',
        '127.0.2.191': 'SK',
        '127.0.2.182': 'SL',
        '127.0.2.162': 'SM',
        '127.0.2.174': 'SN',
        '127.0.2.194': 'SO',
        '127.0.2.228': 'SR',
        '127.0.2.166': 'ST',
        '127.0.0.222': 'SV',
        '127.0.2.248': 'SY',
        '127.0.2.236': 'SZ',
        '127.0.3.28': 'TC',
        '127.0.0.148': 'TD',
        '127.0.1.4': 'TF',
        '127.0.3.0': 'TG',
        '127.0.2.252': 'TH',
        '127.0.2.250': 'TJ',
        '127.0.3.4': 'TK',
        '127.0.3.27': 'TM',
        '127.0.3.20': 'TN',
        '127.0.3.8': 'TO',
        '127.0.2.114': 'TL',
        '127.0.3.24': 'TR',
        '127.0.3.12': 'TT',
        '127.0.3.30': 'TV',
        '127.0.0.158': 'TW',
        '127.0.3.66': 'TZ',
        '127.0.3.36': 'UA',
        '127.0.3.32': 'UG',
        '127.0.3.58': 'UK',
        '127.0.2.69': 'UM',
        '127.0.3.72': 'US',
        '127.0.3.90': 'UY',
        '127.0.3.92': 'UZ',
        '127.0.1.80': 'VA',
        '127.0.2.158': 'VC',
        '127.0.3.94': 'VE',
        '127.0.0.92': 'VG',
        '127.0.3.82': 'VI',
        '127.0.2.192': 'VN',
        '127.0.2.36': 'VU',
        '127.0.3.108': 'WF',
        '127.0.3.114': 'WS',
        '127.0.3.119': 'YE',
        '127.0.0.175': 'YT',
        '127.0.3.123': 'YU',
        '127.0.2.198': 'ZA',
        '127.0.3.126': 'ZM',
        '127.0.0.180': 'CD',
        '127.0.2.204': 'ZW',
    }

    kod = kody_liczbowe[0]
    if kod in wszystkie_kody_liczbowe:
        return wszystkie_kody_liczbowe[kod]
    else:
        return ''

# kanoniczny adres, do rozpoznawania duplikatów
def adres_k(adres):
    adres = urllib.parse.urlparse(adres)
    if adres.scheme == '' or adres.hostname in [None, '']:
        return None

    host = adres.hostname
    sciezka = adres.path

    host = re.sub(r'^www\.|\.$', '', host, flags=re.IGNORECASE)
    if sciezka in [None, '']:
       sciezka = '/'
    
    return host + sciezka
