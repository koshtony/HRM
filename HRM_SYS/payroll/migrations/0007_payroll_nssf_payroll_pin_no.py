# Generated by Django 4.1.6 on 2023-10-01 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0006_payroll_sign_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payroll',
            name='nssf',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='payroll',
            name='pin_no',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
