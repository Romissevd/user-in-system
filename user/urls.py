from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('url/<str:uuid>/', views.enter, name='enter'),
    path('url/', views.url, name='url'),
]