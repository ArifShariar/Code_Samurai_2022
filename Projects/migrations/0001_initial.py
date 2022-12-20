# Generated by Django 4.1.4 on 2022-12-20 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(max_length=255)),
                ('exec_by', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('cost', models.FloatField()),
                ('timespan', models.IntegerField()),
                ('goal', models.TextField(max_length=255, null=True)),
                ('start_date', models.DateField(null=True)),
                ('completion', models.FloatField(null=True)),
                ('actual_cost', models.FloatField(null=True)),
                ('is_proposal', models.BooleanField(default=False)),
                ('proposal_date', models.DateField(null=True)),
            ],
        ),
    ]
