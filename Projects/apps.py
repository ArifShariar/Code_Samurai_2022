from django.apps import AppConfig
from django.utils.dateparse import parse_date
from django.db import connection

from CsvParser.utils import parseCsv, PROJECTS, PROPOSALS


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Projects'

    def ready(self) -> None:
        from .models import Project
        
        print("------------------------------------------------>Project loading")

        all_tables = connection.introspection.table_names()
        if 'Projects_project' not in all_tables:
            print("------------------------------------------------>Project loading")
            return

        
        projects = parseCsv(PROJECTS)
        for project in projects:
            try:
                p = Project.objects.get(project_id=project['project_id'])
            except Project.DoesNotExist:
                Project.objects.create(
                    project_id  =   project['project_id'],
                    exec_by     =   project['exec'],
                    name        =   project['name'],
                    location    =   project['location'],
                    latitude    =   project['latitude'],
                    longitude   =   project['longitude'],
                    cost        =   project['cost'],
                    timespan    =   project['timespan'],
                    goal        =   project['goal'],
                    start_date  =   parse_date(project['start_date']),
                    completion  =   project['completion'],
                    actual_cost =   project['actual_cost'],
                    is_proposal =   False,
                    proposal_date=  None
                ).save()

        proposals = parseCsv(PROPOSALS)
        for proposal in proposals:
            try:
                p = Project.objects.get(project_id=proposal['project_id'])
            except Project.DoesNotExist:
                Project.objects.create(
                    project_id  =   proposal['project_id'],
                    exec_by     =   proposal['exec'],
                    name        =   proposal['name'],
                    location    =   proposal['location'],
                    latitude    =   proposal['latitude'],
                    longitude   =   proposal['longitude'],
                    cost        =   proposal['cost'],
                    timespan    =   proposal['timespan'],
                    goal        =   proposal['goal'],
                    start_date  =   None,
                    completion  =   None,
                    actual_cost =   None,
                    is_proposal =   True,
                    proposal_date=  proposal['proposal_date']
                ).save()

        print("------------------------------------------------>Project done")
        return super().ready()
