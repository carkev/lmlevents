from django import forms
from django.forms.models import inlineformset_factory
from .models import News, Module


ModuleFormSet = inlineformset_factory(News,
                                      Module,
                                      fields=['title',
                                              'description'],
                                      extra=2,
                                      can_delete=True)
