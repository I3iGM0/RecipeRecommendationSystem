from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='healthyliving-home'),
    path('about/', views.about, name='healthyliving-about'),
    path('fitbit/', views.fitbit, name='fitbit'),
    path('fitbit1/', views.fitbit1, name='fitbit1'),
    path('fitbit2/', views.fitbit2, name='fitbit2'),
]
