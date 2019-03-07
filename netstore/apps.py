from django.apps import AppConfig
from suit.apps import DjangoSuitConfig
from django.forms import ModelForm


class NetstoreConfig(AppConfig):
    name = 'netstore'

class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'



