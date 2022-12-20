# Repository for Code Samurai 2022 Hackathon

# Loading into database when server starts
```python
from django.db import connection

class MyAppConfig(AppConfig):
    default_auto_field = '...'
    name = 'MyApp'

    def ready(self) -> None:
        from .models import MyApp

        all_tables = connection.introspection.table_names()
        if 'MyApp_myApp' not in all_tables:
            return
        # code here
```

# List of csv files
- agencies
    - code
    - name
    - type
    - description

- components
    - project_id
    - executing_agency
    - component_id
    - component_type

- constraints
    - latitude
    - longitude
    - max_projects

- projects
    - name
    - location
    - latitude
    - longitude
    - exec
    - cost
    - timespan
    - project_id
    - goal
    - start_date
    - completion
    - actual_cost

- proposals
    - name
    - location
    - latitude
    - longitude
    - exec
    - cost
    - timespan
    - project_id
    - goal
    - proposal_date

- user_types
    - code
    - committee
    - description