from django.urls import path, include
from .views import *
urlpatterns = [
    path('', default_home, name='default_home'),
    path('home/', home, name='home'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
]
