from django.shortcuts import render
from .models import BramkaProxy

def index(zadanie):
    kontekst = {
        'lista': BramkaProxy.objects.all()[:80]
    }
    return render(zadanie, 'prx_aplikacja/index.html', kontekst)
