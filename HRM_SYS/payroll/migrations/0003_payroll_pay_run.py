# Generated by Django 4.1.6 on 2023-10-11 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0002_payroll_status_payrollsetting_relief_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payroll',
            name='pay_run',
            field=models.CharField(default='', max_length=200),
        ),
    ]
