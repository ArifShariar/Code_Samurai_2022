# Generated by Django 4.1.4 on 2022-12-20 18:03

# Generated by Django 4.1.4 on 2022-12-20 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constraints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('max_limit', models.IntegerField()),
                ('constraint_type', models.CharField(choices=[('executing_agency_limit', 'executive agency limit'), ('location_limit', 'location limit'), ('yearly_funding', 'yearly funding')], max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Constraints',
            },
        ),
    ]
