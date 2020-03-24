# Generated by Django 3.0.4 on 2020-03-24 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamstudent', '0002_auto_20200324_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='name_first',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='student',
            name='name_last',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='student',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=100, unique=True),
        ),
    ]