from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('store/', views.store, name='store'),
    path('checkout/', views.checkout, name='checkout'),
]
