from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('url/', views.url, name='url'),
]