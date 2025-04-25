from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search/', views.search_word, name='search_word'),
    path('save/', views.save_word, name='save_word'),
    path('wordbox/delete/', views.delete_word, name='delete_word'),

    path('list/', views.list_saved_words, name='list_saved_words'),
    path('daily/', views.daily_review, name='daily_review'),
]
