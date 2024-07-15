from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('search/', views.search_view, name='search'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('aesthetic/<str:aesthetic>/', views.apparel_set_view, name='apparel_set'),
    path('item/<str:item_name>/', views.darkacademia, name='dark-academia'),
]