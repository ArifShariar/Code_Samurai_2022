from django.shortcuts import render
from Projects.views import simulate
from Projects.models import Project


# Create your views here.

def get_proposals(request):
    proposal_list = Project.objects.get(is_proposal=True)
    count = {}
    for proposal in proposal_list:
        start, end = simulate(proposal)
        start = start.year
        end = end.year

    return render(request, 'Charts/charts_show.html')