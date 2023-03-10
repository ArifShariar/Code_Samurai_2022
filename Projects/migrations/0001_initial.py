# Generated by Django 4.1.4 on 2022-12-20 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='UserFK', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
