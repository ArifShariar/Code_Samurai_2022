from django.shortcuts import render

from Projects.models import Project


# Create your views here.


def show_project_list(request):
    return render(request, 'projects/show_project_list.html')


def show_project_details(request, pk):
    project_object = Project.objects.get(pk=pk)
    context = {'project_object': project_object}
    return render(request, 'projects/show_project_details.html', context)
