from django.apps import AppConfig
from django.db import connection

from CsvParser.utils import parseCsv, CONSTRAINTS


class ConstraintsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Constraints'


    def ready(self) -> None:
        from .models import Constraints

        print("------------------------------> loading constraints ...")

        all_tables = connection.introspection.table_names()
        if 'Constraints_constraints' not in all_tables:
            print("------------------------------> done")
            return


        constraints = parseCsv(CONSTRAINTS)
        for constraint in constraints:
            code        = constraint['code']
            max_limit   = int(constraint['max_limit'])
            constraint_type = constraint['constraint_type']
            try:
                c = Constraints.objects.get(code=code, max_limit=max_limit, constraint_type=constraint_type)
            except Constraints.DoesNotExist:
                Constraints.objects.create(
                    code        = code,
                    max_limit   = max_limit,
                    constraint_type = constraint_type
                ).save()

        print("----------------------------------> done")
        return super().ready()