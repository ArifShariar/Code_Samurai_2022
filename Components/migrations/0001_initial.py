from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Components',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component_id', models.CharField(max_length=20)),
                ('project_id', models.CharField(max_length=20)),
                ('executing_agency', models.CharField(max_length=20)),
                ('component_type', models.CharField(max_length=20)),
                ('depends_on', models.CharField(max_length=20, null=True)),
                ('budget_ratio', models.FloatField()),
            ],
        ),
    ]
