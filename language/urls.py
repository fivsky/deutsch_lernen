from django.urls import path
from . import views

app_name = 'language'
urlpatterns = [
    path('', views.word_list, name='word_list'),
    path('trainer/', views.trainer, name='trainer'),
    path('texts/', views.text_list, name='text_list'),
    path('text/<int:pk>/', views.text_detail, name='text_detail'),
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('exercise/<int:pk>/', views.exercise_detail, name='exercise_detail'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
]



