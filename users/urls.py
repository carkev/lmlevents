from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = "users"

urlpatterns = [
    path('register/',
        views.UserRegistrationView.as_view(),
        name='user_registration'),
    path('news/',
        views.UserNewsListView.as_view(),
        name='user_news_list'),
    path('news/<pk>/',
        cache_page(60 * 15)(views.UserNewsDetailView.as_view()),
        name='user_news_detail'),
    path('news/<pk>/<module_id>/',
        cache_page(60 * 15)(views.UserNewsDetailView.as_view()),
        name='user_news_detail_module'),
]
