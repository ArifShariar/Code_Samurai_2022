from django.urls import path, include
from .views import *
urlpatterns = [
    path('show_project_list/', show_project_list, name='show_project_list'),
    path('show_project_details/<int:pk>/', show_project_details, name='show_project_details'),
    path('search_projects/', search_projects, name='search_projects'),
    path('search_projects_results/', search_project_result, name='search_projects_results'),
]
