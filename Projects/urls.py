from django.urls import path, include
from .views import *
urlpatterns = [
    path('show_project_list/', show_project_list, name='show_project_list'),
    path('show_project_details/<int:pk>/', show_project_details, name='show_project_details'),
    path('show_search_page/', search_page, name='search_page'),
    path('show_search_results/', search_projects, name='show_search_results'),
]
