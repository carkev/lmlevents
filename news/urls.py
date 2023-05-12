from django.urls import path
from . import views
from users import views as user_view


app_name = "news"

urlpatterns = [
    path('mine/',
         views.ManageNewsListView.as_view(),
         name='manage_news_list'),
    path('create/',
         views.NewsCreateView.as_view(),
         name='news_create'),
    path('<pk>/edit/',
         views.NewsUpdateView.as_view(),
         name='news_edit'),
    path('<pk>/delete/',
         views.NewsDeleteView.as_view(),
         name='news_delete'),
    path('<pk>/module/',
         views.NewsModuleUpdateView.as_view(),
         name='news_module_update'),
    path('module/<int:module_id>/content/<model_name>/create/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_update'),
    path('content/<int:id>/delete/',
         views.ContentDeleteView.as_view(),
         name='module_content_delete'),
    path('module/<int:module_id>/',
         views.ModuleContentListView.as_view(),
         name='module_content_list'),
    path('module/order/',
         views.ModuleOrderView.as_view(),
         name='module_order'),
    path('content/order/',
         views.ContentOrderView.as_view(),
         name='content_order'),
     path('subject/<slug:subject>/',
          views.NewsListView.as_view(),
          name='news_list_subject'),
     path('<slug:slug>/',
          user_view.UserNewsDetailView.as_view(),
          name='news_detail'),
         
]
