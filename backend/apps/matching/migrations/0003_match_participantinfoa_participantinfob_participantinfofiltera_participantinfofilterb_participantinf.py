# Generated by Django 3.0.7 on 2020-07-14 17:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0002_permission_group_creation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipantInfoA',
            fields=[
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('registration_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('participant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='info', serialize=False, to='matching.ParticipantA')),
                ('pers_info--first_name', models.CharField(blank=True, default='', max_length=100)),
                ('pers_info--last_name', models.CharField(max_length=100)),
                ('pers_info--phone_number', models.CharField(blank=True, default='', max_length=20)),
                ('info_supp--pref_area-ME', models.BooleanField(default=False)),
                ('info_supp--pref_area-PD', models.BooleanField(default=False)),
                ('info_supp--pref_area-HO', models.BooleanField(default=False)),
                ('info_supp--pref_area-ES', models.BooleanField(default=False)),
                ('info_supp--pref_area-PH', models.BooleanField(default=False)),
                ('info_supp--pref_area-NF', models.BooleanField(default=False)),
                ('info_supp--pref_area-LA', models.BooleanField(default=False)),
                ('info_supp--pref_area-MP', models.BooleanField(default=False)),
                ('info_supp--time_avail', models.IntegerField(choices=[(0, '10h per week'), (1, '20h per week'), (2, '30h per week'), (3, '40h per week')])),
                ('info_supp--accom', models.BooleanField(blank=True, default=False)),
                ('prof_train--medstud--experience', models.IntegerField(blank=True, choices=[(0, 'Preclinical Section'), (1, 'Last Year Student'), (2, 'Assistant Doctor'), (3, 'Consultant')], default=0, null=True)),
                ('prof_train--medstud--area-AN', models.BooleanField(default=False)),
                ('prof_train--medstud--area-SU', models.BooleanField(default=False)),
                ('prof_train--medstud--area-IM', models.BooleanField(default=False)),
                ('prof_train--medstud--area-IC', models.BooleanField(default=False)),
                ('prof_train--medstud--area-EM', models.BooleanField(default=False)),
                ('prof_train--medstud--area-GM', models.BooleanField(default=False)),
                ('prof_train--medstud--internship', models.BooleanField(blank=True, default=False)),
                ('prof_train--medstud--other', models.CharField(max_length=500)),
                ('prof_train--medstud-cond', models.BooleanField(default=False)),
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
                ('name', models.CharField(max_length=100)),
                ('contact', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantInfoLocationB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('registration_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('country_code', models.CharField(choices=[('DE', 'Germany'), ('AT', 'Austria')], default='DE', max_length=2)),
                ('plz', models.CharField(max_length=5, null=True)),
                ('radius', models.IntegerField(choices=[(10, '<10 km'), (20, '<20 km'), (30, '<40 km'), (40, '>40 km')], default=30)),
                ('participant_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='matching.ParticipantInfoB')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantInfoLocationA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('registration_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('country_code', models.CharField(choices=[('DE', 'Germany'), ('AT', 'Austria')], default='DE', max_length=2)),
                ('plz', models.CharField(max_length=5, null=True)),
                ('radius', models.IntegerField(choices=[(10, '<10 km'), (20, '<20 km'), (30, '<40 km'), (40, '>40 km')], default=30)),
                ('participant_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='matching.ParticipantInfoA')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantInfoFilterB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('registration_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('name', models.CharField(max_length=100)),
                ('name-icontains', models.CharField(blank=True, max_length=100, null=True)),
                ('contact-icontains', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number-icontains', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-registration_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantInfoFilterA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('registration_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('name', models.CharField(max_length=100)),
                ('info_supp--pref_area-ME-exact', models.NullBooleanField()),
                ('info_supp--pref_area-PD-exact', models.NullBooleanField()),
                ('info_supp--pref_area-HO-exact', models.NullBooleanField()),
                ('info_supp--pref_area-ES-exact', models.NullBooleanField()),
                ('info_supp--pref_area-PH-exact', models.NullBooleanField()),
                ('info_supp--pref_area-NF-exact', models.NullBooleanField()),
                ('info_supp--pref_area-LA-exact', models.NullBooleanField()),
                ('info_supp--pref_area-MP-exact', models.NullBooleanField()),
                ('info_supp--time_avail-gte', models.IntegerField(blank=True, choices=[(None, 'No choice'), (0, '10h per week'), (1, '20h per week'), (2, '30h per week'), (3, '40h per week')], null=True)),
                ('info_supp--time_avail-lte', models.IntegerField(blank=True, choices=[(None, 'No choice'), (0, '10h per week'), (1, '20h per week'), (2, '30h per week'), (3, '40h per week')], null=True)),
                ('info_supp--accom-exact', models.NullBooleanField()),
                ('prof_train--medstud-cond-exact', models.NullBooleanField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-registration_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True)),
                ('initiator', models.CharField(choices=[('A', 'A'), ('B', 'B')], max_length=1)),
                ('match_date', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('state', models.IntegerField(choices=[(1, 'contacted'), (2, 'successful'), (3, 'not successful'), (4, 'blocked')], default=1)),
                ('contact_text', models.CharField(blank=True, max_length=500)),
                ('filterA', models.ForeignKey(blank=True, null=True, on_delete=models.SET(None), to='matching.ParticipantInfoFilterA')),
                ('filterB', models.ForeignKey(blank=True, null=True, on_delete=models.SET(None), to='matching.ParticipantInfoFilterB')),
                ('participantA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.ParticipantA')),
                ('participantB', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matching.ParticipantB')),
            ],
        ),
    ]
