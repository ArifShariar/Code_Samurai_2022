from django.urls import path, include
from .views import *
urlpatterns = [
    path('', default_home, name='default_home'),
    path('home/', home, name='home'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('unverified_user/', get_all_unverified_users, name='unverified_user'),
    path('approve_user/<int:pk>/', approve_user, name='approve_user'),
    path('decline_user/<int:pk>/', decline_user, name='decline_user'),
]
