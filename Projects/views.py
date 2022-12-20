from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.shortcuts import render
from django.core.files.base import ContentFile

from django.shortcuts import render, redirect


from Projects.models import Project, Feedback

from itertools import chain

# Create your views here.
import csv
import random
import base64
import json
import datetime

from Users.models import Profile


def show_project_list(request):
    return render(request, 'projects/show_project_list.html')


@login_required(login_url='login_user')
def show_project_details(request, pk):
    project_object = Project.objects.get(pk=pk)
    feedbacks = Feedback.objects.filter(project=project_object)
    print(feedbacks)
    context = {'project_object': project_object, 'feedbacks': feedbacks}
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
        lst_of_dick = []
        
        for project in result_list:
            lst_of_dick.append({
                'Project ID'    : project.project_id, 
                'Name'          : project.name, 
                'Location'      : project.location, 
                'Exec'          : project.exec_by, 
                'Latitude'      : project.latitude,
                'Longitude'     : project.longitude,
                'Cost'          : project.cost, 
                'Timespan'      : project.timespan, 
                'Goal'          : project.goal, 
                'Start Date'    : project.start_date, 
                'Completion'    : project.completion,
                'Actual Cost'   : project.actual_cost, 
                'Is Proposal'   : project.is_proposal, 
                'Proposal Date' : project.proposal_date
            })

        context = {'result_list': result_list}
        request.session['result_list'] = str(lst_of_dick)
        return render(request, 'projects/search_project_result.html', context)



@login_required(login_url='login_user')
def download(request):
    result_project_list = request.session['result_list']
    result_project_list = list(eval(result_project_list))
    print(result_project_list)
    print(type(result_project_list))
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow([
        'Project ID', 
        'Name', 
        'Location', 
        'Exec', 
        'Latitude', 
        'Longitude', 
        'Cost', 
        'Timespan', 
        'Goal',
        'Start Date', 
        'Completion', 
        'Actual Cost', 
        'Is Proposal', 
        'Proposal Date'
    ])
    for project in result_project_list:
        writer.writerow([
            project['Project ID'], 
            project['Name'], 
            project['Location'], 
            project['Exec'], 
            project['Latitude'],
            project['Longitude'],
            project['Cost'], 
            project['Timespan'], 
            project['Goal'], 
            project['Start Date'], 
            project['Completion'],
            project['Actual Cost'], 
            project['Is Proposal'], 
            project['Proposal Date']
        ])

    del request.session['result_list']
    return response



@login_required(login_url='login_user')
def feedback_form(request, pk):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        rating = request.POST.get('rate')
        user_id = request.user
        project_object = Project.objects.get(pk=pk)
        feedback_object = Feedback.objects.create(
            feedback=feedback,
            rating=rating,
            project=project_object,
            created_by=user_id,
        )
        feedback_object.save()
        return redirect('show_project_details', pk=pk)

    return redirect('show_project_details', pk=pk)


@login_required(login_url='login_user')
def view_proposed_projects(request):
    user = Profile.objects.get(user=request.user)
    if user.user_type == "MOP":
        proposed_projects = Project.objects.filter(is_proposal=True, cost__lte=50)
        print(proposed_projects)
        context = {'proposed_projects': proposed_projects}
        return render(request, 'projects/proposed_projects.html', context)
    elif user.user_type == "ECNEC":
        proposed_projects = Project.objects.filter(is_proposal=True, cost__gt=50)
        print(proposed_projects)
        context = {'proposed_projects': proposed_projects}
        return render(request, 'projects/proposed_projects.html', context)
    else:
        print("You are not authorized to view this page")
        return redirect('home')


@login_required(login_url='login_user')
def view_proposed_project_details(request, pk):
    user = Profile.objects.get(user=request.user)
    if user.user_type == "MOP" or user.user_type == "ECNEC":
        project_object = Project.objects.get(pk=pk)
        context = {'project_object': project_object}
        return render(request, 'projects/proposed_project_details.html', context)
    else:
        print("You are not authorized to view this page")
        return redirect('home')


@login_required(login_url='login_user')
def approve_proposed_project(request, pk):
    user = Profile.objects.get(user=request.user)
    if user.user_type == "MOP" or user.user_type == "ECNEC":
        project_object = Project.objects.get(pk=pk)
        project_object.is_proposal = False
        project_id = project_object.project_id
        # remove prop from first portion of project id
        project_id = project_id[4:]
        # add proj to first portion of project id
        project_id = f"proj{project_id}"
        # check if the project id already exists in Project model
        while Project.objects.filter(project_id=project_id).exists():
            random_n = random.randint(1000, 9999)
            project_id = f"proj{random_n}"
        project_object.save()
        return redirect('view_proposed_projects')
    else:
        print("You are not authorized to view this page")
        return redirect('home')


@login_required(login_url='login_user')
def reject_proposed_project(request, pk):
    user = Profile.objects.get(user=request.user)
    if user.user_type == "MOP" or user.user_type == "ECNEC":
        project_object = Project.objects.get(pk=pk)
        project_object.delete()
        return redirect('view_proposed_projects')
    else:
        print("You are not authorized to view this page")
        return redirect('home')

