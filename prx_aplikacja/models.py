from django.db import models

class BramkaProxy(models.Model):
    # URL bramki
    adres = models.URLField(max_length=255)

    # kanoniczna postać adresu - do rozpoznawania duplikatów 
    adres_k = models.CharField(max_length=255)
    
    # dwuliterowe oznaczenie kraju
    kraj = models.CharField(max_length=2)
    
    # adres IP
    ip = models.GenericIPAddressField(protocol='IPv4')

    # która z kolei na IP
    ip_indeks = models.PositiveIntegerField(null=True)
    
    # ile razem na tym samym IP
    ip_liczba = models.PositiveIntegerField()
    
    # czas odpowiedzi na połączenie TCP
    ping = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    
    # data ostatniego sprawdzenia połączenia z IP
    ost_spr_ip = models.DateTimeField()
    
    # data ostatniego sprawdzenia czasu odpowiedzi
    ost_spr_ping = models.DateTimeField()
    
    # ile razy wystąpił błąd połączenia TCP/IP
    ip_blad = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'bramki_proxy'
