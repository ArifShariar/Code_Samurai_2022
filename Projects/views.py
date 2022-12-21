# Create your views here.
import csv
import random
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from Projects.models import Project, Feedback

from Constraints.models import Constraints
from Components.models import Components

from itertools import chain
from datetime import date, datetime, timedelta
from geopy import distance

# Create your views here.
import csv
import random
import base64
import json
import math


from Users.models import Profile


def isclose(proposal, project):
    d = distance.distance((proposal.latitude, proposal.longitude), (project.latitude, project.longitude)).meters
    return True


def getExpectedDaysToFinish(project, start_date):
    components = Components.objects.filter(project_id=project.project_id)
    total_component_count = len(components)

    remaining_days = float(project.timespan)*365
    exec_limits = Constraints.objects.filter(code=project.exec_by, constraint_type='executing_agency_limit')
    location_limits = Constraints.objects.filter(code=project.location, constraint_type='location_limit')
    mn_exec = math.inf
    mn_loc = math.inf
    if exec_limits:
        mn_exec = exec_limits.order_by('max_limit').first().max_limit
    if location_limits:
        mn_loc = location_limits.order_by('max_limit').first().max_limit
    active_component_count = min(mn_exec, mn_loc, total_component_count) 
    # if daily we could run total_component_count=n components, days to finish = remaining day
    # if daily we could run active_component_count=m components, days to finish = remaining day/n * m
    if total_component_count == 0:
        return remaining_days

    expected_days_to_finish = active_component_count*remaining_days/total_component_count
    dependent_count = len(components.filter(depends_on__isnull=False))
    expected_days_to_finish += dependent_count*project.timespan*365/total_component_count
    return expected_days_to_finish


def simulate(proposal):
    projects = Project.objects.all().filter(is_proposal=False).order_by('start_date')
    min_expected_days_to_finish = math.inf
    
    for project in projects:
        if not isclose(proposal, project):
            continue
        
        start_date = project.start_date
        percent_completed = project.completion
        days_passed = (date.today() - start_date).days
        if days_passed <= 0 or percent_completed == 0:
            continue

        components = Components.objects.filter(project_id=project.project_id)
        total_component_count = len(components)

        remaining_days = (100-percent_completed)*days_passed/percent_completed
        exec_limits = Constraints.objects.filter(code=project.exec_by, constraint_type='executing_agency_limit')
        location_limits = Constraints.objects.filter(code=project.location, constraint_type='location_limit')
        mn_exec = math.inf
        mn_loc = math.inf
        if exec_limits:
            mn_exec = exec_limits.order_by('max_limit').first().max_limit
        if location_limits:
            mn_loc = location_limits.order_by('max_limit').first().max_limit
        active_component_count = min(mn_exec, mn_loc, total_component_count) 

        # if daily we could run total_component_count=n components, days to finish = remaining day
        # if daily we could run active_component_count=m components, days to finish = remaining day/n * m
        expected_days_to_finish = active_component_count*remaining_days/total_component_count
        dependent_count = len(components.filter(depends_on__isnull=False))
        expected_days_to_finish += dependent_count*project.timespan*365/total_component_count
        min_expected_days_to_finish = min(min_expected_days_to_finish, expected_days_to_finish)
    
    expected_start_date = date.today() + timedelta(days=min_expected_days_to_finish)
    print('expected_start_date = ' + str(expected_start_date))
    days_to_finish = getExpectedDaysToFinish(proposal, expected_start_date)
    expected_end_date = expected_start_date + timedelta(days=days_to_finish) 
    print('expected_end_date = ' + str(expected_end_date))


def show_project_list(request):
    return render(request, 'projects/show_project_list.html')


@login_required(login_url='login_user')
def show_project_details(request, pk):
    project_object = Project.objects.get(pk=pk)
    feedbacks = Feedback.objects.filter(project=project_object)
    profile = Profile.objects.get(user=request.user)
    my_feedback = Feedback.objects.filter(project=project_object, created_by=request.user)
    context = {'project_object': project_object, 'feedbacks': feedbacks, 'profile': profile, 'my_feedback': my_feedback}
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

        # simulate to predict this timeframe
        simulate(project_object)

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
                'Project ID': project.project_id,
                'Name': project.name,
                'Location': project.location,
                'Exec': project.exec_by,
                'Latitude': project.latitude,
                'Longitude': project.longitude,
                'Cost': project.cost,
                'Timespan': project.timespan,
                'Goal': project.goal,
                'Start Date': project.start_date,
                'Completion': project.completion,
                'Actual Cost': project.actual_cost,
                'Is Proposal': project.is_proposal,
                'Proposal Date': project.proposal_date
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


@login_required(login_url='login_user')
def own_projects(request):
    user = Profile.objects.get(user=request.user)
    if user.user_type == "MOP" or user.user_type == "ECNEC":
        own_proposal_list = Project.objects.filter(created_by=request.user)
        own_project_list = Project.objects.filter(created_by=request.user, is_proposal=False)
        print(own_proposal_list)
        print(own_project_list)
        context = {'own_project_list': own_project_list, 'own_proposal_list': own_proposal_list}
        return render(request, 'projects/show_project_list.html', context)
    else:
        print("You are not authorized to view this page")
        return redirect('home')


@login_required(login_url='login_user')
def edit_project_details(request, pk):
    user = Profile.objects.get(user=request.user)
    if user.user_type == "MOP" or user.user_type == "ECNEC":
        project_object = Project.objects.get(pk=pk)
        return render(request, 'projects/edit_project_details.html', {'project_object': project_object})

    else:
        print("You are not authorized to view this page")
        return redirect('home')


@login_required(login_url='login_user')
def update_project_details(request, pk):
    user = Profile.objects.get(user=request.user)
    if user.user_type == "MOP" or user.user_type == "ECNEC":
        project_object = Project.objects.get(pk=pk)
        print(request.POST.get('location'))

        if request.POST.get('name'):
            project_object.name = request.POST.get('name')
        if request.POST.get('location'):
            project_object.location = request.POST.get('location')
            print("changed location")
        if request.POST.get('latitude'):
            project_object.latitude = request.POST.get('latitude')
        if request.POST.get('longitude'):
            project_object.longitude = request.POST.get('longitude')
        if request.POST.get('cost'):
            project_object.cost = request.POST.get('cost')
        if request.POST.get('timespan'):
            project_object.timespan = request.POST.get('timespan')
        if request.POST.get('goal'):
            project_object.goal = request.POST.get('goal')
        if request.POST.get('start_date'):
            project_object.start_date = request.POST.get('start_date')
        if request.POST.get('completion'):
            project_object.completion = request.POST.get('completion')
        if request.POST.get('actual_cost'):
            project_object.actual_cost = request.POST.get('actual_cost')
        project_object.save()
        print("saved")
        return redirect('own_projects')
    else:
        print("You are not authorized to view this page")
        return redirect('home')


@login_required(login_url='login_user')
def sort_by_rating(request):
    user = Profile.objects.get(user=request.user)
    if user.user_type != "APP":
        # sort using Feedback model
        feedback_list = Feedback.objects.order_by('-rating')
        res_list = []
        for feedback in feedback_list:
            res_list.append(feedback.project)

        context = {'project_list': res_list}
        return render(request, 'projects/sorted_project_list.html', context)
    else:
        print("You are not authorized to view this page")
        return redirect('home')
