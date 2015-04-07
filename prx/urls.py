from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from .settings import BASE_DIR
import glob
import re

urlpatterns = [
    # Examples:
    # url(r'^$', 'prx.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^', include('prx_aplikacja.urls')),
]

# udostępnianie wszystkich plików z folderu static
# np. URL /style.css -> plik prx_aplikacja/static/style.css
folder = 'prx_aplikacja/static'
sciezka = BASE_DIR + '/' + folder
for plik in glob.glob(sciezka + '/*'):
    # względem folderu static, a nie bezwzględne
    plik = plik[len(sciezka) + 1:]
    
    urlpatterns.append(
        url(
            r'^(?P<path>' + re.escape(plik) + ')$',
            'django.views.static.serve',
            {'document_root': folder}
        )
    )
