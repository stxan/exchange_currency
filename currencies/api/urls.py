from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.viewHomePage, name='home_page'),
    path('rates/', views.convertCurrency, name='convert_currency')
]