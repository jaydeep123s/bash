# Generated by Django 3.0.4 on 2020-03-22 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iamstudent', '0012_remove_student_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='braucht_bezahlung',
            field=models.IntegerField(choices=[(1, 'Unentgeltlich'), (2, 'Minijob'), (3, 'Vollzeit')], default=1),
        ),
    ]
