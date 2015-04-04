from django.apps import AppConfig
from django.template.base import add_to_builtins

class PrxAppConfig(AppConfig):
    name = 'prx_aplikacja'
    verbose_name = 'prx_aplikacja'

    def ready(self):
        add_to_builtins('prx_aplikacja.templatetags.tagi')
