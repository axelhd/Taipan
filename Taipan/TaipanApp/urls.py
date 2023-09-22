from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get/<int:id>', views.get, name='get'),
    path('set', views.set, name='set'),
    path('out/<int:id>', views.out, name='out'),
]