# Generated by Django 4.2.7 on 2023-11-04 09:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approvers', models.TextField(default='')),
                ('details', tinymce.models.HTMLField()),
                ('created_date', models.DateField(default=django.utils.timezone.now)),
                ('created_time', models.TimeField(default=django.utils.timezone.now)),
                ('attachment', models.FileField(default='attachment', upload_to='approval_files')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('cancelled', 'cancelled'), ('complete', 'complete')], default='pending', max_length=10)),
                ('stage', models.IntegerField(default=0)),
                ('rate', models.IntegerField(default=0)),
                ('expected', models.IntegerField(default=0)),
                ('start', models.DateField(default=django.utils.timezone.now)),
                ('end', models.DateField(default=django.utils.timezone.now)),
                ('days', models.IntegerField(default=0)),
                ('remarks', models.TextField()),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Approvals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=10)),
                ('approvers', models.TextField(default='')),
                ('created', models.DateField(default=django.utils.timezone.now)),
                ('remarks', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AttSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=100, null=True)),
                ('start', models.TimeField(default=datetime.datetime(2023, 11, 4, 9, 56, 50, 172516, tzinfo=datetime.timezone.utc))),
                ('end', models.TimeField(default=datetime.datetime(2023, 11, 4, 9, 56, 50, 172538, tzinfo=datetime.timezone.utc))),
                ('deduction_per_day', models.FloatField(default=0.0)),
                ('expected_days', models.FloatField(default=24.0)),
                ('leave_days', models.FloatField(default=21.0)),
                ('remarks', models.TextField(default='')),
                ('clock_in_latitude', models.CharField(default='', max_length=1000)),
                ('clock_in_longitude', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='None', max_length=50)),
                ('hod_username', models.CharField(default='None', max_length=50)),
                ('size', models.FloatField(default=1)),
                ('created', models.DateField(default=django.utils.timezone.now)),
                ('remarks', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='FilesCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='None', max_length=50)),
                ('requirements', models.CharField(default='None', max_length=50)),
                ('created', models.DateField(default=django.utils.timezone.now)),
                ('remarks', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('created', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recpient_id', models.CharField(default='', max_length=30)),
                ('details', models.TextField()),
                ('links', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='user.jpeg', upload_to='profile_images')),
                ('first', models.CharField(default='None', max_length=50)),
                ('surname', models.CharField(default='None', max_length=50)),
                ('email', models.EmailField(default='user@gmail.com', max_length=254)),
                ('phone', models.CharField(default='None', max_length=20)),
                ('activation', models.CharField(default='None', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', tinymce.models.HTMLField()),
                ('created', models.DateField()),
                ('attachments', models.FileField(default='process.pdf', upload_to='application_files')),
                ('status', models.CharField(choices=[('pending', 'pending'), ('cancelled', 'cancelled'), ('complete', 'complete')], default='pending', max_length=10)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('approvals', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='processes', to='management.approvals')),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField()),
                ('url', models.CharField(default='', max_length=100)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
                ('seen', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('annual', 'annual'), ('sick', 'sick'), ('compassionate', 'compassionate'), ('office', 'office')], default='', max_length=100)),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(default=django.utils.timezone.now)),
                ('days', models.FloatField(default=0)),
                ('attachments', models.FileField(default='attachment.pdf', upload_to='application_files')),
                ('status', models.CharField(default='pending', max_length=30)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('details', models.TextField()),
                ('Approvals_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='leave', to='management.approvals')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='applicant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('details', models.TextField()),
                ('category', models.CharField(choices=[('announcement', 'announcement'), ('events', 'events'), ('updates', 'updates')], default='', max_length=100)),
                ('viewers', models.CharField(choices=[('all', 'all'), ('members', 'members'), ('admins', 'admins')], default='', max_length=100)),
                ('viewers_list', models.TextField(default='')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('files', models.FileField(default='posts.png', upload_to='posts_files')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(default='None', max_length=50)),
                ('first_name', models.CharField(default='None', max_length=50)),
                ('second_name', models.CharField(default='None', max_length=50)),
                ('national_no', models.CharField(default='None', max_length=50)),
                ('kra_pin', models.CharField(default='None', max_length=50)),
                ('email', models.EmailField(default='None', max_length=254)),
                ('dob', models.DateField(default=django.utils.timezone.now)),
                ('phone', models.CharField(default='None', max_length=50)),
                ('next_kin_name', models.CharField(default='None', max_length=50)),
                ('next_kin_id', models.CharField(default='None', max_length=50)),
                ('next_kin_phone', models.CharField(default='None', max_length=50)),
                ('address', models.CharField(default='None', max_length=50)),
                ('location', models.CharField(default='None', max_length=50)),
                ('office', models.CharField(default='None', max_length=50)),
                ('education_level', models.CharField(default='None', max_length=50)),
                ('doj', models.DateField(default=django.utils.timezone.now)),
                ('dol', models.DateField(default=django.utils.timezone.now)),
                ('account_no', models.CharField(default='None', max_length=50)),
                ('bank_name', models.CharField(default='None', max_length=50)),
                ('salary', models.FloatField(default=0.0)),
                ('allowance', models.FloatField(default=0.0)),
                ('add_ons', models.FloatField(default=0.0)),
                ('other_fields', models.TextField(default='name:value')),
                ('status', models.CharField(choices=[('incomplete', 'incomplete'), ('active', 'active'), ('resigned', 'resigned'), ('terminated', 'terminated'), ('suspended', 'suspended')], default='None', max_length=50)),
                ('image', models.ImageField(default='emoloyee.png', upload_to='emp_images')),
                ('departments', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='management.department')),
                ('payroll_settings', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='payroll.payrollsetting')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='management.roles')),
            ],
        ),
        migrations.CreateModel(
            name='EmpFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.CharField(max_length=100)),
                ('file_name', models.CharField(default='none', max_length=100)),
                ('document', models.FileField(default='document.pdf', upload_to='emp_files')),
                ('properties', models.TextField(default='none')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.filescategory')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', tinymce.models.HTMLField()),
                ('anonymous', models.BooleanField(default=False)),
                ('sent', models.DateTimeField(default=datetime.datetime(2023, 11, 4, 9, 56, 50, 195761, tzinfo=datetime.timezone.utc))),
                ('seen', models.BooleanField(default=False)),
                ('file', models.FileField(null=True, upload_to='chat_files')),
                ('anonymous_sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='anonymous_sender', to='management.profile')),
                ('recep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_recepient', to='management.profile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_sender', to='management.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_leave', models.BooleanField(default=False)),
                ('day', models.DateField(default=django.utils.timezone.now)),
                ('clock_in', models.CharField(default='', max_length=1000)),
                ('clock_out', models.CharField(default='', max_length=1000)),
                ('lat', models.CharField(default='', max_length=10)),
                ('long', models.CharField(default='', max_length=10)),
                ('lat1', models.CharField(default='', max_length=10)),
                ('long1', models.CharField(default='', max_length=10)),
                ('image1', models.TextField()),
                ('image2', models.TextField()),
                ('status', models.CharField(default='partial', max_length=100)),
                ('counts', models.IntegerField(default=0)),
                ('hours', models.FloatField(default=0.0)),
                ('days', models.FloatField(default=0.0)),
                ('leave_days', models.IntegerField(default=21)),
                ('deductions', models.FloatField(default=0.0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('remarks', models.TextField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.employee')),
            ],
        ),
        migrations.CreateModel(
            name='approvalTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(default='no comment')),
                ('status', models.CharField(default='pending', max_length=100)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time', models.TimeField(default=django.utils.timezone.now)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.applications')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='applications',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='management.approvals'),
        ),
    ]
