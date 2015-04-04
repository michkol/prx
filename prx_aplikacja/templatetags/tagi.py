from django import template
from django.utils.safestring import mark_safe

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
