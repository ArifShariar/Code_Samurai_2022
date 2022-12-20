from django.apps import AppConfig
from django.db import connection

from CsvParser.utils import parseCsv, COMPONENTS

class ComponentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Components'

    def ready(self) -> None:
        from .models import Components

        print("-------------------------------------->loading components ...")

        all_tables = connection.introspection.table_names()
        if 'Components_components' not in all_tables:
            print("-------------------------------------->done ...")
            return

        components = parseCsv(COMPONENTS)
        for component in components:
            try:
                c = Components.objects.get(component_id=component['component_id'])
            except Components.DoesNotExist:
                componentObject = Components.objects.create(
                    component_id        = component['component_id'],
                    project_id          = component['project_id'],
                    executing_agency    = component['executing_agency'],
                    component_type      = component['component_type'],
                    depends_on          = component['depends_on'],
                    budget_ratio        = float(component['budget ratio'])
                ).save()

        print("-------------------------------------->done")
        return super().ready()
