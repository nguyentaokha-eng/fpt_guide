from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('experience/<slug:slug>/', views.experience_detail, name='experience'),
    path('explore/', views.explore, name='explore'),
    path('afford/', views.afford, name='afford'),
    path('families/', views.families, name='families'),
    path('rate-lecture/', views.rate_lecture, name='rate_lecture'),
    path('rate/', views.rate_lecture, name='rate_lecture_alias'),
    path('lecturer/<str:lecturer_id>/', views.lecturer_detail, name='lecturer_detail'),
    path('student_life/', views.student_life, name='student_life'),
    path('curriculum/', views.curriculum, name='curriculum'),
    #url mo rong cua afford
    path('Afford/food/', views.Afford_food, name='Afford_food'),
    path('Afford/living/', views.Afford_living, name='Afford_living'),
    path('afford/job/', views.Afford_job, name='Afford_job'),
]
