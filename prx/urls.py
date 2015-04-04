from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'prx.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^', include('prx_aplikacja.urls')),
]

urlpatterns += static('/', document_root='prx_aplikacja/static')