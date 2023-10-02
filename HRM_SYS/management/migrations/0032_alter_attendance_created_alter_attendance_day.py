# Generated by Django 4.1.6 on 2023-10-02 04:06

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0031_employee_kra_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='day',
            field=models.DateField(default=datetime.date(2023, 10, 2)),
        ),
    ]
