from django.apps import AppConfig
from django.db import connection

from CsvParser.utils import parseCsv, AGENCIES


class AgenciesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Agencies'

    def ready(self) -> None:
        from .models import Agencies
        print("---------------------------------> loading agency ...")
        all_tables = connection.introspection.table_names()
        if 'Agencies_agencies' not in all_tables:
            print("---------------------------------> loading agency ...")
            return

        agencies = parseCsv(AGENCIES)
        for agency in agencies:
            try:
                ag = Agencies.objects.get(code=agency['code'])
            except Agencies.DoesNotExist:
                agencyObject = Agencies.objects.create(
                    code = agency['code'],
                    name = agency['name'],
                    type = agency['type'],
                    description = agency['description']
                )
                agencyObject.save()
        
        print("---------------------------------> done ...")
        return super().ready()


    def __str__(self):
        return self.name