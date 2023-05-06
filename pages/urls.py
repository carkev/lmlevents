"""Pages routing module.
"""
from django.urls import path
from .views import (HomePageView, CGUPageView, PartnersPageView, CGVPageView,
                    LegalNoticesView, AboutPageView, GPDRPageView)

app_name = 'home'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('cgu/', CGUPageView.as_view(), name='cgu'),
    path('cgv/', CGVPageView.as_view(), name='cgv'),
    path('rgpd/', GPDRPageView.as_view(), name='rgpd'),
    path('partenaires/', PartnersPageView.as_view(), name='partners'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('mentions-legales/', LegalNoticesView.as_view(), name='mentions'),
]
