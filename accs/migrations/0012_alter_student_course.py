# Generated by Django 3.2.4 on 2021-06-10 14:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accs', '0011_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(6), django.core.validators.MinValueValidator(1)]),
        ),
    ]
