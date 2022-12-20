from django.apps import AppConfig
from django.utils.dateparse import parse_date
from django.db import connection

from CsvParser.utils import parseCsv, PROJECTS


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Projects'

    def ready(self) -> None:
        from .models import Project
        
        all_tables = connection.introspection.table_names()
        print(all_tables)
        if 'Projects_project' not in all_tables:
            print('------------------->no tables found. Returning from ready()')
            return

        print("------------------------------------------------>Project loading")
        projects = parseCsv(PROJECTS)
        for project in projects:
            projectObject = Project.objects.create(
                project_id=project['project_id'],
                exec_by=project['exec'],
                name=project['name'],
                location=project['location'],
                latitude=project['latitude'],
                longitude=project['longitude'],
                cost=project['cost'],
                timespan=project['timespan'],
                goal=project['goal'],
                start_date=parse_date(project['start_date']),
                completion=project['completion'],
                actual_cost=project['actual_cost'],
                is_proposal=False,
                proposal_date=None
            )
            projectObject.save()            

        return super().ready()
