# Generated by Django 4.2.7 on 2023-11-04 10:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrapayments',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 4, 13, 15, 41, 592617)),
        ),
    ]
