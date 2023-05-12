"""Routing module.
"""
from django.urls import path, re_path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('forgotten-password/', views.forgotten_password,
         name='forgotten-password'),
    path('users/email/', views.email, name='email'),
    path('account/', views.account, name='account'),
    re_path(r'^verification/(?P<uidb64>.+)/(?P<token>.+)/$',
            views.verification, name='verification'),
]
