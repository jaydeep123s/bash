# Generated by Django 3.0.4 on 2020-03-22 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamstudent', '0009_auto_20200322_0345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='ba_famulatur',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='ba_fsj_krankenhaus',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='ba_pflegepraktika',
            field=models.CharField(default='', max_length=100),
        ),
    ]
