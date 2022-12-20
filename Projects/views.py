from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from Projects.models import Project

from itertools import chain

# Create your views here.


def show_project_list(request):
    return render(request, 'projects/show_project_list.html')


def show_project_details(request, pk):
    project_object = Project.objects.get(pk=pk)
    context = {'project_object': project_object}
    return render(request, 'projects/show_project_details.html', context)


@login_required(login_url='login_user')
def search_projects(request):
    return render(request, 'projects/search_project.html')


@ login_required(login_url='login_user')
def search_project_result(request):
    context = dict()
    if request.method == "POST":
        search_text = request.POST.get('search-input')
        result1 = Project.objects.filter(name__contains=search_text)
        result2 = Project.objects.filter(location__contains=search_text)
        result_list = list(chain(result1, result2))
        context = {'result_list': result_list}
    return render(request, 'projects/search_project_result.html', context)
