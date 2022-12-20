from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from Projects.models import Project

from itertools import chain

# Create your views here.
import csv
import random

from Users.models import Profile


def show_project_list(request):
    return render(request, 'projects/show_project_list.html')


def show_project_details(request, pk):
    project_object = Project.objects.get(pk=pk)
    context = {'project_object': project_object}
    return render(request, 'projects/show_project_details.html', context)


@login_required(login_url='login_user')
def search_projects(request):
    return render(request, 'projects/search_project.html')


@login_required(login_url='login_user')
def dpp_form(request):
    if request.method == "POST":
        project_name = request.POST.get('name')
        location = request.POST.get('location')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        cost = request.POST.get('cost')
        timespan = request.POST.get('timespan')
        goal = request.POST.get('goal')

        # get a 4 digit random number
        random_n = random.randint(1000, 9999)
        project_id = f"prop{random_n}"

        # check if the project id already exists in Project model
        while Project.objects.filter(project_id=project_id).exists():
            random_n = random.randint(1000, 9999)
            project_id = f"prop{random_n}"
        user_profile = Profile.objects.get(user=request.user)
        # create a new project object
        project_object = Project.objects.create(
            project_id=project_id,
            exec_by=user_profile.user_type,
            name=project_name,
            location=location,
            latitude=latitude,
            longitude=longitude,
            cost=cost,
            timespan=timespan,
            goal=goal,
            is_proposal=True,
            created_by=request.user,
        )
        project_object.save()

        return HttpResponse("OK")
    return render(request, 'projects/dpp_form.html')


@login_required(login_url='login_user')
def search_project_result(request):
    context = dict()
    if request.method == "POST":
        search_text = request.POST.get('search-input')
        result1 = Project.objects.filter(name__contains=search_text)
        result2 = Project.objects.filter(location__contains=search_text)
        result_list = list(chain(result1, result2))

        response = HttpResponse(content_type='text/csv',
                                headers={'Content-Disposition': 'attachment; filename="search_result.csv"'})

        writer = csv.writer(response)
        writer.writerow(['Project ID', 'Name', 'Location', 'Exec', 'Latitude', 'Longitude', 'Cost', 'Timespan', 'Goal',
                         'Start Date', 'Completion', 'Actual Cost', 'Is Proposal', 'Proposal Date'])
        for project in result_list:
            writer.writerow([project.project_id, project.name, project.location, project.exec_by, project.latitude,
                             project.longitude,
                             project.cost, project.timespan, project.goal, project.start_date, project.completion,
                             project.actual_cost, project.is_proposal, project.proposal_date])

        # convert result_list to csv file

        context = {'result_list': result_list, 'csv': response}
    return render(request, 'projects/search_project_result.html', context)
