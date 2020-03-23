from django.urls import path
from .views import PostListView, PostDetailView
from . import views

urlpatterns = [
    path('', views.home, name='healthyliving-home'),
    path('test/', views.test, name='healthyliving-test'),
    path('recipes/', PostListView.as_view(), name='healthyliving-recipes'),
    path('recipes/<int:pk>/', views.getRecipe, name='getRecipe'),
    path('recipes/<int:pk>/recentlyVisited', views.recentlyVisited, name='recentlyVisited'),
    path('fitbit/', views.fitbit, name='fitbit'),
    path('fitbit1/', views.fitbit1, name='fitbit1'),
    path('fitbit2/', views.fitbit2, name='fitbit2'),
]
