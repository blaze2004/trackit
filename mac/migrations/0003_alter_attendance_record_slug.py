# Generated by Django 4.0 on 2022-04-11 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mac', '0002_attendance_record_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance_record',
            name='slug',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
