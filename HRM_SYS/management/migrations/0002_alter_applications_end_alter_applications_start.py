# Generated by Django 4.1.6 on 2023-10-09 05:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applications',
            name='end',
            field=models.DateField(default=datetime.datetime(2023, 10, 9, 8, 12, 5, 382688)),
        ),
        migrations.AlterField(
            model_name='applications',
            name='start',
            field=models.DateField(default=datetime.datetime(2023, 10, 9, 8, 12, 5, 382688)),
        ),
    ]
