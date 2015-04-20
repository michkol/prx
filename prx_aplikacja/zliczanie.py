from .models import BramkaProxy

def oblicz_ip_indeks_liczba(ip):
    bramki = list(enumerate(BramkaProxy.objects.filter(ip=ip).order_by('id'), start=1))
    for (numer, bramka) in bramki:
        bramka.ip_indeks = numer
        bramka.ip_liczba = len(bramki)
        bramka.save()
