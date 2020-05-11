from django.urls import path
from django.conf.urls import url
from .views import PostListView, PostDetailView
from . import views

# Links each URL to a view function
urlpatterns = [
    path('', views.home, name='healthyliving-home'),
    url(r'^recipes/$', PostListView.as_view(), name='healthyliving-recipes'),
    path('recipes/<int:pk>/', views.getRecipe, name='getRecipe'),
    path('recipes/<int:pk>/recentlyVisited', views.recentlyVisited, name='recentlyVisited'),
    path('recipes/<int:pk>/favourites', views.favourites, name='favourites'),
    path('recipes/<int:pk>/rating', views.rating, name='rating'),
    path('healthdata/', views.healthdata, name='healthdata'),
    path('healthdata1/', views.healthdata1, name='healthdata1'),
    path('healthdata2/', views.healthdata2, name='healthdata2'),
    path('test/', views.test, name='test'),

]
