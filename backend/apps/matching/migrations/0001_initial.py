# Generated by Django 3.0.7 on 2020-06-20 19:40

import datetime
import uuid

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_participant', models.BooleanField(default=False)),
                ('is_A', models.BooleanField(default=False)),
                ('is_B', models.BooleanField(default=False)),
                ('validated_email', models.BooleanField(default=False)),
                ('email_validation_date', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantA',
            fields=[
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('registration_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('is_activated', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='a', serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantB',
            fields=[
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('registration_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('is_activated', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='b', serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ParticipantInfoA',
            fields=[
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('registration_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('participant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='info', serialize=False, to='matching.ParticipantA')),
                ('personal_information--first_name', models.CharField(blank=True, default='', max_length=100)),
                ('personal_information--last_name', models.CharField(max_length=100)),
                ('personal_information--phone_number', models.CharField(blank=True, default='', max_length=20)),
                ('information_about_support--preferred_area_of_help-ME', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-PD', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-HO', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-ES', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-PH', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-NF', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-LA', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-MP', models.BooleanField(default=False)),
                ('information_about_support--time_availability_per_week', models.IntegerField(choices=[(0, '10h per week'), (1, '20h per week'), (2, '30h per week'), (3, '40h per week')])),
                ('information_about_support--i_need_accommodation', models.BooleanField(blank=True, default=False)),
                ('professional_training--medical_student_or_doctor--experience_level', models.IntegerField(blank=True, choices=[(0, 'Preclinical Section'), (1, 'Last Year Student'), (2, 'Assistant Doctor'), (3, 'Consultant')], default=0, null=True)),
                ('professional_training--medical_student_or_doctor--area_of_expertise-AN', models.BooleanField(default=False)),
                ('professional_training--medical_student_or_doctor--area_of_expertise-SU', models.BooleanField(default=False)),
                ('professional_training--medical_student_or_doctor--area_of_expertise-IM', models.BooleanField(default=False)),
                ('professional_training--medical_student_or_doctor--area_of_expertise-IC', models.BooleanField(default=False)),
                ('professional_training--medical_student_or_doctor--area_of_expertise-EM', models.BooleanField(default=False)),
                ('professional_training--medical_student_or_doctor--area_of_expertise-GM', models.BooleanField(default=False)),
                ('professional_training--medical_student_or_doctor--recognition_as_an_internship_or_other_study_requirements_is_important', models.BooleanField(blank=True, default=False)),
                ('professional_training--medical_student_or_doctor--other_qualifications', models.CharField(max_length=500)),
                ('professional_training--medical_student_or_doctor-condition', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantInfoB',
            fields=[
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('registration_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('participant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='info', serialize=False, to='matching.ParticipantB')),
                ('personal_information--first_name', models.CharField(blank=True, default='', max_length=100)),
                ('personal_information--last_name', models.CharField(max_length=100)),
                ('personal_information--phone_number', models.CharField(blank=True, default='', max_length=20)),
                ('information_about_support--preferred_area_of_help-ME', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-PD', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-HO', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-ES', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-PH', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-NF', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-LA', models.BooleanField(default=False)),
                ('information_about_support--preferred_area_of_help-MP', models.BooleanField(default=False)),
                ('information_about_support--time_availability_per_week', models.IntegerField(choices=[(0, '10h per week'), (1, '20h per week'), (2, '30h per week'), (3, '40h per week')])),
                ('information_about_support--i_need_accommodation', models.BooleanField(blank=True, default=False)),
                ('professional_training--medical_student_or_doctor--experience_level', models.IntegerField(blank=True, choices=[(0, 'Preclinical Section'), (1, 'Last Year Student'), (2, 'Assistant Doctor'), (3, 'Consultant')], default=0, null=True)),
                ('professional_training--medical_student_or_doctor--area_of_expertise-AN', models.BooleanField(default=False)),
                ('professional_training--medical_student_or_doctor--area_of_expertise-SU', models.BooleanField(default=False)),
                ('professional_training--medical_student_or_doctor--area_of_expertise-IM', models.BooleanField(default=False)),
                ('professional_training--medical_student_or_doctor--area_of_expertise-IC', models.BooleanField(default=False)),
                ('professional_training--medical_student_or_doctor--area_of_expertise-EM', models.BooleanField(default=False)),
                ('professional_training--medical_student_or_doctor--area_of_expertise-GM', models.BooleanField(default=False)),
                ('professional_training--medical_student_or_doctor--recognition_as_an_internship_or_other_study_requirements_is_important', models.BooleanField(blank=True, default=False)),
                ('professional_training--medical_student_or_doctor--other_qualifications', models.CharField(max_length=500)),
                ('professional_training--medical_student_or_doctor-condition', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='participantb',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='matching.Staff'),
        ),
        migrations.AddField(
            model_name='participanta',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='matching.Staff'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(('is_A', True), ('is_B', True), _negated=True), name='matching_user_has_only_one_participant'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(('is_participant', False), ('is_staff', False), _connector='OR'), name='matching_user_only_staff_or_participant_or_none'),
        ),
        migrations.CreateModel(
            name='ParticipantInfoLocationA',
            fields=[
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('registration_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('country_code', models.CharField(choices=[('DE', 'Germany'), ('AT', 'Austria')], default='DE', max_length=2)),
                ('plz', models.CharField(max_length=5, null=True)),
                ('radius', models.IntegerField(choices=[(10, '<10 km'), (20, '<20 km'), (30, '<40 km'), (40, '>40 km')], default=30)),
                ('participant_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='location', serialize=False, to='matching.ParticipantInfoA')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantInfoLocationB',
            fields=[
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('registration_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('country_code', models.CharField(choices=[('DE', 'Germany'), ('AT', 'Austria')], default='DE', max_length=2)),
                ('plz', models.CharField(max_length=5, null=True)),
                ('radius', models.IntegerField(choices=[(10, '<10 km'), (20, '<20 km'), (30, '<40 km'), (40, '>40 km')], default=30)),
                ('participant_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='location', serialize=False, to='matching.ParticipantInfoB')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
