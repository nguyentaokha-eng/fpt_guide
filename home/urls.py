from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('experience/<slug:slug>/', views.experience_detail, name='experience'),
    path('explore/', views.explore, name='explore'),
    path('afford/', views.afford, name='afford'),
    path('families/', views.families, name='families'),
]
