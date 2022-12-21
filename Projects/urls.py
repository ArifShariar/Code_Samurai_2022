from django.urls import path, include
from .views import *

urlpatterns = [
    path('show_project_list/', show_project_list, name='show_project_list'),
    path('show_project_details/<int:pk>/', show_project_details, name='show_project_details'),
    path('search_projects/', search_projects, name='search_projects'),
    path('search_projects_results/', search_project_result, name='search_projects_results'),
    path('download/', download, name='download'),

    path('dpp_form/', dpp_form, name='dpp_form'),
    path('feedback_form/<int:pk>/', feedback_form, name='feedback_form'),

    path('view_proposed_projects/', view_proposed_projects, name='view_proposed_projects'),
    path('view_proposed_projects_details/<int:pk>/', view_proposed_project_details,
         name='view_proposed_projects_details'),
    path('approve_proposed_project/<int:pk>/', approve_proposed_project, name='approve_proposed_project'),
    path('reject_proposed_project/<int:pk>/', reject_proposed_project, name='reject_proposed_project'),

    path('own_projects/', own_projects, name='own_projects'),
    path('edit_project_details/<int:pk>/', edit_project_details, name='edit_project_details'),
    path('update_project_details/<int:pk>/', update_project_details, name='update_project_details'),

    path('sorted_list/', sort_by_rating, name='sorted_list'),
]
